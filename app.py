import os

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from respond import *

from data import *


app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# Activity Dictionary
city_dict = generate_city_dict()
city_with_activity = city_dict.keys()
city_month_dict = generate_city_month_dict(city_dict)


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# 訊息傳遞區塊
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    message = ''

    user_input = event.message.text.replace('臺', '台')

    match user_input:
        case input if '/' in input and checkCityMonthFormat(input):
            city, month = input.split('/')
            if city in city_with_activity and month in city_month_dict[city]:
                message = send_city_activity(city_month_dict[city][month])
            else:
                message = TextSendMessage(text=f'唉呀，{city} 在 {month} 沒有喜劇活動喔！')
        case input if input in city_with_activity:
            message = send_city_activity(city_dict[input])
        case input if input in tw_city_list:
            message = TextSendMessage(text=f'唉呀，{input} 最近沒有喜劇活動喔！')
        case input if '/' in input and checkCityRecommendFormat(input):
            city, recommend = input.split('/')
            if city in city_with_activity:
                activity = random_city_recommend_activity(city_dict[city])
                message = send_recommend_activity(activity)
            else:
                message = TextSendMessage(text=f'唉呀，{city} 最近沒有喜劇活動喔！')
        case input if checkRecommendFormat(input):
            activity = random_recommend_activity()
            message = send_recommend_activity(activity)
        case input if '逗逗' in input:
            one_liner = random_one_liner()
            text_message = send_one_liner(one_liner)
            message = TextSendMessage(text=text_message)
        case _:
            return

    line_bot_api.reply_message(event.reply_token, message)


def checkCityMonthFormat(input):
    city, month = input.split('/')
    if city in tw_city_list and month in month_convert_dict.values():
        return True
    else:
        return False


def checkRecommendFormat(input):
    keywords = ['推薦', '隨機推薦', '隨機']
    if any(keyword in input for keyword in keywords):
        return True
    else:
        return False


def checkCityRecommendFormat(input):
    city, recommend = input.split('/')
    keywords = ['推薦', '隨機推薦', '隨機']
    if city in tw_city_list and any(keyword in recommend for keyword in keywords):
        return True
    else:
        return False


@handler.add(FollowEvent)
def handle_follow(event):
    message = TextSendMessage(
        text='喵喵喵～朕想去看喜劇，姑且讓你這卑微的人類告訴我，想去哪個城市看表演吧!\n(๑ↀᆺↀ๑)✧')
    line_bot_api.reply_message(event.reply_token, message)


@handler.add(JoinEvent)
def handle_join(event):
    message = TextSendMessage(
        text='喵喵喵～朕想去看喜劇，姑且讓你們這些卑微的人類告訴我，想去哪個城市看表演吧!\n(๑ↀᆺↀ๑)✧')
    line_bot_api.reply_message(event.reply_token, message)


@handler.add(PostbackEvent)
def handle_postback(event):
    this_month = generateThisMonth()
    message = TextSendMessage(
        text=f'告訴我吧，卑微的人類～你想查詢的城市，如:[台北]，我還可以篩選月份，如:[台北/{this_month}] <(๑ↀVↀ๑)>')
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
