import json
from .db import SQLManger
from PIL import Image
import os
dirname = os.path.dirname(__file__)
filePath = os.path.join(dirname, 'assets/images')

class GETfoodDataAPI():
    def __init__(self):
        self.flexMessage_carousel = {
            "type": "carousel",
            "contents": []
        }
        self.result = ''


    def excute(self, dataFood, dataSuggestion):
        self.genAPI(dataFood, dataSuggestion)

        return self.result

    def genAPI(self, dataFood, dataSuggestion):
        colorNa, colorP, colorKa, colorTitle, nameTitle = '', '', '', '', ''

        _foodSuggestion = {
            'suggestionHighProtein': dataSuggestion[0]['suggest'],
            'suggestionLowProtein': dataSuggestion[1]['suggest'],
            'suggestionKa': dataSuggestion[2]['suggest'],
            'suggestionP': dataSuggestion[3]['suggest'],
            'suggestionNa': dataSuggestion[4]['suggest'],
        }

        for item in dataFood:
            noticeDict = {}
            noticeFormat = []

            if item['proteinDesc']:
                proteinDesc = item['proteinDesc']
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
            if item['foodNaa'] > 700:
                colorNa = '#FF0000'
                noticeDict[1] = {
                    "descName": _foodSuggestion['suggestionNa'],
                    "isDesc": True,
                }
            else:
                colorNa = '#888888'
                noticeDict[1] = {
                    "descName": " ",
                    "isDesc": False,
                }

            if item['foodP']> 250:
                colorP = '#FF0000'
                noticeDict[2] = {
                    "descName": _foodSuggestion['suggestionP'],
                    "isDesc": True,
                }
            else:
                colorP = '#888888'
                noticeDict[2] = {
                    "descName": " ",
                    "isDesc": False,
                }

            if item['foodKa']> 300:
                colorKa = '#FF0000'
                noticeDict[3] = {
                    "descName": _foodSuggestion['suggestionKa'],
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
                                "text": "【" + item['foodName'] + "】",
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
                                    "text": str(item['foodKcal']),
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
                                    "text": str(item['foodProtein']),
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
                                    "text": str(item['foodNaa']),
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
                                    "text": str(item['foodKa']),
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
                                    "text": str(item['foodP']),
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
                                    "text": str(item['foodCarbohydrate']),
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

        self.result = self.flexMessage_carousel

class GETsubMedicalAPI():
    def __init__(self):
        self.flexMessage_carousel = {
            "type": "carousel",
            "contents": []
        }
        self.result_FlexMessage = ''
        self.result_ReplyMessage = ''
        self.result_QuickReply = ''


    def excute(self, dataMedical):
        self.genAPI(dataMedical)

        return self.result_FlexMessage, self.result_ReplyMessage, self.result_QuickReply

    def genAPI(self, dataMedical):

        for item in dataMedical:

            test = item['imgsrc'].split('/')[-1]
            img = Image.open(f"{filePath}/{test}")
            w = img.width
            h = img.height

            image = {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "image",
                        "url": item['imgsrc'],
                        "size": "100%",
                        "aspectRatio": f"{w}:{h}",
                        "aspectMode": "fit"
                    }
                ]
            } if item['imgsrc'] else {
                "type": "box",
                "layout": "vertical",
                "contents": []
            }

            flexMessage_bubble = {
                "type": "bubble",
                "size": "giga",
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
                                    "contents": [
                                        {
                                            "type": "span",
                                            "text": item['title'],
                                            "color": "#2b7ce6",
                                            "weight": "bold",
                                            "size": "lg"
                                        }
                                    ]
                                }
                            ],
                            "paddingBottom": "10px"
                        },
                        image
                    ],
                    "paddingAll": "15px"
                }
            }

            new_text = item['full_desc'].replace('\\n', '\n')
            self.result_ReplyMessage = new_text
            self.result_QuickReply = item['checklist']

        self.result_FlexMessage = flexMessage_bubble

class GETmedicalAPI():

    def __init__(self):
        self.flexMessage_carousel = {
            "type": "carousel",
            "contents": []
        }
        self.result = ''


    def excute(self, dataMedical):
        self.genAPI(dataMedical)

        return self.result

    def genAPI(self, dataMedical):

        for item in dataMedical:

            infoList = []
            for index, info in enumerate(eval(item['infolist'])):
                infoList.append({
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"{index+1}、{info['title']}",
                            "size": "md",
                            "weight": "bold",
                            "color": "#2b7ce6",
                            "action": {
                                "type": "message",
                                "label": "action",
                                "text": info['title']
                            }
                        },
                    ],
                    "paddingBottom": "10px"
                })
            flexMessage_bubble = {
                "type": "bubble",
                "size": "kilo",
                "direction": "ltr",
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
                            "text": "第三期",
                            "weight": "bold",
                            "size": "xl",
                            "align": "center",
                            "contents": [
                            {
                                "type": "span",
                                "text": item['title']
                            }
                            ]
                        }
                        ],
                        "justifyContent": "center",
                        "alignItems": "center",
                        "paddingBottom": "5px",
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
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "size": "xs",
                                "weight": "bold",
                                "text": item['brief_desc'] if item['brief_desc'] else ' ',
                                "wrap": True,
                                "color": "#acacac"
                            }
                            ],
                            "paddingBottom": "5px"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": item['notification'],
                                "color": "#acacac",
                                "size": "sm",
                                "weight": "bold"
                            }
                            ],
                            "paddingBottom": "20px"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": infoList,
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": " ",
                                "size": "md",
                                "weight": "bold",
                                "color": "#2b7ce6"
                            }
                            ],
                            "paddingBottom": "10px"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": " ",
                                "size": "md",
                                "weight": "bold",
                                "color": "#2b7ce6"
                            }
                            ],
                            "paddingBottom": "10px"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": " ",
                                "size": "md",
                                "weight": "bold",
                                "color": "#2b7ce6"
                            }
                            ],
                            "paddingBottom": "10px"
                        }
                        ],
                        "paddingTop": "15px",
                        "paddingBottom": "15px",
                        "paddingStart": "18px",
                        "paddingEnd": "18px"
                    }
                    ],
                    "paddingAll": "0px"
                }
            }



        self.result = flexMessage_bubble

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