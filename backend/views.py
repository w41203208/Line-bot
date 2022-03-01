from flask import Blueprint, jsonify, request, abort
import json
import os
import requests

from .models import Food
from .api import GETfoodDataAPI, GETrichMenuURIAPI
from . import db

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage,QuickReply,QuickReplyButton,MessageAction


views = Blueprint('views', __name__)

CHANNEL_ACCESS_TOKEN = "F5OQYnRnsuiAf51vzmRiswuQ/VAI06Ag5AVrDookZoapt+GEkfJFvbKJYBp08IrGPPJjqRHwu7HIJbfQs58T2zbPfh9zCQbnOsE2NWNYSgOBGlpcwFPQ7PDiOrpVNmZg6bTJ4zmeh4E6r1P86w6BugdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "1497d9253b7fc842f5ba2a22c15b9ce7"

# line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
# handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

Level = 0

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
    global Level
    get_message = event.message.text
    id = event.source.user_id

    #richMenu action
    if get_message == '個人資訊':
        res = GETrichMenuURIAPI(event.source.user_id, get_message).excute()
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', res))
    elif get_message == '血壓記錄':
        res = GETrichMenuURIAPI(event.source.user_id, get_message).excute()
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', res))
    elif get_message == '血糖記錄':
        res = GETrichMenuURIAPI(event.source.user_id, get_message).excute()
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', res))
    elif get_message == '飲食記錄':
        res = GETrichMenuURIAPI(event.source.user_id, get_message).excute()
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', res))
    if get_message == '衛教資訊':
        FlexMessage = json.load(open('./assets/medical.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))

    elif get_message == '第一、二期資訊':
        Level = 1
        FlexMessage = json.load(open('./assets/medical-indicate-one.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '第三期資訊':
        Level = 2
        FlexMessage = json.load(open('./assets/medical-indicate-three.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '第四期資訊':
        Level = 3
        FlexMessage = json.load(open('./assets/medical-indicate-four.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '第五期資訊':
        FlexMessage = json.load(open('./assets/medical-indicate-five.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '血液透析':
        Level = 4
        FlexMessage = json.load(open('./assets/blood.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
    elif get_message == '腹膜透析':
        Level = 5
        FlexMessage = json.load(open('./assets/fomo.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))

    elif get_message == '血壓血糖控制':
        FlexMessage = json.load(open('./assets/_info1-bsContral.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
        bsControlTextMessage = TextSendMessage(bsControlTextReply,quick_reply=quick_reply_level1)

        line_bot_api.push_message(id, bsControlTextMessage, timeout=3)

    elif get_message == '認識【蛋白質飲食】':
        FlexMessage = json.load(open('./assets/_info2-knowProtein.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))
        knowProteinTextMessage1 = TextSendMessage(knowProteinTextReply1)
        knowProteinTextMessage2 = TextSendMessage(knowProteinTextReply2,quick_reply=quick_reply_level1)

        line_bot_api.push_message(id, [knowProteinTextMessage1,knowProteinTextMessage2], timeout=3)

    elif get_message == '認識【鉀】含量高的食物':
        FlexMessage = json.load(open('./assets/_info3-knowKa.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))


        if Level == 2:
            knowKaTextMessage = TextSendMessage(knowKaTextReply,quick_reply=quick_reply_level2)
        elif Level == 3:
            knowKaTextMessage = TextSendMessage(knowKaTextReply,quick_reply=quick_reply_level3)
        elif Level == 4:
            knowKaTextMessage = TextSendMessage(knowKaTextReply,quick_reply=quick_reply_level4)
        elif Level == 5:
            knowKaTextMessage = TextSendMessage(knowKaTextReply,quick_reply=quick_reply_level5)


        line_bot_api.push_message(id, [knowKaTextMessage], timeout=3)

    elif get_message == '認識【磷】含量高的食物':
        FlexMessage = json.load(open('./assets/_info4-knowP.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))

        if Level == 2:
            knowPTextMessage = TextSendMessage(knowPTextReply,quick_reply=quick_reply_level2)
        elif Level == 3:
            knowPTextMessage = TextSendMessage(knowPTextReply,quick_reply=quick_reply_level3)
        elif Level == 4:
            knowPTextMessage = TextSendMessage(knowPTextReply,quick_reply=quick_reply_level4)
        elif Level == 5:
            knowPTextMessage = TextSendMessage(knowPTextReply,quick_reply=quick_reply_level5)

        line_bot_api.push_message(id, knowPTextMessage, timeout=3)

    elif get_message == '蛋白質飲食(第三期)':
        proteinEatFlexMessage = json.load(open('./assets/_info5-proteinEat.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', proteinEatFlexMessage))

        proteinEatTextMessage1 = TextSendMessage(proteinEat1TextReply1)
        proteinEatTextMessage2 = TextSendMessage(priteinEat3TextReply2, quick_reply=quick_reply_level2)

        line_bot_api.push_message(id, [proteinEatTextMessage1,proteinEatTextMessage2], timeout=3)

    elif get_message == '水份控制':
        FlexMessage = json.load(open('./assets/_info6-waterContral.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))

        if Level == 2:
            waterControlTextMessage = TextSendMessage(waterControlTextReply, quick_reply=quick_reply_level2)
        elif Level == 3:
            waterControlTextMessage = TextSendMessage(waterControlTextReply, quick_reply=quick_reply_level3)

        line_bot_api.push_message(id, waterControlTextMessage, timeout=3)

    elif get_message == '蛋白質飲食(第四期)':
        proteinEatFlexMessage = json.load(open('./assets/_info5-proteinEat.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', proteinEatFlexMessage))

        proteinEatTextMessage1 = TextSendMessage(proteinEat1TextReply1)
        proteinEatTextMessage2 = TextSendMessage(priteinEat4TextReply2)
        proteinEatTextMessage3 = TextSendMessage(priteinEat1TextReply3)
        proteinEatTextMessage4 = TextSendMessage(priteinEat1TextReply4, quick_reply=quick_reply_level3)

        line_bot_api.push_message(id, [proteinEatTextMessage1,proteinEatTextMessage2,proteinEatTextMessage3,proteinEatTextMessage4], timeout=3)

    elif get_message == '蛋白質飲食(第五期)':
        proteinEatFlexMessage = json.load(open('./assets/_info11-proteinEat2.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', proteinEatFlexMessage))

        if Level == 4:
            proteinEatTextMessage1 = TextSendMessage(proteinEat1TextReply1)
            proteinEatTextMessage2 = TextSendMessage(priteinEat5TextReply2)
            proteinEatTextMessage3 = TextSendMessage(priteinEat1TextReply3)
            proteinEatTextMessage4 = TextSendMessage(priteinEat1TextReply4, quick_reply=quick_reply_level4)
        elif Level == 5:
            proteinEatTextMessage1 = TextSendMessage(proteinEat1TextReply1)
            proteinEatTextMessage2 = TextSendMessage(priteinEat5TextReply2)
            proteinEatTextMessage3 = TextSendMessage(priteinEat1TextReply3)
            proteinEatTextMessage4 = TextSendMessage(priteinEat1TextReply4, quick_reply=quick_reply_level5)

        line_bot_api.push_message(id, [proteinEatTextMessage1,proteinEatTextMessage2,proteinEatTextMessage3,proteinEatTextMessage4], timeout=3)

    elif get_message == '充足的【熱量】攝取':
        FlexMessage = json.load(open('./assets/_info7-kcal.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))

        if Level == 4:
            kcalGetTextMessage = TextSendMessage(kcalGetTextReply, quick_reply_level4)
        elif Level == 5:
            kcalGetTextMessage = TextSendMessage(kcalGetTextReply, quick_reply_level5)

        line_bot_api.push_message(id, kcalGetTextMessage, timeout=3)

    elif get_message == '水份控制(第五期)':
        FlexMessage = json.load(open('./assets/_info8-waterContral2.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))

        if Level == 4:
            kcalGetTextMessage = TextSendMessage(waterControl5bloodTextReply, quick_reply_level4)
        elif Level == 5:
            kcalGetTextMessage = TextSendMessage(waterControl5fomoTextReply, quick_reply_level5)

        line_bot_api.push_message(id, kcalGetTextMessage, timeout=3)

    elif get_message == '鹽分攝取(鈉攝取)':
        FlexMessage = json.load(open('./assets/_info9-salt.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))

        if Level == 4:
            saltControlTextMessage = TextSendMessage(saltControlTextReply,quick_reply=quick_reply_level4)
        elif Level == 5:
            saltControlTextMessage = TextSendMessage(saltControlTextReply,quick_reply=quick_reply_level5)

        line_bot_api.push_message(id, saltControlTextMessage, timeout=3)

    elif get_message == '腹膜透析【鉀離子】攝取':
        FlexMessage = json.load(open('./assets/_info10-fomoKa.json', 'r', encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))

        fomokaTextMessage = TextSendMessage(fomokaTextReply,quick_reply=quick_reply_level5)

        line_bot_api.push_message(id, fomokaTextMessage, timeout=3)



    else: #只要資料庫找的到的都輸出foodData

        query_text = get_message
        outputData = Food.query.filter(Food.foodName.like('%'+ query_text + '%') if query_text is not None else '').all()[:5]
        res = GETfoodDataAPI(outputData).excute()


        if not outputData:
            reply_msg = get_message
            reply = TextSendMessage(text=f"{reply_msg}不在資料庫內，請洽詢護理師!")
            line_bot_api.reply_message(event.reply_token, reply)
        else:
            FlexMessage = res
            line_bot_api.reply_message(event.reply_token, FlexSendMessage('profile', FlexMessage))



bsControlTextReply = f"1.1 不要吃太鹹，血壓要正常\n(1)減少鹽與醬油的使用量。\n(2)少調味，如不加胡椒鹽、番茄醬、辣椒醬、豆瓣醬、沙茶醬。\n(3)少喝湯，盡量不要在外面用餐，都能減少吃進的鹽量。\n(4)少吃過鹹食物，如醃漬品、酸菜、泡菜、味噌、醬瓜、鹹蛋、肉燥、泡麵、鹽酥雞、泰式料理、洋芋片、海苔等。\n\n★以上少吃能控制好血壓，腎功能才不會快速惡化。有高血壓的人一定要依照醫師指示服用降血壓藥，不能自行調整藥物!!"

knowProteinTextReply1 = f"2.1 少吃低生物價蛋白質\n蛋白質有分好壞！優質的蛋白質為高生物價的蛋白質，非優質的蛋白質為低生物價的蛋白質。\n\n(1)質的蛋白質（高生物價的蛋白質），在體內利用率佳、產生尿毒素較少的蛋白質。例如：\n★ 蛋豆魚肉類：蛋、豬、雞、鴨、魚、牛、豆腐等(黃豆製成的食品)。\n★ 蛋白質攝取最好要選【蛋豆魚肉類】為主。\n\n(2)非優質的蛋白質（低生物價的蛋白質），會產生較多的尿毒素，會增加腎臟負擔，要避免吃。例如：\n★ 堅果類：腰果、松子、杏仁、花生、瓜子、芝麻等\n★ 豆 類：綠豆、紅豆、蓮子、薏仁、蠶豆、碗豆等。\n★ 麵筋製成的食品：麵筋、麵腸、麵輪、烤麩等，產生較多的尿毒素。上述都要避免吃!!"

knowProteinTextReply2 = f"3.1 糖尿病\n(1)有腎臟病，且有糖尿病的人，初期(1-2期)不用減少肉量，飲食以控制血糖為重，但還是要選擇優質的蛋白質為主\n運動：\n不運動容易造成血液中脂肪累積、血液循環速度變慢，使得血壓、血糖、血脂控制不良，讓腎臟健康愈來愈差。持續、規律的運動能讓病人健康整體改善，運動的好處包括：\（一）強化肌力及耐力。\n（二）血壓控制穩定。\n（三）改善體內血脂肪、膽固醇及三酸甘油脂過高現象。\n（四）促進血糖的平衡調控。\n（五）改善心理健康。\n（六）減少骨質疏鬆\n腎臟病患者建議每週至少運動五天，中等激烈程度之動( 如打球、 快走、 慢跑、騎自 行車、游泳舞蹈跑步機 、有氧運動登山等)，每天累積達30 分鐘以上，運動後心跳達到 130 下右，能夠增進心肺功的運動尤佳 。\n\n根據上述資料並歸納為庫的建檔， 並依照衛生福利部中央健康保險署 「全民健康保險末期腎臟病前（ Pre-ESRD）之病人照護與衛教計畫」 (2018)法規所定。\n\n服藥：\n您不能不知道！亂用藥物會加速疾病的惡化，像是電台取得的偏方，在不清楚來源的情況下都不能吃!\n不管任何藥品或中草藥皆需經由醫護人員認可後才能食用，遵循醫生正確指引之下規律服藥，建立良好的服藥習慣才能延緩腎臟功能惡化。"
knowKaTextReply = f"1.1鉀離子是什麼?\n一般常見的蔬菜水果都含有鉀，而鉀離子過高會心率不整、心跳停止，患者要注意才行。生的食物所含的鉀離子較多經過水煮後，食物所含的鉀離子大部份會流到湯汁裡，而愛「喝湯」就會容易導致高血鉀，是腎臟病患最常見的原因，要特別小心。\n\n1.2那該如何控制呢？\n(1)正常的鉀濃度範圍標準值3.5~5.1 mmol/L，患者須知道自己屬於哪個階段(屬於第幾期腎臟病)。\n\n(2)認識高鉀食物：(以下食物含鉀較高，慢性腎臟病患要避免食用)\n★果乾類：水果乾的鉀離子含量非常高要避吃。\n★水果類：蕃茄、奇異果、哈密瓜、香瓜、火龍果、櫻桃、草莓是鉀含量較多的水果要避免吃。純果汁、果菜汁也要避免喝。\n★中藥類：中藥材燉補品、雞湯、肉湯，這些都含有很高鉀離子，要避免吃。\n★勾芡類：勾芡食物，燴飯、燴麵、酸辣湯、咖哩飯、羹麵等與燉補品的湯汁要避免吃。\n★湯 類：菜汁、菜湯、肉汁拌飯，會導致高血鉀要避免吃。\n★其 他：咖啡雞精、人參精、運動飲料、巧克力、梅子汁、蕃茄醬等鉀含量叫高，要避免食用。\n\n(3)如何吃呢?\n★水燙蔬菜：吃蔬菜，要經由水燙過後，再以油炒或油拌即可(選用不飽和脂肪油，如芥油、大豆沙拉油、橄欖油、葵花油、玉米油等)。不食用菜湯、精力湯、生菜。\n★不 喝 湯 ： 不論菜湯或肉湯都含有高量的鉀。且勿食用濃縮湯及使用肉汁拌飯。\n★調 味 品 ： 不能用鈉鹽、薄鹽醬油、無鹽醬油，因為鉀離子含量較高。可以加少許辣椒、八角、胡椒增添味道。\n★低鉀水果：選擇低鉀水果食用，如鳳梨、蘋果、蓮霧、葡萄、水梨、軟柿子、檸檬。吃太多水也會使得血鉀上升。水果攝取需要營養師建議，每天大約吃2至3 個棒球大小的水果營養就夠。\n★中 草 藥 ：鉀磷離子都較高，須由中醫師或西醫師開的處方籤才能吃，如從電台取得，在清楚來源的情況下都不能吃。"
knowPTextReply = f"1、磷離子是什麼？\n幾乎所有的食物包括加工食品或天然食物都含有磷，只是量多量少的差別而已。而當慢性腎臟病患者因腎功能下降，無排除飲食中攝取到的磷時，血磷濃度就會上升，過多會導致，眼睛會糊糊的、皮膚搔癢、骨質病變、副甲狀腺機能亢進。因此每日好好控制磷攝取量相當重要，才能避免高血磷對健康造成的害。\n\n2、那該如何控制呢？\n(1)正常的血磷濃度範圍標準值是3.5~5 mg/dL，患者知道自己屬於第幾期腎臟病。\n\n(2)認識高磷食物：(以下食物含磷較高，慢性腎臟病患者要避免食用\n★全 穀 類：全麥麵包、糙米、穀片、麥片、蓮子、薏仁、小麥胚芽。\n★堅 果 類：花生、栗子、杏仁果、開心果、核桃、腰果、瓜子。堅果類由營養師確認抽血報告確認磷指數後才可吃，不然一律不能吃。\n★乳 製 品：牛奶、奶粉、羊奶、優格、乳酪、優酪乳、發酵乳、養樂 多等乳酸飲料等。\n★動物內臟：豬肝、豬心、雞胗等。\n★加工肉品：豬肉鬆、火腿片、豬乾、肉燥、貢丸類、餃類、香腸、火腿、燻肉、臘肉。\n★豆 類：綠豆、紅豆、蓮子、薏仁、蠶豆、碗豆等，磷含量高。\n★飲 品 類：如咖啡、拿鐵、可樂、汽水、可可、碳酸飲料。\n★湯食品：燉補品、羊肉爐、薑母鴨、麻油雞、牛肉麵、燴麵、燴飯、肉羹麵、魷魚羮麵、酸辣湯、燴飯、咖哩飯、即食調理包\n\n(3)該如何吃呢?\n★磷每日攝取量為800~1200毫克/天。\n★奶與奶製品的磷含量很高，且使用鈣片類的磷結合劑並不能有效降低奶類磷的吸收，所以慢性腎臟病患者要避免奶類與奶製品的攝取。\n★肉類食材水煮 30 分鐘，磷含量幾乎都轉移到湯汁中可將磷含量降低20~55%。因此不要喝肉湯，避免這些從食材溶出的磷又吃進肚內。\n★病情較嚴重的病患，即使降低高磷食物的攝取也無法維持血磷正常，因此需根據醫師建議，在用餐中要磷結合劑以降低磷的吸收才能降低血磷。\n"
proteinEat1TextReply1 = f"3.1 不要吃太鹹，血壓要正常\n(1)減少鹽與醬油的使用量。\n(2)少調味，如不加胡椒鹽、番茄醬、辣椒醬、豆瓣醬、沙茶醬。\(3)少喝湯，盡量不要在外面用餐，都能減少吃進的鹽量。\n(4)少吃過鹹食物，如醃漬品、酸菜、泡菜、味噌、醬瓜、鹹蛋、肉燥、泡麵、鹽酥雞、泰式料理、洋芋片、海苔等。\n\n★以上吃能控制好血壓，腎功能才不會快速惡化。有高血壓的人一定要依照醫師指示服用降血壓藥，不能自行調整藥物!!"
priteinEat3TextReply2 = f"3.2限蛋白質飲食\n蛋白質攝取過多導致腎絲球內高血壓，對腎臟造成負擔，因此維持良好營養狀態下適量減少蛋白質攝取相當重要能有助於延緩腎功能惡化。\n\n3.2.1 那如何選擇蛋白質攝取呢?\n(1)少吃【非優質的蛋白質】（低生物價的蛋白質），會產生較多的尿毒素，會增加腎臟負擔，要避免吃。例如：\n★主類 ：像一般常吃到的主食，如米飯、麵條、燕麥、玉米、饅頭、 包子、水餃，蓮藕、芋頭、馬鈴薯、南瓜等澱粉，這類為【非優質的蛋白質】，對腎臟負擔較大，每天要限量食用。而慢性臟病患最好以白米飯為主食，雖然白米飯也是非優質蛋白質，但白米飯對腎臟負擔比較小，比起麵條、包子饅頭、麵包等麵粉等食品對腎臟的負擔會比較大。\n★ 堅果類：腰果、松子、杏仁花生、瓜子、芝麻等，要避免吃。\n★ 豆 類：綠豆、紅豆、蓮子、薏仁、蠶豆、碗豆等，要避免吃。\n★ 麵筋製成的食品：麵筋、麵腸、麵輪、烤麩等，產生較多的尿毒素。都要避免!!\n\n(2)選擇【優質蛋白質】（高生物價的蛋白質）食用，優質蛋白質在體內利用率佳、產生尿毒素較少的蛋白質。例如：\n★ 蛋豆魚肉類：蛋、豬、雞、鴨、魚、牛等(黃豆製成的食品)\n★ 黃豆製成的食品：豆腐、豆乾、豆包等。\n★ 蛋白質攝取最好要選擇【蛋豆魚肉類】為主，至少要有50%-75%。\n\n3.2.2 每日所需攝取多少份量的蛋白質？\n★第3期腎臟病，蛋白質天每公斤攝取量為0.8-1.0 g/kg/day。\n舉例：如以一個體重60公斤的人，腎臟病第三期患者蛋白質需限制0.8 (g/kg)，則他每天需要的蛋白質為60x0.8= 48(g)，份量至少50%~75%的優蛋白質，所以一天三餐最多吃5份蛋白質(蛋豆魚肉類)+2碗白飯(主食)。份量參考如上表。\n\n3.2.3 如何判斷一份蛋白質有多少分量?\n1份的蛋白質\n=1份/雞豬牛羊肉 ( 約3支手指頭小，如上圖參考)\n=1份/半個手掌心大小的魚肉\n=1顆/雞蛋\n=2片/豆干\n=1碗/飯\n=1杯260ml/豆漿"
priteinEat4TextReply2 = f"3.2限蛋白質飲食\n蛋白質攝取過多導致腎絲球內高血壓，對腎臟造成負擔，因此維持良好營養狀態下適量減少蛋白質攝取相當重要能有助於延緩腎功能惡化。\n\n3.2.1 那如何選擇蛋白質攝取呢?\n(1)少吃【非優質的蛋白質】（低生物價的蛋白質），會產生較多的尿毒素，會增加腎臟負擔，要避免吃。例如：\n★主類 ：像一般常吃到的主食，如米飯、麵條、燕麥、玉米、饅頭、 包子、水餃，蓮藕、芋頭、馬鈴薯、南瓜等澱粉，這類為【非優質的蛋白質】，對腎臟負擔較大，每天要限量食用。而慢性臟病患最好以白米飯為主食，雖然白米飯也是非優質蛋白質，但白米飯對腎臟負擔比較小，比起麵條、包子饅頭、麵包等麵粉等食品對腎臟的負擔會比較大。\n★ 堅果類：腰果、松子、杏仁花生、瓜子、芝麻等，要避免吃。\n★ 豆 類：綠豆、紅豆、蓮子、薏仁、蠶豆、碗豆等，要避免吃。\n★ 麵筋製成的食品：麵筋、麵腸、麵輪、烤麩等，產生較多的尿毒素。都要避免!!\n\n(2)選擇【優質蛋白質】（高生物價的蛋白質）食用，優質蛋白質在體內利用率佳、產生尿毒素較少的蛋白質。例如：\n★ 蛋豆魚肉類：蛋、豬、雞、鴨、魚、牛等(黃豆製成的食品)\n★ 黃豆製成的食品：豆腐、豆乾、豆包等。\n★ 蛋白質攝取最好要選擇【蛋豆魚肉類】為主，至少要有50%-75%。\n\n3.2.2 每日所需攝取多少份量的蛋白質？\n★第4期腎臟病，且沒有糖尿病，蛋白質攝取量為0.6g/kg/day。\n\n例如，以一個體重65公斤的人，腎臟病第四期患者蛋白質需限制0.6 (g/kg)，則他每天需要的蛋白質為65x0.6= 39(g)，份量(至少50%~75%的優質蛋白質)，所以一天三餐最多吃4份蛋白質(蛋豆魚肉類)+2碗白飯(主食)。份量參考如上表。\n\n★第4期腎臟病，且有糖尿病，蛋白質攝取量為0.8g/kg/day。如果血糖平穩正常、營養狀態良好在營養師的指導下，可以降至0.6 克。\n\n3.2.3 如何判斷一份蛋白質有多少分量?\n1份的蛋白質\n=1份/雞豬牛羊肉 ( 約3支手指頭小，如上圖參考)\n=1份/半個手掌心大小的魚肉\n=1顆/雞蛋\n=2片/豆干\n=1碗/飯\n=1杯260ml/豆漿"
priteinEat5TextReply2 = f"2.2限蛋白質飲食\n蛋白質攝取過多導致腎絲球內高血壓，對腎臟造成負擔，因此維持良好營養狀態下適量減少蛋白質攝取相當重要能有助於延緩腎功能惡化。\n\n2.2.1 那如何選擇蛋白質攝取呢?\n(1)少吃【非優質的蛋白質】（低生物價的蛋白質），會產生較多的尿毒素，會增加腎臟負擔，要避免吃。例如：\n★主類 ：像一般常吃到的主食，如米飯、麵條、燕麥、玉米、饅頭、 包子、水餃，蓮藕、芋頭、馬鈴薯、南瓜等澱粉，這類為【非優質的蛋白質】，對腎臟負擔較大，每天要限量食用。而慢性臟病患最好以白米飯為主食，雖然白米飯也是非優質蛋白質，但白米飯對腎臟負擔比較小，比起麵條、包子饅頭、麵包等麵粉等食品對腎臟的負擔會比較大。\n★ 堅果類：腰果、松子、杏仁花生、瓜子、芝麻等，要避免吃。\n★ 豆 類：綠豆、紅豆、蓮子、薏仁、蠶豆、碗豆等，要避免吃。\n★ 麵筋製成的食品：麵筋、麵腸、麵輪、烤麩等，產生較多的尿毒素。都要避免!!\n\n(2)選擇【優質蛋白質】（高生物價的蛋白質）食用，優質蛋白質在體內利用率佳、產生尿毒素較少的蛋白質。例如：\n★ 蛋豆魚肉類：蛋、豬、雞、鴨、魚、牛等(黃豆製成的食品)\n★ 黃豆製成的食品：豆腐、豆乾、豆包等。\n★ 蛋白質攝取最好要選擇【蛋豆魚肉類】為主，至少要有50%-75%。\n\n2.2.2 每日所需攝取多少份量的蛋白質？\n★血液透析患者，蛋白質攝取量每日以每公斤體重 1~1.2 公克為原則，請先諮詢營養師後食用。\n★血液透析患者，蛋白質攝取量每日以每公斤體重 1~1.2 公克為原則，請先諮詢營養師後食用。\n★富含蛋白質的食物一般都含『磷』較高，所以必須配合醫師指示服用磷的結合劑（如鈣片、胃乳片）一起服用。\n\n2.2.3 如何判斷一份蛋白質有多少分量?\n1份的蛋白質\n=1份/雞豬牛羊肉 ( 約3支手指頭小，如上圖參考)\n=1份/半個手掌心大小的魚肉\n=1顆/雞蛋\n=2片/豆干\n=1碗/飯\n=1杯260ml/豆漿"
priteinEat1TextReply3 = f"3.3用低蛋白澱粉和營養品補充足夠熱量\n減少蛋白質攝取的時候會比較沒有飽足感、容易餓，容易導致熱量攝取不足，會導致營養良問題。因此吃足夠熱量對慢性腎臟病患非常重要。那熱量攝取不足又要限制蛋白質要怎麼吃呢?\n\n3.3.1 可以利用低氮澱粉補充：(每天需補充1-2 碗才足夠)\n(1)低蛋白澱粉的優點：提供熱量富含熱量、蛋白質含量很少的食物，不會產生尿毒素或產生的尿毒素很低。例如：地瓜(水煮) 、米粉、冬粉、粄條、太白粉、番薯粉、藕粉、 澄粉、粉圓、西谷米等食物。如果想飯(因為一般的米蛋白質含量較高一碗8克)，如經濟允許也建議可吃低蛋白的米食(一碗最多2克)，可以有飽足感又較低蛋白質。\n\n(2)補充低蛋白澱粉時，可以加砂糖、果糖、冰糖、蜂蜜糖果等，以增加熱量。但有糖尿病共病者，使用純醣類須諮詢相關醫護人員。\n\n3.3.2 營養品補充\n(1)營 養 品 ：主要成分是經過處理的醣類與油脂，對血糖與血脂的影響小，有些還添加腎臟病患需要的維生素與礦物質及纖維素。最好在與營養師討論後，選擇適合自己的營養品來補充。\n\n(2)市面常見營養品介紹：\n★腎 補 鈉 ：一罐為400-500卡是一個排骨便當量主要是給後期吃部下飯或不想吃飯的人，或年輕人比較沒時間吃飯也可以喝一罐，也可以加冰塊當奶茶喝。\n★補 體 素 ：可以用來當三餐之間的點心補充熱量。\n★補維勝錠：專給腎臟病者吃的維他命，為沒有磷、鉀、維生素A。\n\n(3)注意!! 腎臟病不能吃的營養品：\n★善 存 ：為一般常見的維生素，善存的鉀、磷、維生素A含量較高，不符合腎臟病患者需求。"
priteinEat1TextReply4 = f"3.4 攝取足夠維生素及適量礦物質\n(1)某些蔬菜類屬於低生物價蛋白質含量高( 身體利用性較差的蛋白質的食物) ，需適量限制如：\n★菇 類：香菇、鮑魚菇、金針菇等)。\n★芽菜類：黃豆芽。\n★豆莢類：菜豆、四季豆、豌豆莢等)。\n\n(2)該如何吃呢?\n★蔬菜份數以3 份( 不超過4 份) 為限，水果份數以2 份(不超過3份) 為限，可獲得適量之維生素及礦物質。\n★油脂類食物要使用足夠的油烹調才能提供足夠的熱量，可選擇市面上之植物油或調和油。\n★奶類或五穀奶有較高量之磷，不建議腎臟後期病患食用，且奶類的磷無法以鈣片類的磷結合劑降低吸收，會導致高血磷。"
waterControlTextReply = f"★慢性腎臟病患者若有嚴重水腫問題，請依據醫師指示限制水份攝取， 以不發生水腫為原則。"
kcalGetTextReply = f"當熱量攝取不足時，身體組織的蛋白質會分解作為熱量來源，不僅增加含氮廢物產生，更加重腎臟負擔。因此，熱量攝取建議為每天每公30~35 大卡（例如：體重 60 公斤，所需熱量為1,800~2,100 大卡），或請依營養師指示。"
waterControl5bloodTextReply =f"血液透析病人當體內水分過多時，因腎臟無法排水，會出現呼吸急促、血壓升高、身體浮腫、肺部積水、心臟負荷增加甚至造成心衰竭⋯等等，因此水分控制很重要，水份包括水果、湯汁、飲料、開水等。\n\n★每日的飲水攝取量，必須根據個人每日的尿量、排汗量、運動量和季節性的不 同做來調整。\n★每日應定時、點、同磅秤量體重，且兩次透析之間的體重以不超過體重增加 5% （如：60 公斤乾體重的人，60×4.5% ＝ 2.7，則體重增加儘量不超 過 2.7 公斤）。\n★避免過量水份攝取與口渴小秘訣：平均分配一日需飲用水分，口渴時，可含小冰塊減少水份攝取量。 保持口腔及嘴唇濕潤，可含無糖的硬糖果、嚼無糖口香糖、檸檬片沾口 或擦護唇膏。 選擇食物以乾性、固體為主，減少取湯湯水水的食物。"
waterControl5fomoTextReply =f"★每日可攝取水量約限制500～800cc，儘可能不使自己有水腫或血壓高之情形發生。"
saltControlTextReply = f"鹽攝取過多，會造成水分積留，使體重增加，引起心臟負荷增加。\n\n★ 血液透析病人建議鹽的攝取量建議每天介於3-5克/天（約 1茶匙）。\n★不可完全不吃鹽，否則會引起低血鈉症。鹽份太多，則會有口渴的感覺；容易產生高血壓、水腫或心臟 衰竭等症狀。\n★儘量選用鈉質低的新鮮天然植物，少食用醃製、滷製、製及各類鈉離子量高 的加鹽食物（例如：火腿、香腸、筍乾、泡菜、味增、豆瓣醬、罐頭、肉醬、 蜜餞、肉鬆、咖哩、臘肉、番茄醬），禁用市售低鈉鹽、薄鹽、代鹽，可以食 用一般鹽或有特別指定透析患者使用的低鈉鹽。\n★平常重視吃、口味重者，可試著使用味道較強烈之調味料來替代如：少量的 酒、白醋、辣椒、肉桂、檸檬汁、蔥、薑、蒜），增加食物的可口性。"
fomokaTextReply = f"5.1 鉀離子是什麼?\n一般常見的蔬菜水果都含有鉀，而鉀離子過高會心率不整、心跳停止，患者要注意才行。生的食物所含的鉀離子較多經過水煮後，食物所含的鉀離子大部份會流到湯汁裡，而愛「喝湯」就會容易導致高血鉀，是腎臟病患最常見的原因，要特別小心。\n\n5.2 那該如何控制呢？\n(1)正常的鉀濃度範圍標準是3.5~5.1 mmol/L，患者須知道自己屬於哪個階段(屬於第幾期腎臟病)。\n(2)認識高鉀食物：(以下食物含鉀較高，慢性腎臟病患要避免食用)\n★果乾類：水果乾的鉀離子含量非常高要避吃。\n★水果類：蕃茄、奇異果、哈密瓜、香瓜、火龍果、櫻桃、草莓是鉀含量較多的水果要避免吃。純果汁、果菜汁也要避免喝。\n★中藥類：中藥材燉補品、雞湯、肉湯，這些都含有很高鉀離子，要避免吃。\n★勾芡類：勾芡食物，燴飯、燴麵、酸辣湯、咖哩飯、羹麵等與燉補品的湯汁要避免吃。\n★湯 類：菜汁、菜湯、肉汁拌飯，會導致高血鉀要避免吃。\n★其 他：咖啡雞精、人參精、運動飲料、巧克力、梅子汁、蕃茄醬等鉀含量叫高，要避免食用。\n\n(3)該如何吃呢?\n★血液透析鉀離子每日攝取量為3000-4000毫克/天。\n★水燙蔬菜：吃蔬菜，要經由燙過後，再以油炒或油拌即可(選用不飽和脂肪油，如芥花油、大豆沙拉油、橄欖油、葵花油、玉米油等)。不食用菜湯、精力湯、生菜。\n★不 喝 湯 ： 不論菜湯或肉湯都含有高量的鉀。勿食用濃縮湯及使用肉汁拌飯。\n★調 味 品 ： 不能用低鈉鹽、薄鹽醬油、無鹽醬油，因為鉀離子含量較高。可以加少許辣椒、八角、胡椒增添味道。\n★低鉀水果：選擇低鉀水果食用，如梨、蘋果、蓮霧、葡萄、水梨、軟柿子、檸檬。吃太多水果也會使得血鉀上升。水果攝取需要營養師建議，每天大約吃2至3 個棒球大小的水果營養就夠。\n★中 草 藥 ：鉀磷離子都較高，由中醫師或西醫師開的處方籤才能吃，如從電台取得，在不清楚來源的情況下都不能吃。"


# def genQuickReplyLevel(dict):
#     temp_arr = []
#     for item in dict:
#         temp_arr.append()

quick_reply_level1 = QuickReply(
    items=[
        QuickReplyButton(
            action=MessageAction(label="1、血壓血糖控制",text="血壓血糖控制")
        ),
        QuickReplyButton(
            action=MessageAction(label="2、認識【蛋白質飲食】",text="認識【蛋白質飲食】")
        )
    ]
)
quick_reply_level2 = QuickReply(
    items=[
        QuickReplyButton(
            action=MessageAction(label="1、認識【鉀】含量高的食物",text="認識【鉀】含量高的食物")
        ),
        QuickReplyButton(
            action=MessageAction(label="2、認識【磷】含量高的食物",text="認識【磷】含量高的食物")
        ),
        QuickReplyButton(
            action=MessageAction(label="3、蛋白質飲食",text="蛋白質飲食(第三期)")
        ),
        QuickReplyButton(
            action=MessageAction(label="4、水份控制",text="水份控制")
        ),
        QuickReplyButton(
            action=MessageAction(label="5、腎臟病常見檢查及其臨床意義",text="腎臟病常見檢查及其臨床意義")
        )
    ]
)
quick_reply_level3 = QuickReply(
    items=[
        QuickReplyButton(
            action=MessageAction(label="1、認識【鉀】含量高的食物",text="認識【鉀】含量高的食物")
        ),
        QuickReplyButton(
            action=MessageAction(label="2、認識【磷】含量高的食物",text="認識【磷】含量高的食物")
        ),
        QuickReplyButton(
            action=MessageAction(label="3、蛋白質飲食",text="蛋白質飲食(第四期)")
        ),
        QuickReplyButton(
            action=MessageAction(label="4、水份控制",text="水份控制")
        ),
        QuickReplyButton(
            action=MessageAction(label="5、腎臟病常見檢查及其臨床意義",text="腎臟病常見檢查及其臨床意義")
        )
    ]
)
quick_reply_level4 = QuickReply(
    items=[
        QuickReplyButton(
            action=MessageAction(label="1、充足的【熱量】攝取",text="充足的【熱量】攝取")
        ),
        QuickReplyButton(
            action=MessageAction(label="2、蛋白質飲食",text="蛋白質飲食(第五期)")
        ),
        QuickReplyButton(
            action=MessageAction(label="3、水份控制",text="水份控制(第五期)")
        ),
        QuickReplyButton(
            action=MessageAction(label="4、鹽分攝取(鈉攝取)",text="鹽分攝取(鈉攝取)")
        ),
        QuickReplyButton(
            action=MessageAction(label="5、認識【鉀】含量高的食物",text="認識【鉀】含量高的食物")
        ),
        QuickReplyButton(
            action=MessageAction(label="6、認識【磷】含量高的食物",text="認識【磷】含量高的食物")
        ),
        QuickReplyButton(
            action=MessageAction(label="7、腎臟病常見檢查及其臨床意義",text="腎臟病常見檢查及其臨床意義")
        ),
    ]
)
quick_reply_level5 = QuickReply(
    items=[
        QuickReplyButton(
            action=MessageAction(label="1、充足的【熱量】攝取",text="充足的【熱量】攝取")
        ),
        QuickReplyButton(
            action=MessageAction(label="2、蛋白質飲食",text="蛋白質飲食(第五期)")
        ),
        QuickReplyButton(
            action=MessageAction(label="3、水份控制",text="水份控制(第五期)")
        ),
        QuickReplyButton(
            action=MessageAction(label="4、鹽分攝取(鈉攝取)",text="鹽分攝取(鈉攝取)")
        ),
        QuickReplyButton(
            action=MessageAction(label="5、認識【鉀】含量高的食物",text="腹膜透析【鉀離子】攝取")
        ),
        QuickReplyButton(
            action=MessageAction(label="6、認識【磷】含量高的食物",text="認識【磷】含量高的食物")
        ),
        QuickReplyButton(
            action=MessageAction(label="7、腎臟病常見檢查及其臨床意義",text="腎臟病常見檢查及其臨床意義")
        ),
    ]
)