import json
import flask
import nlp
from flask import request
import requests
import os
import sys
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pathlib import Path
from tkinter import *
import logging

fp = open('log.txt', 'w')


@nlp.app.route('/', methods=["GET"])
def base():
    return "Welcome to the NLP server!"


@nlp.app.route('/voice/', methods=["POST"])
def parse_voice():
    fp = open('log.txt', 'a')
    voice_file = request.files["voice"]
    voice_file.save("test.mp3")
    sound = AudioSegment.from_mp3("test.mp3")
    sound.export("test.wav", format="wav")
    # 1. speech 2 text
    user_text = _speech_to_text(voice_file)
    # TODO: Ambiguity Regex Match!
    user_text = user_text.replace("*", "star")  # FIX ME!!!
    user_text = user_text.replace("start", "star")
    user_text = user_text.replace("fire", "star")
    user_text = user_text.replace("stop", "star")
    # logging.info(user_text)
    fp.write("User: "+user_text+"\n")

    # 2. parse command, email_id & args
    command = _parse_command(user_text)
    # text = "Receive your command: " + command
    # fp.write(text+"\n")

    email_id = 0
    args = {}

    # 3. send command to backend
    if command != "default":
        response = _send_command(command, email_id, args)

    # 4. response = generated by AI
    print('response generate')
    bot_text = "Sorry, can you speak again?" if command == "default" else "OK."
    if command == "show":
        bot_text = _mail_dict_to_str(response)
        bot_text += "\n--------------------\nWhat can I do for you?"
        bot_text = "SHOW"+bot_text

    fp.write(bot_text+"\n")

    return flask.jsonify({
        "user": user_text,
        "bot": bot_text
    })


@nlp.app.route('/response/', methods=["GET"])
def get_response():
    user_text = request.args.get('text')
    fp.write("User: "+user_text+"\n")
    command = _parse_command(user_text)
    email_id = 0
    args = {}
    if command != "default":
        response = _send_command(command, email_id, args)
    bot_text = "Sorry, can you speak again?" if command == "default" else "OK."
    if command == "show":
        bot_text = _mail_dict_to_str(response)
        bot_text += "\n--------------------\nWhat can I do for you?"
        bot_text = "SHOW"+bot_text

    fp.write(bot_text+"\n")
    return flask.jsonify({
        "bot": bot_text
    })


def _mail_dict_to_str(mail_dict):
    """
    >>> mail_dict = {
            "id": email_id,
            "from": message.sender,
            "to": message.recipient.split(","),
            "subject": message.subject,
            "time": message.timestamp,
            "body": message.body
        }
    """
    _to_print = []
    _to_print.append("{:10s}: {}".format("Subject", mail_dict["subject"]))
    _to_print.append("{:10s}: {}".format("From", mail_dict["from"]))
    _to_print.append("{:10s}: {}".format("To", ";".join(mail_dict["to"])))
    _to_print.append("{:10s}: {}".format("Time", mail_dict["time"]))
    _to_print.append("{:10s}: \n{}".format("Body", mail_dict["body"]))
    return "\n".join(_to_print)


def _send_command(command, email_id, args):
    # pass
    email_dict = _get_email(email_id)  # for other functionalities
    command_dict = {
        "id": email_id,
        "command": command,
        "args": args
    }
    response = requests.get(
        f"http://localhost:{nlp.app.config['BACKEND_SERVER_PORT']}/api/command/", json=command_dict)
    print(response)
    data = response.json()
    print(data)
    return data["response"]


def _get_email(email_id):
    return requests.get(f"http://localhost:{nlp.app.config['BACKEND_SERVER_PORT']}/api/email/").json()


def _speech_to_text(path, verbose=False):
    '''
    path:       the path to the speech file
    returns:    text version of speech content
    '''
    r = sr.Recognizer()
    text = ""
    with sr.AudioFile(path) as source:
        audio_text = r.listen(source)
        text = ""
        try:
            text = r.recognize_google(audio_text)
            if verbose:
                print('Converting audio transcripts into text ...')
                print(text)
        except:
            print('Sorry.. run again...')
    return text


def _parse_command(text, keywords=Path(nlp.__file__).parent / "command_keywords.txt"):
    '''
    text:       the text to be parsed for commands
    keywords:   either a set of string, or a path to keywords_file
    returns:    query dict containing counts of each keyword
    '''

    # get keywords first
    if isinstance(keywords, set):
        keywords = keywords
    else:
        try:
            keywords_file = open(keywords, 'r+')
            keywords = set(line.rstrip() for line in keywords_file.readlines())
        except FileNotFoundError:
            print("Keywords file not found")

    def preprocess(word: str) -> str:
        return word.lower()  # FIXME:

    query = dict()
    for word in text.split(' '):
        word = preprocess(word)
        if word in keywords:
            query[word] = query.get(word, 0) + 1

    command = "default"
    max_count = -1
    for keyword, count in query.items():
        if count > max_count:
            command = keyword

    if command == "*":
        command = "star"  # Fix Me!
    return command


def _text_to_audio(text: str, save_file: str, language="en", slow=False):
    audio_obj = gTTS(text=text, lang=language, slow=slow)
    ext = os.path.splitext(save_file)[-1]
    if ext.lower() == ".mp3":
        audio_obj.save(save_file)
    elif ext.lower() == ".wav":
        audio_obj.save("/tmp/tmp.mp3")
        sound = AudioSegment.from_mp3("/tmp/tmp.mp3")
        sound.export(save_file, format="wav")
    else:
        print("Unsupported format, available formats are mp3 and wav", file=sys.stderr)
        raise NotImplementedError
