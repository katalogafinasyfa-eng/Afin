import os
import logging
import pytz
from datetime import datetime, time
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Import logika chatbot
from core import get_bot_reply

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
JKT_TZ = pytz.timezone("Asia/Jakarta")

# ... (logika is_open_now dan handler lainnya tetap sama) ...

def main():
    if not TOKEN:
        print("❌ ERROR: TELEGRAM_TOKEN tidak ditemukan!")
        return

    # SOLUSI FINAL: Masukkan timezone ke builder SEBELUM build 
    # agar APScheduler tidak mencari timezone sistem sendiri.
    app = ApplicationBuilder() \
        .token(TOKEN) \
        .timezone(JKT_TZ) \
        .job_queue(None) \
        .build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot Berhasil Jalan!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()