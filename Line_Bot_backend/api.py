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

        for item in query_data:
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
                            "text": "不建議吃！！",
                            "align": "center",
                            "offsetStart": "15px",
                            "size": "xl",
                            "weight": "bold"
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
                                },
                                {
                                "type": "text",
                                "text": "每份 100公克",
                                "wrap": True,
                                "color": "#888888",
                                "flex": 4,
                                "gravity": "bottom",
                                "align": "end"
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
                                    "text": "鉀(mg)",
                                    "color": "#888888"
                                    },
                                    {
                                    "type": "text",
                                    "text": str(item.foodKa),
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
                                    "text": "磷(mg)",
                                    "color": "#888888"
                                    },
                                    {
                                    "type": "text",
                                    "text": str(item.foodP),
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
                                }
                            ],
                            "paddingTop": "20px"
                            },
                            {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                "type": "text",
                                "text": "為高鉀食品，要避免食用。建議吃蔬菜前先川燙，菜湯不喝。全穀物、果乾、乾香菇避免吃。",
                                "wrap": True,
                                "weight": "bold",
                                "color": "#000000"
                                }
                            ],
                            "paddingTop": "15px",
                            "height": "100px"
                            }
                        ],
                        "paddingStart": "20px",
                        "paddingEnd": "20px",
                        "paddingTop": "20px"
                        },
                        {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                            "type": "button",
                            "action": {
                                "type": "message",
                                "label": "搜尋記錄",
                                "text": "hello"
                            },
                            "align": "end"
                            },
                            {
                            "type": "text",
                            "text": "搜尋記錄",
                            "action": {
                                "type": "message",
                                "label": "action",
                                "text": "hello"
                            },
                            "align": "center",
                            "weight": "bold",
                            "size": "xxl"
                            }
                        ],
                        "paddingTop": "30px",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "paddingBottom": "15px"
                        },
                        {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "80px",
                        "height": "80px",
                        "backgroundColor": "#cccccc",
                        "position": "absolute"
                        }
                    ],
                    "paddingAll": "0px"
                }
            }
            self.flexMessage_carousel['contents'].append(flexMessage_bubble)

        self.req = self.flexMessage_carousel


    def genJSON(self):
        with open('./assets/card.json', 'w', encoding='utf-8') as json_file:
            json.dump(self.flexMessage_carousel, json_file)

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