import json
import re
from pathlib import Path

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
    # Menghapus karakter khusus
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return text.strip()

# =============================
# LOGIKA PENCARIAN JAWABAN
# =============================
def get_bot_reply(user_input: str) -> str:
    if not user_input:
        return "Ada yang bisa saya bantu?"

    clean_input = normalize_text(user_input)

    # 1. Cek Kata Kasar (Bad Words)
    if any(word in clean_input for word in BAD_WORDS):
        return "Mohon gunakan bahasa yang sopan ya Kak 😊 Kami siap membantu dengan senang hati."

    # 2. Cek Sapaan Sederhana
    greetings = ["halo", "hai", "p", "siang", "pagi", "sore", "malam", "assalamualaikum"]
    if clean_input in greetings:
        return (
            "Halo 👋 Selamat datang di Vivian Collection!\n\n"
            "Ada yang bisa kami bantu? Silakan tanya tentang:\n"
            "• Jam buka toko\n"
            "• Alamat toko\n"
            "• Produk yang tersedia\n"
            "• Cara order"
        )

    # 3. Cari Jawaban berdasarkan Keyword di FAQ
    matched_answer = None
    max_matches = 0

    for faq in FAQS:
        matches = 0
        for keyword in faq["keywords"]:
            if keyword.lower() in clean_input:
                matches += 1
        
        if matches > max_matches:
            max_matches = matches
            matched_answer = faq["answer"]

    if matched_answer:
        return matched_answer

    # 4. Jawaban jika tidak mengerti (Fallback)
    return (
        "Maaf, saya belum memahami pertanyaan tersebut 🤔\n\n"
        "Bisa coba gunakan kata kunci lain seperti 'lokasi', 'cara pesan', atau 'produk'?"
    )
