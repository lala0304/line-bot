from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import schedule
import time
import threading
import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv(JkW7rJP8rQxVZSl8bl++bdVgTbOkPvJefah1hPmC07xh+qFvXawciuNC2iDOSgtbWIizaJvS1rYWjARdvjPPzzk/vZ/RQ+3cD61Lt/tU/D5eSUHvygVHIprXeCp4mxrHlUq8oR5N1X7bLFcjNM7FLQdB04t89/1O/w1cDnyilFU=)
LINE_CHANNEL_SECRET = os.getenv(f475bd13e3d5d5fc374837d7bec07089)

if LINE_CHANNEL_ACCESS_TOKEN is None or LINE_CHANNEL_SECRET is None:
    raise ValueError("環境變數 LINE_CHANNEL_ACCESS_TOKEN 或 LINE_CHANNEL_SECRET 未設置")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

user_ids = []

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    if user_id not in user_ids:
        user_ids.append(user_id)
    reply_message = "已經記錄你的 ID，會在特定時間提醒你喝水。"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

def send_drink_water_reminder():
    for user_id in user_ids:
        line_bot_api.push_message(user_id, TextSendMessage(text='記得喝水哦！'))

def schedule_task():
    schedule.every().day.at("07:00").do(send_drink_water_reminder)
    schedule.every().day.at("09:00").do(send_drink_water_reminder)
    schedule.every().day.at("11:30").do(send_drink_water_reminder)
    schedule.every().day.at("13:00").do(send_drink_water_reminder)
    schedule.every().day.at("15:30").do(send_drink_water_reminder)
    schedule.every().day.at("17:30").do(send_drink_water_reminder)
    schedule.every().day.at("19:00").do(send_drink_water_reminder)
    schedule.every().day.at("21:30").do(send_drink_water_reminder)
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_app():
    threading.Thread(target=schedule_task).start()
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    run_app()
