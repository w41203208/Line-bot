
from flask import Blueprint, jsonify, request, abort, make_response
import json
import os, re
import base64
from numpy import empty
import requests
from sqlalchemy import false
from .api import GETfoodDataAPI, GETmedicalAPI, GETsubMedicalAPI
from .db import SQLManger
from .util import plotHeatMap
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
LEVEL = 0
USER_AND_LEVEL_DICT = {}
USER_AND_MORE_DICT = {}
USER_AND_SEARCH = {}
LEVEL_DICT = {
    '第一、二期衛教指引':1,
    '第三期衛教指引':4,
    '第四期衛教指引':10,
    '第五期衛教指引':12,
    '血液透析':13,
    '腹膜透析':14,
}
COLOR_DICT = {
    '糖類':'E92137',
    '糕餅點心類':'E92137',
    '飲料類':'E92137',
    '澱粉類':'E92137',
    '調味料及香辛料類':'E92137',
    '加工調理食品類':'E92137',
    '肉類':'F0C92B',
    '豆類':'F0C92B',
    '蛋類':'F0C92B',
    '魚貝類':'F0C92B',
    '菇類':'32BB44',
    '藻類':'32BB44',
    '蔬菜類':'32BB44',
    '水果類':'C57CC6',
    '穀物類':'F0A61C',
    '油脂類':'835A0E',
    '堅果及種子類':'835A0E',
    '乳品':'64DEE6',
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
        if data['imageFile'] == '' or data['imageName'] == '':
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
    # https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id=1657008810&redirect_uri=https://b20c-2001-b011-400b-fe62-469-9903-a1c3-8683.ngrok.io/login&state=12345abcde&scope=profile%20openid&nonce=09876xyz
    state = request.args.get('state')
    code = request.args.get('code')
    request_body = {
        'grant_type':'authorization_code',
        'code': code,
        'redirect_uri': 'https://b20c-2001-b011-400b-fe62-469-9903-a1c3-8683.ngrok.io/login',
        'client_id':'1657008810',
        'client_secret':'025ee20c1b2e2d476680d22396d9ceb7',
    }
    x = requests.post('https://api.line.me/oauth2/v2.1/token', data=request_body)
    print(x.content)
    resp = make_response(jsonify({
        'code': code,
        'state': state,
    }),200)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@handler.add(MessageEvent, message=TextMessage)
def handle_message_heatmap(event):
    get_message = event.message.text
    id = event.source.user_id
    pattern = r'^(近3個月熱搜)|(近1個月熱搜)|(近1週熱搜)|(我的搜尋紀錄)|(我的搜尋紀錄)|(飲食查詢)|(最近熱搜紀錄)$'
    if not re.match(pattern, get_message): return

    if get_message == '我的搜尋紀錄':
        USER_AND_SEARCH[id] = False
    else:
        USER_AND_SEARCH[id] = True

    traceBackDate = None
    if get_message == '近3個月熱搜':
        traceBackDate = '90'
    elif get_message == '近1個月熱搜':
        traceBackDate = '30'
    elif get_message == '近1周熱搜':
        traceBackDate = '7'

    _params = {}
    if traceBackDate: _params["traceBackDate"] = traceBackDate
    if USER_AND_SEARCH[id]: _params["lineId"] = id
    heatmapProps = requests.get('https://kcs-backend.secplavory.page/getHeatmapProps', params=_params).json()['data']

    food_word_dict = {}
    for index, item in enumerate(heatmapProps):
        food_word_dict[index] = {
            'name': item['foodName'],
            'tag': item['foodTag'],
            'times': item['times'],
        }

    n = len(food_word_dict)
    for i in range(n):
        for j in range(0, n-i-1):
            if food_word_dict[j]['times'] > food_word_dict[j + 1]['times']:
                food_word_dict[j], food_word_dict[j+1] = food_word_dict[j+1], food_word_dict[j]

    name_arr = []
    times_arr = []
    colors_arr = []
    tag_color_arr = []
    temp_tag_dict = []
    for items in list(food_word_dict.values()):
        color = COLOR_DICT[items['tag']] if items['tag'] in COLOR_DICT else '000000'

        if len(temp_tag_dict) == 0 or items['tag'] not in temp_tag_dict:
            temp_tag_dict.append(items['tag'])
            tag_color_arr.append({
                'tag': items['tag'],
                'color': color
            })
        colors_arr.append(color)
        name_arr.append(items['name'])
        times_arr.append(items['times'])

    plotHeatMap(times_arr, name_arr, colors_arr, tag_color_arr, filePath_word)
    quick_reply = QuickReply(
        items=[
            QuickReplyButton(action=MessageAction(label='近3個月熱搜', text='近3個月熱搜')),
            QuickReplyButton(action=MessageAction(label='近1個月熱搜', text='近1個月熱搜')),
            QuickReplyButton(action=MessageAction(label='近1週熱搜', text='近1週熱搜')),
        ]
    )
    imageMessage = ImageSendMessage(original_content_url='https://kcs-linebot.secplavory.page/word_images/plot.png',preview_image_url='https://kcs-linebot.secplavory.page/word_images/plot.png', quick_reply=quick_reply)
    line_bot_api.reply_message(event.reply_token, imageMessage)
    return

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    db = SQLManger()
    db.connect()
    global LEVEL
    get_message = event.message.text
    id = event.source.user_id

    #####回傳關鍵字查詢#####
    queryFoodKeyword = db.query(
        f"SELECT a.*, JSON_ARRAYAGG(ac.content) as contentlist \
        FROM autoreply as a LEFT JOIN autoreplycontent as ac ON a.id = ac.keyid \
        WHERE a.keyword = '{get_message}'"
    )

    if queryFoodKeyword[0]['id']:
        print(queryFoodKeyword)
        for item in queryFoodKeyword:
            imageMessage = ImageSendMessage(original_content_url=f'{item["imgsrc"]}',preview_image_url=f'{item["imgsrc"]}')
            line_bot_api.reply_message(event.reply_token, imageMessage)
            for text in eval(item['contentlist']):
                TextMessage = TextSendMessage(text)
                line_bot_api.push_message(id, TextMessage, timeout=3)

    if get_message == '衛教資訊':
        FlexMessage = json.load(open('./backend/assets/medical.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
        return

    #####找食物#####
    query_text = get_message
    queryFood = db.query(f"SELECT f.* FROM food as f  WHERE foodName LIKE '%{query_text}%'")
    querySuggestion = db.query('SELECT * FROM foodsuggestion')
    if len(queryFood) != 0:
        sum = len(queryFood)
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
        request_body = {
            'lineId': id,
            'foodName': query_text,
        }
        print(request_body)
        requests.post('https://kcs-backend.secplavory.page/updateSearchtime', json=request_body)
        if (sum - 5 * (USER_AND_MORE_DICT[id]['times'] - 1)) <= 0:
            reply = TextSendMessage(text=f"{query_text}沒有更多了")
            line_bot_api.reply_message(event.reply_token, reply)
            return
        else:
            start = (USER_AND_MORE_DICT[id]['times']-1)*5
            end = start+5
            if (sum - 5 * (USER_AND_MORE_DICT[id]['times'] - 1)) < 5:
                end = start + sum - 5*(USER_AND_MORE_DICT[id]['times']-1)
            FlexMessage = GETfoodDataAPI().excute(queryFood[start:end], querySuggestion)
            quick_reply = QuickReply(items=[QuickReplyButton(action=MessageAction(label=f"查詢更多：{query_text}", text=query_text))])
            line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage, quick_reply=quick_reply))
            return

    #####找衛教資訊#####
    queryMedical = db.query(f"SELECT h.title, h.brief_desc, h.notification, JSON_ARRAYAGG(JSON_OBJECT('id', hh.healthinfolistid, 'sorted', hh.sorted, 'title', (select title from healthinfo where id = hh.healthinfolistid))) as infolist FROM healthinfo as h JOIN healthinfo__healthinfo as hh ON hh.healthinfoid = h.id WHERE h.title='{get_message}'")
    queryMedicalTitle = queryMedical[0]['title']

    if queryMedicalTitle:
        USER_AND_LEVEL_DICT[id] = LEVEL_DICT[queryMedicalTitle]
        FlexMessage = GETmedicalAPI().excute(queryMedical)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
        return

    if id in USER_AND_LEVEL_DICT:
        LEVEL = USER_AND_LEVEL_DICT[id]
    #####找子查詢#####
    querySubMedical = db.query(f"SELECT one.title, one.full_desc, one.imgsrc, JSON_ARRAYAGG(JSON_OBJECT('title', two.checklist)) as checklist FROM (SELECT healthinfo.title, healthinfo.imgsrc, healthinfo.full_desc, healthinfo__healthinfo.healthinfoid FROM healthinfo JOIN healthinfo__healthinfo ON healthinfo__healthinfo.healthinfolistid = healthinfo.id WHERE healthinfo.title='{get_message}' and healthinfo__healthinfo.healthinfoid = {LEVEL}) as one, (SELECT hh.healthinfoid, h.title as checklist FROM healthinfo__healthinfo as hh LEFT JOIN healthinfo as h on h.Id = hh.healthinfolistid WHERE healthinfoid = (SELECT healthinfo__healthinfo.healthinfoid FROM healthinfo JOIN healthinfo__healthinfo ON (healthinfo__healthinfo.healthinfolistid = healthinfo.id)WHERE healthinfo.title = '{get_message}' and healthinfo__healthinfo.healthinfoid = {LEVEL})) as two")
    querySubMedicalTitle = querySubMedical[0]['title']

    if querySubMedicalTitle:
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
    return
