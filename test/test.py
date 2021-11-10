    ###透過flask orm 找出符合蛋糕的產品並轉呈jsonfile####

    #####要做成API#####

    query_text = '蛋糕'
    sql_flexMessage_dict_carousel = {
        "type": "carousel",
        "contents": []
    }
    outputData = Product.query.filter(Product.product_name.like('%'+ query_text + '%') if query_text is not None else '').all()

    for item in outputData:
        sql_flexMessage_dict_bubble = {
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
                            "text": "【" + item.product_name + "】",
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
                                "text": str(item.product_kcal),
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
                                "text": str(item.product_protein),
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
                                "text": str(item.product_Na),
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
                                "text": str(item.product_Ka),
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
                                "text": str(item.product_p),
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
                                "text": str(item.product_carbohydrate),
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
        sql_flexMessage_dict_carousel['contents'].append(sql_flexMessage_dict_bubble)


    with open('./assets/card.json', 'w', encoding='utf-8') as json_file:
        json.dump(sql_flexMessage_dict_carousel, json_file)




###將資料匯進有外鍵資料庫的方法####
#dirname = os.path.dirname(__file__)
    #filePath = os.path.join(dirname, 'sql_product.csv')
    #import csv
    #with open(filePath) as f:
    #    f_csv = csv.reader(f, delimiter=';')
    #    for index, row in enumerate(f_csv):
    #        if(index != 0):
    #            test = int(row[9])
    #            if (test == 0):
    #                new_product = Product(product_name=row[1], product_tag=row[2], product_kcal=float(row[3]), #product_protein=float(row[4]), product_Na=float(row[5]),product_Ka=float(row[6]),product_p=float(row#[7]),product_carbohydrate=float(row[8]))
    #                db.session.add(new_product)
    #                db.session.commit()
    #            else:
    #                new_product = Product(product_name=row[1], product_tag=row[2], product_kcal=float(row[3]), #product_protein=float(row[4]), product_Na=float(row[5]),product_Ka=float(row[6]),product_p=float(row#[7]),product_carbohydrate=float(row[8]),product_protein_range=test)
    #                db.session.add(new_product)
    #                db.session.commit()