import telebot
from telebot.types import *
import json
import os

# ================= CONFIG =================

TOKEN = "8899354895:AAGDhY-1DT4vQIbcWpR4u2h7MS4radBeNA4"

CHANNEL_1 = "https://t.me/remembermefrnd"
CHANNEL_2 = "https://t.me/UBDTG_Earn_Bot"
CHANNEL_3 = "https://t.me/lotsofincome"

BOT_1 = "https://t.me/FoxiGrowbot?start=ref_7237976087"
BOT_2 = "https://t.me/GmailFarmerBot?start=7237976087"

YOUTUBE = "https://youtube.com/@ultrabd"

REF_BONUS = 3
MIN_WITHDRAW = 10

# ==========================================

bot = telebot.TeleBot(TOKEN)

DATA_FILE = "users.json"

# ================= DATABASE =================

if os.path.exists(DATA_FILE):

    with open(DATA_FILE, "r") as f:
        users = json.load(f)

else:
    users = {}


def save_users():

    with open(DATA_FILE, "w") as f:
        json.dump(users, f)


# ================= START =================

@bot.message_handler(commands=['start'])
def start(message):

    user_id = str(message.from_user.id)

    args = message.text.split()

    if user_id not in users:

        users[user_id] = {
            "balance": 0,
            "referrals": 0,
            "completed": []
        }

        # Referral Bonus
        if len(args) > 1:

            referrer = args[1]

            if referrer != user_id and referrer in users:

                users[referrer]["balance"] += REF_BONUS
                users[referrer]["referrals"] += 1

                bot.send_message(
                    referrer,
                    f"🎉 New Referral Joined!\n💰 +৳{REF_BONUS}"
                )

        save_users()

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row("📋 Tasks", "💰 Balance")
    markup.row("👥 Refer", "🏆 Leaderboard")
    markup.row("💸 Withdraw")

    bot.send_message(
        message.chat.id,
        """👋 Welcome To UBD TASKS

💰 Earn Money By Completing Tasks

✅ Join Channels
✅ Join Bots
✅ Refer Friends

💵 Every Task Reward = ৳2""",
        reply_markup=markup
    )

# ================= TASKS =================

@bot.message_handler(func=lambda m: m.text ==