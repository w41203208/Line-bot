from asyncio.windows_events import NULL
from flask import Blueprint, jsonify, request, abort, make_response
import json

from sqlalchemy import null
from .api import GETfoodDataAPI, GETmedicalAPI, GETsubMedicalAPI
from .db import SQLManger
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage,QuickReply,QuickReplyButton,MessageAction

views = Blueprint('views', __name__)

CHANNEL_ACCESS_TOKEN = "F5OQYnRnsuiAf51vzmRiswuQ/VAI06Ag5AVrDookZoapt+GEkfJFvbKJYBp08IrGPPJjqRHwu7HIJbfQs58T2zbPfh9zCQbnOsE2NWNYSgOBGlpcwFPQ7PDiOrpVNmZg6bTJ4zmeh4E6r1P86w6BugdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "1497d9253b7fc842f5ba2a22c15b9ce7"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

Level = 0

USER_AND_LEVEL_DICT = {}

LEVEL_DICT = {
    '第一、二期衛教指引':1,
    '第三期衛教指引':4,
    '第四期衛教指引':10,
    '第五期衛教指引':12,
    '血液透析':13,
    '腹膜透析':14,
}


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
    db = SQLManger()
    db.connect()
    get_message = event.message.text
    id = event.source.user_id

    #richMenu action
    # if get_message == '個人資訊':
    #     res = GETrichMenuURIAPI(event.source.user_id, get_message).excute()
    #     line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', res))
    # elif get_message == '血壓記錄':
    #     res = GETrichMenuURIAPI(event.source.user_id, get_message).excute()
    #     line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', res))
    # elif get_message == '血糖記錄':
    #     res = GETrichMenuURIAPI(event.source.user_id, get_message).excute()
    #     line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', res))
    # elif get_message == '飲食記錄':
    #     res = GETrichMenuURIAPI(event.source.user_id, get_message).excute()
    #     line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', res))

    if get_message == '飲食查詢':
        return
    if get_message == '衛教資訊':
        FlexMessage = json.load(open('./assets/medical.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
        return

    #####找食物#####
    query_text = get_message
    queryFood = db.query(f"SELECT f.*, p.proteinDesc FROM food as f LEFT JOIN protein as p ON p.proteinId = f.foodProteinId WHERE foodName LIKE '%{query_text}%' LIMIT 5")
    querySuggestion = db.query('SELECT * FROM foodsuggestion')


    if queryFood:
        FlexMessage = GETfoodDataAPI().excute(queryFood, querySuggestion)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
        return


    #####找衛教資訊#####
    queryMedical = db.query(f"SELECT h.title, h.brief_desc, h.notification, JSON_ARRAYAGG(JSON_OBJECT('id', hh.healthinfolistid, 'sorted', hh.sorted, 'title', (select title from healthinfo where id = hh.healthinfolistid))) as infolist FROM healthinfo as h JOIN healthinfo__healthinfo as hh ON hh.healthinfoid = h.id WHERE h.title='{get_message}'")


    if queryMedical[0]['title']:
        if id not in USER_AND_LEVEL_DICT.keys():
            USER_AND_LEVEL_DICT[id] = LEVEL_DICT[queryMedical[0]['title']]
        else:
            USER_AND_LEVEL_DICT[id] = LEVEL_DICT[queryMedical[0]['title']]

        print(USER_AND_LEVEL_DICT)
        FlexMessage = GETmedicalAPI().excute(queryMedical)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
        return





    level = USER_AND_LEVEL_DICT[id]
    #####找子查詢#####
    querySubMedical = db.query(f"SELECT one.title, one.full_desc, one.imgsrc, JSON_ARRAYAGG(JSON_OBJECT('title', two.checklist)) as checklist FROM (SELECT healthinfo.title, healthinfo.imgsrc, healthinfo.full_desc, healthinfo__healthinfo.healthinfoid FROM healthinfo JOIN healthinfo__healthinfo ON healthinfo__healthinfo.healthinfolistid = healthinfo.id WHERE healthinfo.title='{get_message}' and healthinfo__healthinfo.healthinfoid = {level}) as one, (SELECT hh.healthinfoid, h.title as checklist FROM healthinfo__healthinfo as hh LEFT JOIN healthinfo as h on h.Id = hh.healthinfolistid WHERE healthinfoid = (SELECT healthinfo__healthinfo.healthinfoid FROM healthinfo JOIN healthinfo__healthinfo ON (healthinfo__healthinfo.healthinfolistid = healthinfo.id)WHERE healthinfo.title = '{get_message}' and healthinfo__healthinfo.healthinfoid = {level})) as two")


    if querySubMedical[0]['title']:
        FlexMessage, TextReplyMessage, QuickReplyMessage = GETsubMedicalAPI().excute(querySubMedical)

        new_items = []
        for index, quickItem in enumerate(eval(QuickReplyMessage)):
            new_items.append(QuickReplyButton(action=MessageAction(label=str(index+1)+"、"+quickItem['title'], text=quickItem['title'])))
        quick_reply = QuickReply(items=new_items)

        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
        TextMessage = TextSendMessage(TextReplyMessage, quick_reply=quick_reply)
        line_bot_api.push_message(id, TextMessage, timeout=3)
        return


    reply_msg = get_message
    reply = TextSendMessage(text=f"{reply_msg}不在資料庫內，請洽詢護理師!")
    line_bot_api.reply_message(event.reply_token, reply)


    db.close()


