import telebot
from telebot.types import *
import json
import os

# ================== CONFIG ==================

TOKEN = "8899354895:AAGDhY-1DT4vQIbcWpR4u2h7MS4radBeNA4"

# CHANNEL USERNAME ( @ সহ )
CHANNEL_1_USERNAME = "@remembermefrnd"
CHANNEL_2_USERNAME = "@UBDTG_Earn_Bot"
CHANNEL_3_USERNAME = "@lotsofincome"

# CHANNEL LINK
CHANNEL_1 = "https://t.me/remembermefrnd"
CHANNEL_2 = "https://t.me/UBDTG_Earn_Bot"
CHANNEL_3 = "https://t.me/lotsofincome"

# BOT LINK
BOT_1 = "https://t.me/FoxiGrowbot?start=ref_7237976087"
BOT_2 = "https://t.me/GmailFarmerBot?start=7237976087"

# YOUTUBE
YOUTUBE = "https://youtube.com/@ultrabd"

# REWARD
CHANNEL_REWARD = 2
BOT_REWARD = 4
YOUTUBE_REWARD = 2

REF_BONUS = 5
MIN_WITHDRAW = 20

# ============================================

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

        # Referral System
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
        """
👋 Welcome To UBD TASKS

💰 Earn Money By Completing Tasks

✅ Join Channels
✅ Join Bots
✅ Refer Friends

💵 Channel Reward = ৳2
🤖 Bot Reward = ৳4
""",
        reply_markup=markup
    )

# ================= TASKS =================

@bot.message_handler(func=lambda m: m.text == "📋 Tasks")
def tasks(message):

    markup = InlineKeyboardMarkup(row_width=2)

    # CHANNEL 1
    markup.row(
        InlineKeyboardButton(
            "📢 Join Channel 1",
            url=CHANNEL_1
        ),
        InlineKeyboardButton(
            "✅ Verify",
            callback_data="channel1"
        )
    )

    # CHANNEL 2
    markup.row(
        InlineKeyboardButton(
            "📢 Join Channel 2",
            url=CHANNEL_2
        ),
        InlineKeyboardButton(
            "✅ Verify",
            callback_data="channel2"
        )
    )

    # CHANNEL 3
    markup.row(
        InlineKeyboardButton(
            "📢 Join Channel 3",
            url=CHANNEL_3
        ),
        InlineKeyboardButton(
            "✅ Verify",
            callback_data="channel3"
        )
    )

    # BOT 1
    markup.row(
        InlineKeyboardButton(
            "🤖 Join Bot 1",
            url=BOT_1
        ),
        InlineKeyboardButton(
            "✅ Verify ৳4",
            callback_data="bot1"
        )
    )

    # BOT 2
    markup.row(
        InlineKeyboardButton(
            "🤖 Join Bot 2",
            url=BOT_2
        ),
        InlineKeyboardButton(
            "✅ Verify ৳4",
            callback_data="bot2"
        )
    )

    # YOUTUBE
    markup.row(
        InlineKeyboardButton(
            "▶️ Subscribe YouTube",
            url=YOUTUBE
        ),
        InlineKeyboardButton(
            "✅ Verify",
            callback_data="youtube"
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

    # Already Completed
    if call.data in users[user_id]["completed"]:

        bot.answer_callback_query(
            call.id,
            "❌ Already Completed"
        )

        return

    # ============ CHANNEL VERIFY ============

    try:

        if call.data == "channel1":

            member = bot.get_chat_member(
                CHANNEL_1_USERNAME,
                user_id
            )

            if member.status in [
                "member",
                "administrator",
                "creator"
            ]:

                reward = CHANNEL_REWARD

            else:

                bot.answer_callback_query(
                    call.id,
                    "❌ Join Channel First"
                )
                return

        elif call.data == "channel2":

            member = bot.get_chat_member(
                CHANNEL_2_USERNAME,
                user_id
            )

            if member.status in [
                "member",
                "administrator",
                "creator"
            ]:

                reward = CHANNEL_REWARD

            else:

                bot.answer_callback_query(
                    call.id,
                    "❌ Join Channel First"
                )
                return

        elif call.data == "channel3":

            member = bot.get_chat_member(
                CHANNEL_3_USERNAME,
                user_id
            )

            if member.status in [
                "member",
                "administrator",
                "creator"
            ]:

                reward = CHANNEL_REWARD

            else:

                bot.answer_callback_query(
                    call.id,
                    "❌ Join Channel First"
                )
                return

        # BOT TASK
        elif call.data == "bot1":

            reward = BOT_REWARD

        elif call.data == "bot2":

            reward = BOT_REWARD

        # YOUTUBE
        elif call.data == "youtube":

            reward = YOUTUBE_REWARD

        else:

            reward = 0

    except:

        bot.answer_callback_query(
            call.id,
            "❌ Verification Failed"
        )

        return

    # ============ REWARD ADD ============

    users[user_id]["balance"] += reward

    users[user_id]["completed"].append(call.data)

    save_users()

    bot.answer_callback_query(
        call.id,
        f"✅ Reward Added ৳{reward}"
    )

    bot.send_message(
        call.message.chat.id,
        f"""
🎉 Task Completed

💰 Reward: ৳{reward}

🏦 Balance: ৳{users[user_id]['balance']}
"""
    )

# ================= BALANCE =================

@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def balance(message):

    user_id = str(message.from_user.id)

    bal = users[user_id]["balance"]

    ref = users[user_id]["referrals"]

    bot.send_message(
        message.chat.id,
        f"""
💰 YOUR BALANCE

🏦 Balance: ৳{bal}

👥 Referrals: {ref}
"""
    )

# ================= REFER =================

@bot.message_handler(func=lambda m: m.text == "👥 Refer")
def refer(message):

    user_id = str(message.from_user.id)

    bot_username = bot.get_me().username

    link = f"https://t.me/{bot_username}?start={user_id}"

    bot.send_message(
        message.chat.id,
        f"""
👥 REFER & EARN

💰 Per Referral = ৳{REF_BONUS}

🔗 Your Referral Link:

{link}
"""
    )

# ================= LEADERBOARD =================

@bot.message_handler(func=lambda m: m.text == "🏆 Leaderboard")
def leaderboard(message):

    top = sorted(
        users.items(),
        key=lambda x: x[1]["balance"],
        reverse=True
    )

    text = "🏆 TOP USERS\n\n"

    num = 1

    for uid, data in top[:10]:

        text += f"{num}. {uid} — ৳{data['balance']}\n"

        num += 1

    bot.send_message(message.chat.id, text)

# ================= WITHDRAW =================

@bot.message_handler(func=lambda m: m.text == "💸 Withdraw")
def withdraw(message):

    user_id = str(message.from_user.id)

    balance = users[user_id]["balance"]

    if balance < MIN_WITHDRAW:

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