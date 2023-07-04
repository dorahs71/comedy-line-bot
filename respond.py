from linebot.models import *

from message_json import *


def send_recommend_activity(activity):
    json_file = generate_activity_json(
        activity['img src'], activity['theme'], activity['location'], activity['duration'], activity['link'])

    try:
        recommend_message = FlexSendMessage(
            alt_text='逗逗推薦你喜劇 o(ↀ∀ↀ*)o',
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

    elif len(city_activity_list) > 12:
        city_activity_list = city_activity_list[:12]

    json_file = [generate_activity_json(
        activity['img src'], activity['theme'], activity['location'], activity['duration'], activity['link']) for activity in city_activity_list]
    flex_contents = {"type": "carousel", "contents": json_file}

    try:
        city_message = FlexSendMessage(
            alt_text='逗逗帶你看喜劇 (= ↀωↀ =)/',
            contents=flex_contents
        )
    except:
        city_message = TextSendMessage(text='唉呀...出了點問題耶～')

    return city_message


def send_one_liner(one_liner):
    name = one_liner['name']
    sentence = one_liner['one_liner']
    fb = one_liner['fb']
    ig = one_liner['ig']
    text = f'「{sentence}」-{name}\nFB: {fb}\nIG: {ig}'

    return text
