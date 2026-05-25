import telebot
from telebot.types import *
import json
import os

# ================== CONFIG ==================

TOKEN = "8899354895:AAGDhY-1DT4vQIbcWpR4u2h7MS4radBeNA4"

# ===== CHANNEL USERNAME =====

CHANNEL_1_USERNAME = "@remembermefrnd"
CHANNEL_2_USERNAME = "@UBDTG_Earn_Bot"
CHANNEL_3_USERNAME = "@lotsofincome"

# ===== CHANNEL LINK =====

CHANNEL_1 = "https://t.me/remembermefrnd"
CHANNEL_2 = "https://t.me/UBDTG_Earn_Bot"
CHANNEL_3 = "https://t.me/lotsofincome"

# ===== BOT LINKS =====

BOT_1 = "https://t.me/FoxiGrowbot?start=ref_7237976087"
BOT_2 = "https://t.me/GmailFarmerBot?start=7237976087"

# ===== YOUTUBE =====

YOUTUBE = "https://youtube.com/@ultrabd"

# ===== SETTINGS =====

REF_BONUS = 4
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
            "verified": False
        }

        # ===== REFERRAL BONUS =====

        if len(args) > 1:

            referrer = args[1]

            if (
                referrer != user_id
                and referrer in users
                and users[user_id]["verified"] == False
            ):

                users[referrer]["balance"] += REF_BONUS

                users[referrer]["referrals"] += 1

                bot.send_message(
                    referrer,
                    f"🎉 New Referral Joined!\n💰 +৳{REF_BONUS}"
                )

        save_users()

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row("📋 Tasks", "💰 Balance")

    markup.row("👥 Refer", "💸 Withdraw")

    bot.send_message(
        message.chat.id,
        f"""
👋 Welcome To UBD TASKS

📢 Complete All Tasks First

💰 Referral Bonus = ৳{REF_BONUS}

💸 Minimum Withdraw = ৳{MIN_WITHDRAW}
""",
        reply_markup=markup
    )

# ================= TASKS =================

@bot.message_handler(func=lambda m: m.text == "📋 Tasks")
def tasks(message):

    markup = InlineKeyboardMarkup()

    # ===== CHANNELS =====

    markup.add(
        InlineKeyboardButton(
            "📢 Join Channel 1",
            url=CHANNEL_1
        )
    )

    markup.add(
        InlineKeyboardButton(
            "📢 Join Channel 2",
            url=CHANNEL_2
        )
    )

    markup.add(
        InlineKeyboardButton(
            "📢 Join Channel 3",
            url=CHANNEL_3
        )
    )

    # ===== BOTS =====

    markup.add(
        InlineKeyboardButton(
            "🤖 Join Bot 1",
            url=BOT_1
        )
    )

    markup.add(
        InlineKeyboardButton(
            "🤖 Join Bot 2",
            url=BOT_2
        )
    )

    # ===== YOUTUBE =====

    markup.add(
        InlineKeyboardButton(
            "▶️ Subscribe YouTube",
            url=YOUTUBE
        )
    )

    # ===== VERIFY BUTTON =====

    markup.add(
        InlineKeyboardButton(
            "✅ Verify All",
            callback_data="verify_all"
        )
    )

    bot.send_message(
        message.chat.id,
        "📋 Complete All Tasks Then Click Verify:",
        reply_markup=markup
    )

# ================= VERIFY =================

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    user_id = str(call.from_user.id)

    try:

        # ===== CHANNEL CHECK =====

        ch1 = bot.get_chat_member(
            CHANNEL_1_USERNAME,
            user_id
        )

        ch2 = bot.get_chat_member(
            CHANNEL_2_USERNAME,
            user_id
        )

        ch3 = bot.get_chat_member(
            CHANNEL_3_USERNAME,
            user_id
        )

        ok1 = ch1.status in [
            "member",
            "administrator",
            "creator"
        ]

        ok2 = ch2.status in [
            "member",
            "administrator",
            "creator"
        ]

        ok3 = ch3.status in [
            "member",
            "administrator",
            "creator"
        ]

        # ===== VERIFIED =====

        if ok1 and ok2 and ok3:

            users[user_id]["verified"] = True

            save_users()

            bot.answer_callback_query(
                call.id,
                "✅ Verification Successful"
            )

            bot.send_message(
                call.message.chat.id,
                """
🎉 Verification Successful!

✅ All Channels Joined
"""
            )

        else:

            bot.answer_callback_query(
                call.id,
                "❌ Join All Channels First"
            )

    except:

        bot.answer_callback_query(
            call.id,
            "❌ Verification Failed"
        )

# ================= BALANCE =================

@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def balance(message):

    user_id = str(message.from_user.id)

    balance = users[user_id]["balance"]

    refs = users[user_id]["referrals"]

    bot.send_message(
        message.chat.id,
        f"""
💰 YOUR ACCOUNT

🏦 Balance: ৳{balance}

👥 Referrals: {refs}
"""
    )

# ================= REFER =================

@bot.message_handler(func=lambda m: m.text == "👥 Refer")
def refer(message):

    user_id = str(message.from_user.id)

    if users[user_id]["verified"] == False:

        bot.send_message(
            message.chat.id,
            "❌ First Complete Verification"
        )

        return

    username = bot.get_me().username

    ref_link = f"https://t.me/{username}?start={user_id}"

    bot.send_message(
        message.chat.id,
        f"""
👥 REFER & EARN

💰 Per Referral = ৳{REF_BONUS}

🔗 Your Referral Link:

{ref_link}
"""
    )

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
        """
💳 Send Your Bkash/Nagad Number

Admin Will Review Your Withdraw Request.
"""
    )

# ================= RUN =================

print("Bot Running...")

bot.infinity_polling()