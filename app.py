import os
from datetime import datetime

from flask import Flask, abort, request
import json

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

@app.route("/", methods=["GET", "POST"])
def home_page_render():

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
    global action, match
    get_message = event.message.text


    action = get_message
    reply_msg = getActionReplyMsg()

    # Send To Line
    if reply_msg == 'See Flex Msg':
        FlexMessage = json.load(open('./assets/card.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    else:
        reply = TextSendMessage(text=f"{reply_msg}")
        line_bot_api.reply_message(event.reply_token, reply)

def getActionReplyMsg():
    global action, match
    if action == "hi":
        match = True
        return "您好!請問需要什麼幫助嗎？"
    elif action == "我想看資訊欄":
        return 'See Flex Msg'
    else:
        action = ""
        match = ''
        return "沒有此指令，請確認後再輸入"

