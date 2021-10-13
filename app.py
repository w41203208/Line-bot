import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("F5OQYnRnsuiAf51vzmRiswuQ/VAI06Ag5AVrDookZoapt+GEkfJFvbKJYBp08IrGPPJjqRHwu7HIJbfQs58T2zbPfh9zCQbnOsE2NWNYSgOBGlpcwFPQ7PDiOrpVNmZg6bTJ4zmeh4E6r1P86w6BugdB04t89/1O/w1cDnyilFU="))
handler = WebhookHandler(os.environ.get("1497d9253b7fc842f5ba2a22c15b9ce7"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text

    # Send To Line
    reply = TextSendMessage(text=f"{get_message}")
    line_bot_api.reply_message(event.reply_token, reply)
