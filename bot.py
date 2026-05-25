import telebot
from telebot.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

import json
import os

# ================= CONFIG =================

TOKEN = "8899354895:AAGDhY-1DT4vQIbcWpR4u2h7MS4radBeNA4"

ADMIN_ID = 7237976087

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

        # Referral bonus
        if len(args) > 1:

            referrer = args[1]

            if referrer != user_id and referrer in users:

                users[referrer]["balance"] += REF_BONUS
                users[referrer]["referrals"] += 1

                bot.send_message(
                    referrer,
                    f"🎉 New Referral!\n💰 Earned ৳{REF_BONUS}"
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

@bot.message_handler(func=lambda m: m.text == "📋 Tasks")
def tasks(message):

    markup = InlineKeyboardMarkup()

    # Channel 1
    markup.row(
        InlineKeyboardButton(
            "📢 Join Channel 1",
            url=CHANNEL_1
        ),

        InlineKeyboardButton(
            "✅ Verify",
            callback_data="task1"
        )
    )

    # Channel 2
    markup.row(
        InlineKeyboardButton(
            "📢 Join Channel 2",
            url=CHANNEL_2
        ),

        InlineKeyboardButton(
            "✅ Verify",
            callback_data="task2"
        )
    )

    # Channel 3
    markup.row(
        InlineKeyboardButton(
            "📢 Join Channel 3",
            url=CHANNEL_3
        ),

        InlineKeyboardButton(
            "✅ Verify",
            callback_data="task3"
        )
    )

    # Bot 1
    markup.row(
        InlineKeyboardButton(
            "🤖 Join Bot 1",
            url=BOT_1
        ),

        InlineKeyboardButton(
            "✅ Verify",
            callback_data="task4"
        )
    )

    # Bot 2
    markup.row(
        InlineKeyboardButton(
            "🤖 Join Bot 2",
            url=BOT_2
        ),

        InlineKeyboardButton(
            "✅ Verify",
            callback_data="task5"
        )
    )

    # YouTube
    markup.row(
        InlineKeyboardButton(
            "▶️ Subscribe YouTube",
            url=YOUTUBE
        ),

        InlineKeyboardButton(
            "✅ Verify",
            callback_data="task6"
        )
    )

    bot.send_message(
        message.chat.id,
        "📋 Complete All Tasks:",
        reply_markup=markup
    )

# ================= VERIFY =================

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    user_id = str(call.from_user.id)

    if user_id not in users:

        users[user_id] = {
            "balance": 0,
            "referrals": 0,
            "completed": []
        }

    if "completed" not in users[user_id]:
        users[user_id]["completed"] = []

    # Prevent repeat reward
    if call.data in users[user_id]["completed"]:

        bot.answer_callback_query(
            call.id,
            "❌ Already Completed"
        )

        return

    # Add task to completed
    users[user_id]["completed"].append(call.data)

    # Add reward
    users[user_id]["balance"] += 2

    save_users()

    bot.answer_callback_query(
        call.id,
        "✅ Reward Added ৳2"
    )

    bot.send_message(
        call.message.chat.id,
        f"🎉 Task Completed\n💰 Balance: ৳{users[user_id]['balance']}"
    )

# ================= BALANCE =================

@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def balance(message):

    user_id = str(message.from_user.id)

    if user_id not in users:

        users[user_id] = {
            "balance": 0,
            "referrals": 0,
            "completed": []
        }

        save_users()

    bal = users[user_id]["balance"]

    bot.send_message(
        message.chat.id,
        f"""💰 YOUR BALANCE

💵 Balance: ৳{bal}

👥 Referrals: {users[user_id]['referrals']}"""
    )

# ================= REFER =================

@bot.message_handler(func=lambda m: m.text == "👥 Refer")
def refer(message):

    user_id = message.from_user.id

    bot_username = bot.get_me().username

    link = f"https://t.me/{bot_username}?start={user_id}"

    bot.send_message(
        message.chat.id,
        f"""👥 REFER & EARN

💰 Earn ৳3 Per Referral

🔗 Your Link:
{link}"""
    )

# ================= LEADERBOARD =================

@bot.message_handler(func=lambda m: m.text == "🏆 Leaderboard")
def leaderboard(message):

    top_users = sorted(
        users.items(),
        key=lambda x: x[1]["balance"],
        reverse=True
    )

    text = "🏆 TOP USERS\n\n"

    count = 1

    for uid, data in top_users[:10]:

        text += f"{count}. User {uid} — ৳{data['balance']}\n"

        count += 1

    bot.send_message(message.chat.id, text)

# ================= WITHDRAW =================

@bot.message_handler(func=lambda m: m.text == "💸 Withdraw")
def withdraw(message):

    user_id = str(message.from_user.id)

    bal = users[user_id]["balance"]

    if bal < MIN_WITHDRAW:

        bot.send_message(
            message.chat.id,
            f"❌ Minimum Withdraw = ৳{MIN_WITHDRAW}"
        )

        return

    bot.send_message(
        message.chat.id,
        "💳 Send Your Bkash/Nagad Number"
    )

# ================= RUN =================

print("Bot Running...")

bot.infinity_polling()