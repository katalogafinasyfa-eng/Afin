# main.py / telegram_bot.py
import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# =============================
# LOAD ENV
# =============================
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("TOKEN Telegram tidak ditemukan di .env!")

# =============================
# LOAD DATA FAQ
# =============================
BASE_DIR = Path(__file__).resolve().parent
FAQ_FILE = BASE_DIR / "faq_toko.json"

try:
    with FAQ_FILE.open("r", encoding="utf-8") as f:
        DATA = json.load(f)
    FAQS = DATA["faq"]
    BAD_WORDS = DATA.get("bad_words", [])
except FileNotFoundError:
    print("Error: File faq_toko.json tidak ditemukan!")
    FAQS = []
    BAD_WORDS = []

# =============================
# FUNGSI PEMBERSIH TEKS
# =============================
def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return text.strip()

# =============================
# LOGIKA FAQ BOT
# =============================
def get_bot_reply(user_input: str) -> str:
    if not user_input:
        return "Ada yang bisa saya bantu?"

    clean_input = normalize_text(user_input)

    # 1. Cek Kata Kasar
    if any(word in clean_input for word in BAD_WORDS):
        return "Mohon gunakan bahasa yang sopan ya Kak 😊 Kami siap membantu dengan senang hati."

    # 2. Sapaan
    greetings = ["halo", "hai", "p", "siang", "pagi", "sore", "malam", "assalamualaikum"]
    if clean_input in greetings:
        return (
            "Halo 👋 Selamat datang di Rayhan Water!\n\n"
            "Ada yang bisa kami bantu? Silakan tanya tentang:\n"
            "• Jam buka toko\n"
            "• Alamat toko\n"
            "• Produk yang tersedia\n"
            "• Cara order"
        )

    # 3. Cari jawaban FAQ
    matched_answer = None
    max_matches = 0
    for faq in FAQS:
        matches = sum(1 for keyword in faq["keywords"] if keyword.lower() in clean_input)
        if matches > max_matches:
            max_matches = matches
            matched_answer = faq["answer"]

    if matched_answer:
        return matched_answer

    # 4. Fallback
    return (
        "Maaf, saya belum memahami pertanyaan tersebut 🤔\n\n"
        "Bisa coba gunakan kata kunci lain seperti 'lokasi', 'cara pesan', atau 'produk'?"
    )

# =============================
# HANDLER TELEGRAM
# =============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo 👋 Selamat datang di Rayhan Water!\nSilakan ketik pertanyaan Anda."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = get_bot_reply(user_text)
    await update.message.reply_text(reply)

# =============================
# MAIN
# =============================
def main():
    app = ApplicationBuilder() \
        .token(TOKEN) \
        .build()  # <-- jangan pakai .timezone()

    # Command /start
    app.add_handler(CommandHandler("start", start))
    # Semua pesan masuk
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Jalankan bot
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
