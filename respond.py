from linebot.models import *

from data import *

from message_json import *

import random


def send_sticker():
    random_sticker_id = random.randint(1988, 2027)
    sticker_message = StickerSendMessage(
        package_id='446',
        sticker_id=random_sticker_id
    )

    return sticker_message


def send_recommend_activity(activity):
    json_file = generate_activity_json(
        activity[-2], activity[0], activity[1], activity[2], activity[-1])

    try:
        recommend_message = FlexSendMessage(
            alt_text='阿鏘推薦喜劇',
            contents=json_file
        )
    except:
        recommend_message = TextSendMessage(text='唉呀...出了點問題耶～')

    return recommend_message


def send_city_activity(city_activity_list):
    if len(city_activity_list) == 1:
        activity = city_activity_list[0]
        city_message = send_recommend_activity(activity)

        return city_message

    elif len(city_activity_list) > 8:
        city_activity_list = city_activity_list[:8]

    json_file = [generate_activity_json(
        activity[-2], activity[0], activity[1], activity[2], activity[-1]) for activity in city_activity_list]
    flex_contents = {"type": "carousel", "contents": json_file}

    try:
        city_message = FlexSendMessage(
            alt_text='阿鏘帶你看喜劇',
            contents=flex_contents
        )
    except:
        city_message = TextSendMessage(text='唉呀...出了點問題耶～')

    return city_message
