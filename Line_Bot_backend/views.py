from flask import Blueprint, jsonify, request, abort
import json
import os

#from pymysql import NULL

#from .models import Product, ProteinRange
#from . import db

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage


views = Blueprint('views', __name__)

#CHANNEL_ACCESS_TOKEN = "F5OQYnRnsuiAf51vzmRiswuQ/VAI06Ag5AVrDookZoapt+GEkfJFvbKJYBp08IrGPPJjqRHwu7HIJbfQs58T2zbPfh9zCQbnOsE2NWNYSgOBGlpcwFPQ7PDiOrpVNmZg6bTJ4zmeh4E6r1P86w6BugdB04t89/1O/w1cDnyilFU="
#CHANNEL_SECRET = "1497d9253b7fc842f5ba2a22c15b9ce7"

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))
#line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
#handler = WebhookHandler(CHANNEL_SECRET)

medicalMatch = ''
searchMatch = ''


@views.route("/", methods=["GET", "POST"])
def home_page_render():

    if request.method == "GET":
        return "Hello Herokuuuu"
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
    global medicalMatch, searchMatch
    get_message = event.message.text


    action = get_message
    reply_msg = getActionReplyMsg(action)

    # Send To Line
    if reply_msg == 'See Flex Msg': #衛教資訊
        FlexMessage = json.load(open('./assets/card.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif reply_msg == "getMedical":
        reply_msg = "可獲得衛教資訊!"

        reply = TextSendMessage(text=f"{reply_msg}")
        line_bot_api.reply_message(event.reply_token, reply)
    elif reply_msg == 'getSearchFood':
        sql_text = get_message


        FlexMessage = json.load(open('./assets/card.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))

    else:
        reply = TextSendMessage(text=f"{reply_msg}")
        line_bot_api.reply_message(event.reply_token, reply)

def getActionReplyMsg(action):
    global medicalMatch, searchMatch
    if action == "飲食查詢":
        searchMatch = True
        medicalMatch = False
        return 'Success to search u can do next step'
    elif action == "衛教資訊":
        medicalMatch = True
        searchMatch = False
        return 'getMedical'
    elif searchMatch == True and action != '':
        return 'getSearchFood'
    else:
        return action
