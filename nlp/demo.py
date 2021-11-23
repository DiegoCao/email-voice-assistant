from google.cloud import dialogflow
import requests
import datetime
# import nlp
from nlp.api.nlp_server import Dialogflow_session, _send_command

OPERATIONS = ["read","unread","delete","spam"]

df_session = Dialogflow_session(session_id=5678)
while True:
    user_text = input("Enter user text: ")
    # print("user text: ", user_text)
    if user_text == "quit":
        break
    action, email_ids, args, bot_text = df_session.parse_command_dialogflow(user_text)


    action_type = action.split('.')[0]
    command = action.split('.')[1]  # e.g. read, unread, spam...

    # send command to backend only when the action is a "command" type and command is in OPERATIONS (operations on an email)
    if action_type == "command":
        if command in OPERATIONS:  # send command to backend only when command is in OPERATIONS (operations on an email)
            for email_id in email_ids:
                _send_command(command, email_id, args)
        elif command == "speak":  # read the email out for the user
            sender = df_session.curr_email_dict["from"]
            email_body = df_session.curr_email_dict["body"]
            extra_bot_text = f" The email is from {sender}. The body is as follows: {email_body}"
            bot_text += extra_bot_text
            # todo: do we need to mark it as read?

    print("action: ", action)
    print("email ids: ", email_ids)
    print("args: ", args)
    print("bot text: ", bot_text)
    print('-' * 20)


