import json
import re
import os
from pathlib import Path
from rapidfuzz import fuzz

# ================= FILE ====================
BASE_DIR = Path(__file__).resolve().parent
FAQ_FILE = BASE_DIR / "faq_toko.json"

with FAQ_FILE.open("r", encoding="utf-8") as f:
    data = json.load(f)

FAQS = data.get("faq", [])
BAD_WORDS = data.get("bad_words", [])

# fallback jika JSON kosong
EXTRA_BAD_WORDS = ["anjing", "bangsat", "kontol", "memek"]
BAD_WORDS = list(set(BAD_WORDS + EXTRA_BAD_WORDS))


# ================= UTIL ====================
def clean_text(text: str) -> str:
    return re.sub(r"[^a-z0-9\s]", "", text.lower()).strip()


def contains_bad_words(text: str) -> bool:
    words = text.split()
    return any(w in words for w in BAD_WORDS)


def is_greeting(text: str) -> bool:
    greetings = [
        "hai", "halo", "hello", "hi",
        "assalamualaikum", "assalamu alaikum",
        "pagi", "siang", "sore", "malam",
        "tes", "test", "permisi"
    ]
    return any(g in text for g in greetings)


def greeting_reply() -> str:
    return (
        "Halo 👋😊\n"
        "Terima kasih telah menghubungi *Toko Grosir Afin Asyfa*.\n\n"
        "Saya asisten virtual yang siap membantu.\n"
        "Silakan tanyakan:\n"
        "• 🕒 Jam buka\n"
        "• 📍 Alamat toko\n"
        "• 🛒  sembako\n"
        "• 📦 Cara order"
    )


# ================= FAQ =====================
def match_faq(text: str):
    best_score = 0
    best_answer = None

    for item in FAQS:
        if not isinstance(item, dict):
            continue

        for kw in item.get("keywords", []):
            score = fuzz.partial_ratio(text, kw.lower())
            if score > best_score:
                best_score = score
                best_answer = item.get("answer")

    return best_answer if best_score >= 65 else None


# ================= MAIN ====================
def get_bot_reply(message: str) -> str:
    if not message:
        return greeting_reply()

    cleaned = clean_text(message)

    # 1️⃣ SAPAAN
    if is_greeting(cleaned):
        return greeting_reply()

    # 2️⃣ KATA KASAR
    if contains_bad_words(cleaned):
        return (
            "🙏 Mohon menggunakan bahasa yang sopan ya.\n"
            "Kami siap membantu dengan senang hati 😊"
        )

    # 3️⃣ FAQ
    faq_answer = match_faq(cleaned)
    if faq_answer:
        return faq_answer

    # 4️⃣ DEFAULT RAMAH (TANPA AI)
    return (
        "🙏 Terima kasih atas pertanyaannya.\n"
        "Silakan tanyakan tentang jam buka, alamat, produk, atau cara order.\n\n"
        "Jika perlu, hubungi admin WhatsApp 083161356733 😊"
    )
