import asyncio
import logging
import signal
import sys
from pyrogram import Client, idle
from TechVJ import app
from flask import Flask

# تنظیمات لاگ
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)

# تنظیم Flask برای Health Check
flask_app = Flask(__name__)

@flask_app.route('/health')
def health_check():
    return "OK", 200

# مدیریت سیگنال SIGTERM
def signal_handler(sig, frame):
    print('Stop signal received, exiting...')
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)

# تابع اصلی برای راه‌اندازی بوت
async def bot_task():
    try:
        await app.start()
        print("Bot is running...")
        await idle()
        await app.stop()
    except Exception as e:
        print(f"Error: {e}")

# تابع برای اجرای Flask
def run_flask():
    flask_app.run(host='0.0.0.0', port=8000)

# اجرای هر دو (بوت و Flask)
if __name__ == "__main__":
    # اجرای Flask توی یه ترد جدا
    from threading import Thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # اجرای بوت
    asyncio.run(bot_task())
