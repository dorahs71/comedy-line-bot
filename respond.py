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
            alt_text='recommend_activity',
            contents=json_file
        )
    except:
        recommend_message = TextSendMessage(text='唉呀...出了點問題耶～')

    return recommend_message
