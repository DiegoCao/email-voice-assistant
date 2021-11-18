import flask
from flask import request
import backend
import backend.ezgmail as ezgmail


@backend.app.route('/', methods=["GET"])
def index():
    return "helloworld"


@backend.app.route('/api/email/', methods=["GET"])
def email():
    email_id = request.args.get("id", default=-1, type=int)
    message_dict = _email_to_dict(email_id)
    if message_dict:
        message_dict["success"] = True
        return flask.jsonify(message_dict)
    else:
        return flask.jsonify({
            'success': False,
            "error": "IndexError"
        }), 400


@backend.app.route("/api/command/", methods=["GET"])
def command():
    req_dict = request.get_json(force=True)  # directly a dict
    print(req_dict)
    try:
        response = _command(
            req_dict["id"], req_dict["command"], req_dict["args"])
    except Exception as e:
        return flask.jsonify({
            'success': False,
            'error': str(e)
        }), 400
    return flask.jsonify({
        'success': True,
        'response': response
    })


def _email_to_dict(message):
    message_dict = {
        "id": message.id,
        "from": message.sender,
        "to": message.recipient.split(","),
        "subject": message.subject,
        "time": message.timestamp,
        "body": message.body
    }
    return message_dict


def _command(email_id, command, args={}):
    """Parse and execute the command.

    List of current avaliable commands:
    1. `read` - no args
    2. `unread` - no args
    3. `spam` - no args
    4. `delete` - no args
    5. `search`
        - `query`: a string, see details @ https://support.google.com/mail/answer/7190?hl=en
    6. `show` - no args
    TODO:
    1. `forward` to a list of users with/without new content
    2. `reply`
    """
    response = None
    labeling = ["read", "unread", "spam", "delete"]
    if command in labeling:
        # Simple labeling & No response
        m = ezgmail.get(email_id)  # Absolute index from previous query
        if command == 'read':
            m.markAsRead()
        elif command == 'unread':
            m.markAsUnread()
        elif command == 'spam':
            m.markAsSpam()
        elif command == 'delete':
            m.trash() 
    else:
        # Query (for now)
        if command == "search":
            query = args["query"]
            m = ezgmail.getMessage(query)  # Return the first matched message
            response = _email_to_dict(message=m)
        elif command == "show":
            m = ezgmail.get(email_id)
            response = _email_to_dict(message=m)
    return response
