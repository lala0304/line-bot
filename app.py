import logging
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

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加載環境變數
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

# 確認環境變數已設置
if LINE_CHANNEL_ACCESS_TOKEN is None or LINE_CHANNEL_SECRET is None:
    raise ValueError("環境變數 LINE_CHANNEL_ACCESS_TOKEN 或 LINE_CHANNEL_SECRET 未設置")

# 設置 Line Bot API 和 WebhookHandler
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/", methods=['GET'])
def home():
    return 'Hello, this is the LINE Bot server.', 200

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'  # 確保返回 200 狀態碼

@app.route("/test", methods=['GET'])
def test_message():
    message = "這是一條測試消息。"
    send_drink_water_reminder(message)
    return 'Test message sent!', 200

def send_drink_water_reminder(message):
    logger.info(f"Attempting to send message: {message}")
    try:
        line_bot_api.broadcast(TextSendMessage(text=message))
        logger.info("Sent drink water reminder to all users")
    except Exception as e:
        logger.error(f"Failed to send drink water reminder: {e}")

def schedule_task():
    logger.info("Scheduling tasks")
    # 設置不同時段的定時任務
    schedule.every().day.at("07:00").do(send_drink_water_reminder, message='🌞 早安！現在是早上7點，新的開始，先來一杯清新的水，喚醒一整天的活力吧！')
    schedule.every().day.at("09:00").do(send_drink_water_reminder, message='🚀 工作要有衝勁，現在是早上9點，別忘了喝水提神哦！💧')
    schedule.every().day.at("11:30").do(send_drink_water_reminder, message='🍽 午餐時間快到了，現在是11點半，先喝杯水，準備迎接美味吧！')
    schedule.every().day.at("13:00").do(send_drink_water_reminder, message='☕ 午餐後的一杯水，現在是下午1點，有助於消化，保持健康！')
    schedule.every().day.at("15:30").do(send_drink_water_reminder, message='🌟 下午茶時間到了，現在是下午3點半，來杯水，保持頭腦清醒，繼續高效工作！')
    schedule.every().day.at("17:30").do(send_drink_water_reminder, message='🌅 工作接近尾聲，現在是下午5點半，來杯水，給今天畫個完美的句號！')
    schedule.every().day.at("19:00").do(send_drink_water_reminder, message='🌙 晚飯時間到了，現在是晚上7點，先來一杯水，幫助消化更健康！')
    schedule.every().day.at("21:30").do(send_drink_water_reminder, message='🌜 現在是晚上9點半，睡前喝杯水，保持身體水分充足，迎接美好的夢境！')

    while True:
        logger.info("Checking scheduled tasks")
        # 運行所有的定時任務
        schedule.run_pending()
        time.sleep(60)  # 改為 60 秒以減少日誌量

def run_app():
    logger.info("Starting scheduled tasks")
    # 啟動定時任務線程
    schedule_thread = threading.Thread(target=schedule_task)
    schedule_thread.daemon = True  # 讓線程在主程序結束時自動結束
    schedule_thread.start()
    logger.info("Scheduled tasks started successfully")
    logger.info("Starting Flask app")
    # 啟動 Flask 應用
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    run_app()
