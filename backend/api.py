import json


class GETfoodDataAPI():
    def __init__(self, query):
        self.flexMessage_carousel = {
            "type": "carousel",
            "contents": []
        }
        self.query_data = query
        self.req = ''


    def excute(self):
        self.genAPI(self.query_data)

        return self.req

    def genAPI(self, query_data):
        colorNa, colorP, colorKa, colorTitle, nameTitle = '', '', '', '', ''

        for item in query_data:
            noticeDict = {}
            noticeFormat = []

            if item.protein:
                proteinDesc = item.protein.proteinDesc
                noticeDict[0] = {
                    'descName': proteinDesc,
                    'isDesc': True,
                }
            else :
                proteinDesc = ' '
                noticeDict[0] = {
                    'descName': proteinDesc,
                    'isDesc': False,
                }


            ###判斷底下顯示內容與值得顏色###
            if item.foodNaa > 700:
                colorNa = '#FF0000'
                noticeDict[1] = {
                    "descName": "為高鹽份食品，要避免吃。此外，少外食，少吃加工食品，養成清淡飲食習慣。",
                    "isDesc": True,
                }
            else:
                colorNa = '#888888'
                noticeDict[1] = {
                    "descName": " ",
                    "isDesc": False,
                }

            if item.foodP > 250:
                colorP = '#FF0000'
                noticeDict[2] = {
                    "descName": "為高磷食品，要避免吃。常見堅果類、奶類製品、動物內臟、加工食品，也為高磷食物要避免吃。",
                    "isDesc": True,
                }
            else:
                colorP = '#888888'
                noticeDict[2] = {
                    "descName": " ",
                    "isDesc": False,
                }

            if item.foodKa > 300:
                colorKa = '#FF0000'
                noticeDict[3] = {
                    "descName": "為高鉀食品，要避免吃。建議吃蔬菜前先川燙，菜湯不喝。全穀物、果乾、乾香菇避免吃。",
                    "isDesc": True,
                }
            else:
                colorKa = '#888888'
                noticeDict[3] = {
                    "descName": " ",
                    "isDesc": False,
                }

            for i in noticeDict:
                if noticeDict[i]['isDesc'] != False:
                    noticeFormat.append({
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": noticeDict[i]['descName'],
                                "wrap": True,
                                "weight": "bold",
                                "color": "#000000"
                            }
                        ],
                    })


            ####判斷標題####
            if colorNa == '#FF0000' or colorP == '#FF0000' or colorKa == '#FF0000':
                colorTitle = '#FF0000'
                nameTitle = '不建議吃'
                imageUrl = "https://upload.cc/i1/2022/02/13/Dk4q3b.png"
            else:
                colorTitle = '#000000'
                nameTitle = '可安全食用'
                imageUrl = "https://upload.cc/i1/2022/02/13/uNfmWz.png"



            flexMessage_bubble = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                            "type": "text",
                            "text": nameTitle,
                            "align": "center",
                            "offsetStart": "17px",
                            "size": "xxl",
                            "weight": "bold",
                            "color": colorTitle,
                            }
                        ],
                        "paddingBottom": "10px",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "paddingTop": "40px"
                        },
                        {
                        "type": "separator",
                        "color": "#aaaaaa"
                        },
                        {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                "type": "text",
                                "text": "【" + item.foodName + "】",
                                "wrap": True,
                                "size": "xl",
                                "weight": "bold",
                                "flex": 7
                                }
                            ]
                            },
                            {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                    "type": "text",
                                    "text": "熱量(Kcal)",
                                    "color": "#888888"
                                    },
                                    {
                                    "type": "text",
                                    "text": str(item.foodKcal),
                                    "align": "end",
                                    "color": "#888888"
                                    }
                                ]
                                },
                                {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                    "type": "text",
                                    "text": "蛋白質(g)",
                                    "color": "#888888"
                                    },
                                    {
                                    "type": "text",
                                    "text": str(item.foodProtein),
                                    "align": "end",
                                    "color": "#888888"
                                    }
                                ]
                                },
                                {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                    "type": "text",
                                    "text": "鈉(mg)",
                                    "color": "#888888"
                                    },
                                    {
                                    "type": "text",
                                    "text": str(item.foodNaa),
                                    "align": "end",
                                    "color": colorNa
                                    }
                                ]
                                },
                                {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                    "type": "text",
                                    "text": "鉀(mg)",
                                    "color": "#888888"
                                    },
                                    {
                                    "type": "text",
                                    "text": str(item.foodKa),
                                    "align": "end",
                                    "color": colorKa
                                    }
                                ]
                                },
                                {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                    "type": "text",
                                    "text": "磷(mg)",
                                    "color": "#888888"
                                    },
                                    {
                                    "type": "text",
                                    "text": str(item.foodP),
                                    "align": "end",
                                    "color": colorP
                                    }
                                ]
                                },
                                {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                    "type": "text",
                                    "text": "碳水化合物(g)",
                                    "color": "#888888"
                                    },
                                    {
                                    "type": "text",
                                    "text": str(item.foodCarbohydrate),
                                    "align": "end",
                                    "color": "#888888"
                                    }
                                ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "每份 100公克",
                                            "wrap": True,
                                            "color": "#888888",
                                            "flex": 4,
                                            "gravity": "bottom",
                                        }
                                    ],
                                    "paddingTop": "20px",
                                }
                            ],
                            "paddingTop": "10px"
                            },
                            {
                            "type": "box",
                            "layout": "vertical",
                            "contents": noticeFormat,
                            "paddingTop": "15px",
                            }
                        ],
                        "paddingStart": "20px",
                        "paddingEnd": "20px",
                        "paddingTop": "20px",
                        "paddingBottom": "20px"
                        },
                        {
                            "type": "image",
                            "url": imageUrl,
                            "aspectMode": "cover",
                            "position": "absolute",
                            "offsetStart": "-20px",
                            "size": "lg",
                            "offsetTop": "-35px"
                        }
                    ],
                    "paddingAll": "0px"
                }
            }
            self.flexMessage_carousel['contents'].append(flexMessage_bubble)

        self.req = self.flexMessage_carousel

class GETrichMenuURIAPI():
    def __init__(self, userId, title):
        self.userId = userId
        self.title = title
        self.req = ''

    def excute(self):
        self.genAPI(self.userId,self.title)

        return self.req

    def genAPI(self, userId, title):
        dict = {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": title,
                                "align": "center",
                                "gravity": "center",
                                "weight": "bold",
                                "size": "lg",
                                "color": "#aaaaaa"
                            },
                            {
                                "type": "button",
                                "action": {
                                "type": "uri",
                                "uri": "http://linecorp.com/"+userId,
                                "label": "點我前往"
                                },
                                "style": "link"
                            }
                            ],
                            "paddingTop": "10px"
                        }
                        ],
                        "paddingAll": "0px"
                    }
                }

        self.req = dict


