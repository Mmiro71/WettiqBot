import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from bs4 import BeautifulSoup

# Dein Telegram-Bot-Token hier einfügen
TOKEN = "8064368838:AAEA0H52fegUsWKOl3qayuMcmF_aXDzbZ5E"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 📌 **Liste der Quellen für Wett-Tipps**
QUELLEN = [
    "https://www.soccerway.com/",
    "https://www.sportskeeda.com/",
    "https://www.sportytrader.com/",
    "https://www.whoscored.com/",
    "https://www.uefa.com/",
    "https://as.com/futbol",
    "https://www.sportsgambler.com",
    "https://www.footboom1.com",
    "https://dailysports.net",
    "https://www.footboom1.com",
    "https://www.beinsports.com",
    "https://news.22bet.com",
    "https://www.goal.com",
    "https://www.thesun.ie",
    "https://theanalyst.com",
    "https://talksport.com/football",
    "https://www.thisisanfield.com",
    "https://oddspedia.com/football",
    "https://www.bild.de/sport/fussball/",
    "https://www.sportskeeda.com/football",
    "https://www.reuters.com",
    "https://www.espn.com",
]

# 📌 **Funktion: Wett-Tipps suchen**
def get_wett_tipp(spiel):
    ergebnisse = []
    for quelle in QUELLEN:
        try:
            url = f"{quelle}/search?q={spiel} Wett-Tipps"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                links = soup.find_all("a", href=True)

                for link in links:
                    href = link["href"]
                    if "http" in href and quelle in href:
                        ergebnisse.append(href)

                if len(ergebnisse) > 0:
                    return ergebnisse[:5]  # Maximal 5 Ergebnisse zurückgeben
        except Exception as e:
            print(f"Fehler bei {quelle}: {e}")

    return None  # Falls nichts gefunden wird

# 📌 **Telegram-Handler für /start**
@dp.message_handler(commands=["start"])
async def send_welcome(message: Message):
    await message.reply("👋 Willkommen! Gib ein Spiel ein, z. B.: Bayern - Dortmund")

# 📌 **Telegram-Handler für Wett-Tipps**
@dp.message_handler()
async def send_tip(message: Message):
    spiel = message.text.strip()
    tipps = get_wett_tipp(spiel)

    if tipps:
        antwort = f"📊 Wett-Tipps für **{spiel}**:\n\n"
        for tipp in tipps:
            antwort += f"🔗 {tipp}\n"
    else:
        antwort = "❌ Keine Wett-Tipps gefunden."

    await message.reply(antwort, parse_mode="Markdown")

# 📌 **Bot starten**
if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp)
