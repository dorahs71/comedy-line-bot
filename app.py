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


app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


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

    user_input = event.message.text

    if "推薦" in user_input:
        message = send_recommend_activity()
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = send_sticker()
        line_bot_api.reply_message(event.reply_token, message)


@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    name = profile.display_name
    message = TextSendMessage(text=f'哼哼～ {name} 就讓我來為你介紹喜劇大小事吧！')
    line_bot_api.reply_message(event.reply_token, message)


@handler.add(JoinEvent)
def handle_join(event):
    message = TextSendMessage(text='哈哈，歡迎我的加入，就讓我來為你介紹喜劇大小事吧！')
    line_bot_api.reply_message(event.reply_token, message)


@handler.add(MemberJoinedEvent)
def handle_member_joined(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'呵呵～ 歡迎 {name} 的加入，可以問我關於喜劇的事呦！')
    line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
