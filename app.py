from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage
import schedule
import time
import threading
import os
from dotenv import load_dotenv

load_dotenv()  # 加載 .env 文件

app = Flask(__name__)

# 加載環境變數
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

# 確認環境變數已設置
if LINE_CHANNEL_ACCESS_TOKEN is None or LINE_CHANNEL_SECRET is None:
    raise ValueError("環境變數 LINE_CHANNEL_ACCESS_TOKEN 或 LINE_CHANNEL_SECRET 未設置")

# 設置 Line Bot API 和 WebhookHandler
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'  # 確保返回 200 狀態碼

def send_drink_water_reminder():
    # 這裡使用 broadcast 來發送消息給所有用戶
    message = TextSendMessage(text='記得喝水哦！💧')
    line_bot_api.broadcast(message)

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
