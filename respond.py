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


def send_recommend_activity():
    activity = random_recommend_activity()
    content_json = recommend_json(
        activity[3], activity[0], activity[1], activity[2], activity[-1])
    recommend_message = FlexSendMessage(
        alt_text='recommend_activity',
        contents=content_json
    )

    return recommend_message
