
from flask import Blueprint, jsonify, request, abort, make_response
import json
import os
import base64

from sqlalchemy import null
from .api import GETfoodDataAPI, GETmedicalAPI, GETsubMedicalAPI
from .db import SQLManger
from .util import test
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage,QuickReply,QuickReplyButton,MessageAction,ImageSendMessage

views = Blueprint('views', __name__)

CHANNEL_ACCESS_TOKEN = "F5OQYnRnsuiAf51vzmRiswuQ/VAI06Ag5AVrDookZoapt+GEkfJFvbKJYBp08IrGPPJjqRHwu7HIJbfQs58T2zbPfh9zCQbnOsE2NWNYSgOBGlpcwFPQ7PDiOrpVNmZg6bTJ4zmeh4E6r1P86w6BugdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "1497d9253b7fc842f5ba2a22c15b9ce7"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

dirname = os.path.dirname(__file__)
filePath = os.path.join(dirname, 'assets/images')
filePath_word = os.path.join(dirname, 'assets/word_images')
Level = 0

USER_AND_LEVEL_DICT = {}
USER_AND_MORE_DICT = {}

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

@views.route("/upload_file", methods=["POST"])
def uploadFile():
    if request.method != 'POST':
        resp = make_response(jsonify({
            'msg': 'Bad request!'
        }),400)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp


    if request.method == 'POST':
        data = json.loads(request.data)
        if data['imageFile'] is None or data['imageName'] is None:
            resp = make_response(jsonify({
                'msg': 'File is not exist! or Name is not exist!'
            }),404)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            imageBase64, imageName = data['imageFile'].split(',')[1], data['imageName']
            for name in os.listdir(filePath):
                if imageName == name.split('.')[0]:
                    resp = make_response(jsonify({
                        'msg': 'FileName is exsit!'
                    }),402)
                    resp.headers['Access-Control-Allow-Origin'] = '*'
                    return resp
            imgdata = base64.b64decode(imageBase64)
            filename = f"{imageName}.jpg"
            with open(f"{filePath}/{filename}", "wb") as f:
                f.write(imgdata)

            url = f'https://kcs-linebot.secplavory.page/images/{filename}'

            resp = make_response(jsonify({
                'msg': 'File is uploaded!',
                'url': url,
            }),200)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp


@views.route("/login", methods=["GET"])
def login():
    resp = make_response(jsonify({
        'msg': 'File is uploaded!',
    }),200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

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




    #####回傳hot word#####
    if get_message == '飲食查詢':
        query_result = db.query(f"SELECT foodName, searchtime FROM food Order by searchtime desc limit 10;")
        food_word_dict = {}
        for index, item in enumerate(query_result):
            food_word_dict[index] = {
                'name':item['foodName'],
                'times': item['searchtime'],
            }
        n = len(food_word_dict)
        for i in range(n):
            for j in range(0, n-i-1):
                if (food_word_dict[j]['times']> food_word_dict[j+1]['times']):
                    food_word_dict[j], food_word_dict[j+1] = food_word_dict[j+1], food_word_dict[j]
        print(food_word_dict)
        name_arr = []
        times_arr = []
        for items in food_word_dict.values():
            name_arr.append(items['name'])
            times_arr.append(items['times'])
        test(times_arr, name_arr, filePath_word)
        # imageMessage = ImageSendMessage(original_content_url='https://kcs-linebot.secplavory.page/word_images/plot.png',preview_image_url='https://kcs-linebot.secplavory.page/word_images/plot.png')

        # line_bot_api.reply_message(event.reply_token, imageMessage)
        return
    if get_message == '衛教資訊':
        FlexMessage = json.load(open('./backend/assets/medical.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
        return

    #####找食物#####
    query_text = get_message
    queryFood = db.query(f"SELECT f.* FROM food as f  WHERE foodName LIKE '%{query_text}%'")
    querySuggestion = db.query('SELECT * FROM foodsuggestion')


    if queryFood:
        sum = len(queryFood)
        db.update(f"update food set searchtime = searchtime + 1 where foodName LIKE '%{query_text}%'")
        if id not in USER_AND_MORE_DICT.keys():
            #都沒有查過的user init 第一次
            USER_AND_MORE_DICT[id] = {
                'name': query_text,
                'times': 1,
            }
        else:
            if USER_AND_MORE_DICT[id]['name'] != query_text:
                USER_AND_MORE_DICT[id] = {
                    'name': query_text,
                    'times': 1,
                }
            else:
                USER_AND_MORE_DICT[id] = {
                    'name': query_text,
                    'times': USER_AND_MORE_DICT[id]['times'] + 1,
                }
        print(USER_AND_MORE_DICT)
        if ((sum - 5*(USER_AND_MORE_DICT[id]['times']-1)) <= 0):
            reply = TextSendMessage(text=f"{query_text}沒有更多了")
            line_bot_api.reply_message(event.reply_token, reply)
            return
        else:
            start = (USER_AND_MORE_DICT[id]['times']-1)*5
            end = start+5
            if ((sum - 5*(USER_AND_MORE_DICT[id]['times']-1)) < 5):
                end = start + sum - 5*(USER_AND_MORE_DICT[id]['times']-1)

            FlexMessage = GETfoodDataAPI().excute(queryFood[start:end], querySuggestion)
            quick_reply = QuickReply(items=[QuickReplyButton(action=MessageAction(label=f"查詢更多：{query_text}", text=query_text))])
            line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage, quick_reply=quick_reply))
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


