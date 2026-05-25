import telebot
from telebot.types import ReplyKeyboardMarkup
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

    # CREATE USER
    if user_id not in users:

        users[user_id] = {
            "balance": 0,
            "referrals": 0
        }

        # REFERRAL BONUS
        if len(args) > 1:

            referrer = args[1]

            if referrer != user_id and referrer in users:

                users[referrer]["balance"] += REF_BONUS
                users[referrer]["referrals"] += 1

                save_users()

                bot.send_message(
                    referrer,
                    f"🎉 New Referral Joined!\n💰 Earned ৳{REF_BONUS}"
                )

        save_users()

    # MENU
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row("📋 Tasks", "💰 Balance")
    markup.row("👥 Refer", "🏆 Leaderboard")
    markup.row("💸 Withdraw")

    bot.send_message(
        message.chat.id,
        f"""
👋 Welcome To UBD TASKS BOT

💵 Earn Money By:

✅ Joining Channels
✅ Joining Bots
✅ Watching YouTube

👥 Refer Friends & Earn ৳{REF_BONUS}
""",
        reply_markup=markup
    )

# ================= TASKS =================

@bot.message_handler(func=lambda m: m.text == "📋 Tasks")
def tasks(message):

    text = f"""
📋 AVAILABLE TASKS

1️⃣ Join Telegram Channel — ৳2
{CHANNEL_1}

2️⃣ Join Telegram Channel — ৳2
{CHANNEL_2}

3️⃣ Join Telegram Channel — ৳2
{CHANNEL_3}

4️⃣ Join Telegram Bot — ৳2
{BOT_1}

5️⃣ Join Telegram Bot — ৳2
{BOT_2}

6️⃣ Subscribe YouTube Channel — ৳2
{YOUTUBE}

✅ After Completing Tasks
Contact Admin For Manual Verification
"""

    bot.send_message(message.chat.id, text)

# ================= BALANCE =================

@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def balance(message):

    user_id = str(message.from_user.id)

    if user_id not in users:

        users[user_id] = {
            "balance": 0,
            "referrals": 0
        }

        save_users()

    bal = users[user_id]["balance"]

    refs = users[user_id]["referrals"]

    bot.send_message(
        message.chat.id,
        f"""
💰 YOUR BALANCE

💵 Balance: ৳{bal}

👥 Referrals: {refs}
"""
    )

# ================= REFER =================

@bot.message_handler(func=lambda m: m.text == "👥 Refer")
def refer(message):

    user_id = message.from_user.id

    bot_username = bot.get_me().username

    link = f"https://t.me/{bot_username}?start={user_id}"

    bot.send_message(
        message.chat.id,
        f"""
👥 REFER & EARN

💰 Earn ৳{REF_BONUS} Per Referral

🔗 Your Referral Link:

{link}
"""
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
            f"❌ Minimum Withdraw Is ৳{MIN_WITHDRAW}"
        )

    else:

        msg = bot.send_message(
            message.chat.id,
            "📲 Send Your Bkash/Nagad Number"
        )

        bot.register_next_step_handler(msg, process_number)

# ================= PROCESS NUMBER =================

def process_number(message):

    number = message.text

    user_id = str(message.from_user.id)

    bal = users[user_id]["balance"]

    bot.send_message(
        ADMIN_ID,
        f"""
💸 NEW WITHDRAW REQUEST

👤 Name: {message.from_user.first_name}

🆔 User ID: {user_id}

💰 Amount: ৳{bal}

📲 Number: {number}
"""
    )

    users[user_id]["balance"] = 0

    save_users()

    bot.send_message(
        message.chat.id,
        "✅ Withdraw Request Submitted Successfully"
    )

# ================= ADMIN ADD BALANCE =================

@bot.message_handler(commands=['add'])
def add_balance(message):

    if message.from_user.id != ADMIN_ID:
        return

    try:

        cmd = message.text.split()

        user_id = cmd[1]

        amount = int(cmd[2])

        if user_id not in users:

            users[user_id] = {
                "balance": 0,
                "referrals": 0
            }

        users[user_id]["balance"] += amount

        save_users()

        bot.send_message(
            message.chat.id,
            f"✅ Added ৳{amount} To {user_id}"
        )

        bot.send_message(
            user_id,
            f"🎉 Admin Added ৳{amount} To Your Balance"
        )

    except:

        bot.send_message(
            message.chat.id,
            "Usage:\n/add USER_ID AMOUNT"
        )

# ================= BROADCAST =================

@bot.message_handler(commands=['broadcast'])
def broadcast(message):

    if message.from_user.id != ADMIN_ID:
        return

    text = message.text.replace("/broadcast ", "")

    total = 0

    for user_id in users:

        try:

            bot.send_message(user_id, text)

            total += 1

        except:
            pass

    bot.send_message(
        message.chat.id,
        f"✅ Broadcast Sent To {total} Users"
    )

# ================= RUN =================

print("Bot Running...")

bot.infinity_polling()