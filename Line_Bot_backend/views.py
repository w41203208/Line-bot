from flask import Blueprint, jsonify, request, abort
import json
import os
import requests

#from .models import Food
#from .api import GETfoodDataAPI
#from . import db

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, URIAction,MessageAction


views = Blueprint('views', __name__)

CHANNEL_ACCESS_TOKEN = "F5OQYnRnsuiAf51vzmRiswuQ/VAI06Ag5AVrDookZoapt+GEkfJFvbKJYBp08IrGPPJjqRHwu7HIJbfQs58T2zbPfh9zCQbnOsE2NWNYSgOBGlpcwFPQ7PDiOrpVNmZg6bTJ4zmeh4E6r1P86w6BugdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "1497d9253b7fc842f5ba2a22c15b9ce7"

#line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
#handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

headers = headers = {"Authorization":"Bearer F5OQYnRnsuiAf51vzmRiswuQ/VAI06Ag5AVrDookZoapt+GEkfJFvbKJYBp08IrGPPJjqRHwu7HIJbfQs58T2zbPfh9zCQbnOsE2NWNYSgOBGlpcwFPQ7PDiOrpVNmZg6bTJ4zmeh4E6r1P86w6BugdB04t89/1O/w1cDnyilFU=" , "Content-Type":"application/json"}
member_rich_menu = "richmenu-93edef72aca9a5c99ffbadc42253fffd"
default_rich_menu = "richmenu-d621822ebadba6020b56a4fc76f08595"

@views.route("/callback", methods=["GET", "POST"])
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



    '''
    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=1686),
        selected=False,
        name="Nice richmenu",
        chat_bar_text="KCS小助手",
        areas=[
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=2500, height=1686),
                action=MessageAction(label='個人資訊', text='個人資訊')
            )
        ]
    )
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    with open('./assets/images/test.jpeg', 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, "image/jpeg", f)
    '''
    #requests.post('https://api.line.me/v2/bot/user/all/richmenu/'+ default_rich_menu, headers=headers)




    rich_menu_list = line_bot_api.get_rich_menu_list()
    for item in rich_menu_list:
        print(item.rich_menu_id)


    #if event.source.user_id 還沒在database裡 = default  2. 按下註冊後會推memberRichMenu給user並將userId存到資料庫
    if event.source.user_id == get_message:
        line_bot_api.link_rich_menu_to_user(event.source.user_id, member_rich_menu)
    else:
        line_bot_api.link_rich_menu_to_user(event.source.user_id, default_rich_menu)




    if get_message == "D" :
        rich_menu_list = line_bot_api.get_rich_menu_list()
        for i in rich_menu_list:
            line_bot_api.delete_rich_menu(i.rich_menu_id)


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
    elif get_message == '血壓血糖控制':
        FlexMessage = json.load(open('./assets/_info1-bsContral.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '認識【蛋白質飲食】':
        FlexMessage = json.load(open('./assets/_info2-knowProtein.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '認識【鉀】含量高的食物':
        FlexMessage = json.load(open('./assets/_info3-knowKa.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '認識【磷】含量高的食物':
        FlexMessage = json.load(open('./assets/_info4-knowP.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '蛋白質飲食(第三期)':
        FlexMessage = json.load(open('./assets/_info5-proteinEat.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '水份控制':
        FlexMessage = json.load(open('./assets/_info6-waterContral.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '蛋白質飲食(第四期)':
        FlexMessage = json.load(open('./assets/_info5-proteinEat.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))

        FlexMessage = json.load(open('./assets/_info5-proteinEat2.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '充足的【熱量】攝取':
        FlexMessage = json.load(open('./assets/_info7-kcal.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '水份控制(第五期)':
        FlexMessage = json.load(open('./assets/_info6-waterContral2.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '鹽分攝取(鈉攝取)':
        FlexMessage = json.load(open('./assets/_info9-salt.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '腹膜透析【鉀離子】攝取':
        FlexMessage = json.load(open('./assets/_info10-fomoKa.json', 'r', encoding='utf-8'))
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



