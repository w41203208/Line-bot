




###將資料匯進有外鍵資料庫的方法####
    # dirname = os.path.dirname(__file__)
    # filePath = os.path.join(dirname, 'sql_product.csv')
    # import csv
    # with open(filePath) as f:
    #     f_csv = csv.reader(f, delimiter=';')
    #     for index, row in enumerate(f_csv):
    #         if(index != 0):
    #             test = int(row[9])
    #             if (test == 0):
    #                 new_product = Food(
    #                     foodName=row[1],
    #                     foodTag=row[2],
    #                     foodKcal=float(row[3]),
    #                     foodProtein=float(row[4]),
    #                     foodNaa=float(row[5]),
    #                     foodKa=float(row[6]),
    #                     foodP=float(row[7]),
    #                     foodCarbohydrate=float(row[8])
    #                 )
    #                 db.session.add(new_product)
    #                 db.session.commit()
    #             else:
    #                 new_product = Food(
    #                     foodName=row[1],
    #                     foodTag=row[2],
    #                     foodKcal=float(row[3]),
    #                     foodProtein=float(row[4]),
    #                     foodNaa=float(row[5]),
    #                     foodKa=float(row[6]),
    #                     foodP=float(row[7]),
    #                     foodCarbohydrate=float(row[8]),foodProteinId=test
    #                 )
    #                 db.session.add(new_product)
    #                 db.session.commit()



'''
rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=1686),
        selected=False,
        name="Nice richmenu",
        chat_bar_text="KCS小助手",
        areas=[
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=2500, height=1686),
                action=MessageAction(label='註冊', text='註冊')
            )
        ]
    )
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    with open('./assets/images/test.jpeg', 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, "image/jpeg", f)
'''

'''
rich_menu_to_create = RichMenu(
    size=RichMenuSize(width=2500, height=1686),
    selected=False,
    name="Nice richmenu",
    chat_bar_text="KCS小助手",
    areas=[
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=2500, height=1686),
            action=MessageAction(label='註冊', text='註冊')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=2500, height=1686),
            action=MessageAction(label='註冊', text='註冊')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=2500, height=1686),
            action=MessageAction(label='註冊', text='註冊')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=2500, height=1686),
            action=MessageAction(label='註冊', text='註冊')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=2500, height=1686),
            action=MessageAction(label='註冊', text='註冊')
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=2500, height=1686),
            action=MessageAction(label='註冊', text='註冊')
        )
    ]
)
rich_menu_id = line_bot_api.create_rich_men(rich_menu=rich_menu_to_create)
with open('./assets/images/test.jpeg', 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, "image/jpeg", f)
'''