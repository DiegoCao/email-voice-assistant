import React, { useState, useEffect, useRef } from 'react';
import './scoped.css';
import RobIcon from '../../img/RobIcon.png';
import UserIcon from '../../img/UserIcon.png';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import { AudioOutlined } from '@ant-design/icons';
import axios from 'axios';

const ChatBox = () => {
  const {
    transcript,
    finalTranscript,
    resetTranscript,
  } = useSpeechRecognition();
  const chatRef = useRef(null);
  const [isBlocked, setIsBlocked] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [msg, setMsg] = useState([]);
  const [speaker, setSpeaker] = useState([]); //0 for assistant, 1 for user
  navigator.getUserMedia = ( navigator.getUserMedia ||
                       navigator.webkitGetUserMedia ||
                       navigator.mozGetUserMedia ||
                       navigator.msGetUserMedia);
  useEffect (() => {
    navigator.getUserMedia({ audio: true },
      () => {
        console.log('Permission Granted');
        setIsBlocked(false);
      },
      () => {
        console.log('Permission Denied');
        setIsBlocked(true);
      },
    );
    var openMsg =
      "Hi, I am your intelligent voice email assistant. What can I help you?";
    setMsg([...msg, openMsg]);
    setSpeaker([...speaker, 0]);
    setTimeout(() => {
      speak(openMsg);
    }, 1000);
  }, [])

  function speak(message) {
    var msg = new SpeechSynthesisUtterance(message);
    var voices = window.speechSynthesis.getVoices();
    msg.voice = voices[0];
    window.speechSynthesis.speak(msg);
  }

  function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

  function punctuate(string){
    // Punctuate according to rule
    const question = ["what", "who", "how", "when", "which", "whom", "whose", "why", "may", "can", "could"];
    var first_word = string.split(" ")[0];
    if (question.includes(first_word.toLowerCase())) {
      string += "?";
    } else {
      string += ".";
    }
    return string
  }

  const startSpeak = () => {
    setIsRecording(true);
    resetTranscript();
    setMsg([...msg, '...']);
    setSpeaker([...speaker, 1]);
    SpeechRecognition.startListening({ language: 'en-US' });
  }
  
  const stopSpeak = async () => {
    setIsRecording(false);
    SpeechRecognition.stopListening();
    var trans = "";
    var trans_cur = String(transcript);
    var trans_final = String(finalTranscript);
    if (trans_final) {  // if the final transcript is ready, use the final one
      trans = trans_final;
    } else {
      trans = trans_cur;
    }
    console.log(trans);
    trans = punctuate(trans);
    trans = capitalizeFirstLetter(trans);
    trans = trans.replace("start","star");
    trans = trans.replace("rat","read");
    var msgArr = [...msg.slice(0,-1), trans];
    setMsg(msgArr);
    await axios.get('/response/',{
      headers: {
                'Access-Control-Allow-Origin': '*'
      },
      params: {
          text: trans
      }
    }).then(res => {
        setMsg([...msgArr,res.data.bot]);
        setSpeaker([...speaker, 0]);
        setTimeout(() => {
          speak(res.data.bot);
        }, 1000);
      }
    ).then (err=>{
      console.log(err);
    })
  }

  useEffect(()=>{
    chatRef.current.scrollIntoView({ behavior: 'smooth',block: "end" });
  })

  return (
    <div className="chat-box-div">
      <div className="chat-box">
        {
          msg.map((m,i) => (
              !speaker[i] ? (
                <div className="assistant-box">
                  <img  className="assistant-avatar" src={RobIcon} />
                  <div className="assistant-msg">
                    {m}
                  </div>
                </div>
              ) : (
                speaker[i] && (
                <div className="user-box">
                  <img  className="user-avatar" src={UserIcon} />
                  <div className="user-msg">
                    {m}
                  </div>
                </div>
              )
              )
            )
          )
        }
        <div ref={chatRef}></div>
      </div>
      <div className="record-listen">
            {
              isRecording && (
                <div className="mic-box" onClick={stopSpeak} >
                  <AudioOutlined style={{ fontSize: 27 }}/><br/>
                  Stop
                </div>
              )
            }
            {
              !isRecording && (
                <div className="mic-box" onClick={startSpeak} >
                  < AudioOutlined style={{ fontSize: 27 }}/><br/>
                  Record
                </div>
              )
            }
      </div>
    </div>
  );
}

export default ChatBox;
