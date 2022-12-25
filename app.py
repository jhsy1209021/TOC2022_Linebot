import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FollowEvent

from fsm import TocMachine
from utils import send_text_message, send_welcome_message

load_dotenv()


machine = TocMachine(
    states=["user", "menu", "meal_type", "add_calories", "meal_name", "exercise_type", "sub_calories", "summary"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "meal_type",
            "conditions": "is_going_to_meal_type",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "exercise_type",
            "conditions": "is_going_to_exercise_type",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "summary",
            "conditions": "is_going_to_summary",
        },
        {
            "trigger": "advance",
            "source": "meal_type",
            "dest": "meal_name",
            "conditions": "is_going_to_meal_name",
        },
        {
            "trigger": "advance",
            "source": "meal_name",
            "dest": "add_calories",
            "conditions": "is_going_to_add_calories",
        },
        {
            "trigger": "advance",
            "source": "exercise_type",
            "dest": "sub_calories",
            "conditions": "is_going_to_sub_calories",
        },
        {
            "trigger": "advance",
            "source": "add_calories",
            "dest": "menu",
            "conditions": "complete_add_calories",
        },
        {
            "trigger": "advance",
            "source": "sub_calories",
            "dest": "menu",
            "conditions": "complete_sub_calories",
        },
        {
            "trigger": "advance",
            "source": "summary",
            "dest": "menu",
            "conditions": "is_going_back_to_menu",
        },
        {
            "trigger": "advance",
            "source": "summary",
            "dest": "user",
            "conditions": "is_going_back_to_user",
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

"""
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"
"""

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            if isinstance(event, FollowEvent):
                send_welcome_message(event.reply_token)
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        # if response == False:
        #     send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
