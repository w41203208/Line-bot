from flask import Blueprint, jsonify, request, abort
import json
import os

#from .models import Food
#from .api import GETfoodDataAPI
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
    get_message = event.message.text

    if get_message == '衛教資訊':
        FlexMessage = json.load(open('./assets/medical.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '第一、二期資訊':
        FlexMessage = json.load(open('./assets/medical-indicate-one.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '第三期資訊':
        FlexMessage = json.load(open('./assets/medical-indicate-three.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '第四期資訊':
        FlexMessage = json.load(open('./assets/medical-indicate-four.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '第五期資訊':
        FlexMessage = json.load(open('./assets/medical-indicate-five.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '血液透析':
        FlexMessage = json.load(open('./assets/blood.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '腹膜透析':
        FlexMessage = json.load(open('./assets/fomo.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))

    else: #只要資料庫找的到的都輸出foodData
        '''
        query_text = '蛋糕' #query_text = get_message
        outputData = Food.query.filter(Food.product_name.like('%'+ query_text + '%') if query_text is not None else '').all()
        res = GETfoodDataAPI(outputData).excute()
        print(res)
        '''

        if get_message != '蛋糕': #if outputData is exist:
            reply_msg = get_message
            reply = TextSendMessage(text=f"{reply_msg}")
            line_bot_api.reply_message(event.reply_token, reply)
        else:
            FlexMessage = json.load(open('./assets/search.json', 'r', encoding='utf-8'))
            line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))



