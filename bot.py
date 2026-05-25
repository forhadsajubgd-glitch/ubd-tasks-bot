import telebot
import sqlite3
from telebot.types import ReplyKeyboardMarkup

TOKEN = "8899354895:AAGDhY-1DT4vQIbcWpR4u2h7MS4radBeNA4"
ADMIN_ID = 7237976087  # আপনার Telegram ID

bot = telebot.TeleBot(TOKEN)

# ================= DATABASE =================

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    balance REAL DEFAULT 0,
    invited_by INTEGER
)
""")

conn.commit()

# ================= MENU =================

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row("📋 Tasks", "💰 Balance")
    markup.row("👥 Refer", "💸 Withdraw")

    return markup

# ================= START =================

@bot.message_handler(commands=['start'])
def start(message):

    user_id = message.chat.id
    args = message.text.split()

    ref = None

    if len(args) > 1:
        ref = args[1]

    cursor.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:

        invited_by = None

        if ref:
            invited_by = int(ref)

        cursor.execute(
            "INSERT INTO users(user_id, invited_by) VALUES(?,?)",
            (user_id, invited_by)
        )

        conn.commit()

        # REFERRAL BONUS
        if invited_by and invited_by != user_id:

            cursor.execute(
                "UPDATE users SET balance = balance + 2 WHERE user_id=?",
                (invited_by,)
            )

            conn.commit()

            bot.send_message(
                invited_by,
                "🎉 New referral joined!\n💵 You earned ৳2"
            )

    text = """
👋 Welcome To UBD TASKS

💵 Earn Money By Completing Tasks

✅ Channel Join
✅ Bot Join
✅ Refer Friends

💰 Every Task Reward = ৳2
"""

    bot.send_message(
        user_id,
        text,
        reply_markup=main_menu()
    )

# ================= TASKS =================

@bot.message_handler(func=lambda m: m.text == "📋 Tasks")
def tasks(message):

    text = """
📋 AVAILABLE TASKS

1️⃣ Join Main Channel — ৳2
https://t.me/remembermefrnd

2️⃣ Join Easy Income Bot — ৳2
https://t.me/FoxiGrowbot?start=ref_7237976087

3️⃣ Join Update Channel — ৳2
https://t.me/UBDTG_Earn_Bot

4️⃣ Refer Friend — ৳2
"""

    bot.send_message(message.chat.id, text)

# ================= BALANCE =================

@bot.message_handler(func=lambda m: m.text == "💰 Balance")
def balance(message):

    cursor.execute(
        "SELECT balance FROM users WHERE user_id=?",
        (message.chat.id,)
    )

    bal = cursor.fetchone()[0]

    bot.send_message(
        message.chat.id,
        f"💰 Your Balance: ৳{bal}"
    )

# ================= REFER =================

@bot.message_handler(func=lambda m: m.text == "👥 Refer")
def refer(message):

    username = bot.get_me().username

    link = f"https://t.me/{username}?start={message.chat.id}"

    text = f"""
👥 Invite Your Friends

💵 Earn ৳2 Per Referral

🔗 Your Link:
{link}
"""

    bot.send_message(message.chat.id, text)

# ================= WITHDRAW =================

@bot.message_handler(func=lambda m: m.text == "💸 Withdraw")
def withdraw(message):

    cursor.execute(
        "SELECT balance FROM users WHERE user_id=?",
        (message.chat.id,)
    )

    bal = cursor.fetchone()[0]

    if bal < 10:

        bot.send_message(
            message.chat.id,
            "❌ Minimum Withdraw = ৳10"
        )

    else:

        bot.send_message(
            message.chat.id,
            "💳 Send Your Bkash/Nagad Number"
        )

        bot.register_next_step_handler(
            message,
            process_number
        )

def process_number(message):

    number = message.text

    cursor.execute(
        "SELECT balance FROM users WHERE user_id=?",
        (message.chat.id,)
    )

    bal = cursor.fetchone()[0]

    admin_text = f"""
💸 NEW WITHDRAW REQUEST

👤 User: {message.chat.id}
💵 Amount: ৳{bal}
📱 Number: {number}
"""

    bot.send_message(ADMIN_ID, admin_text)

    cursor.execute(
        "UPDATE users SET balance = 0 WHERE user_id=?",
        (message.chat.id,)
    )

    conn.commit()

    bot.send_message(
        message.chat.id,
        "✅ Withdraw Request Sent"
    )

# ================= ADMIN =================

@bot.message_handler(commands=['broadcast'])
def broadcast(message):

    if message.chat.id != ADMIN_ID:
        return

    msg = message.text.replace("/broadcast ", "")

    cursor.execute("SELECT user_id FROM users")

    users = cursor.fetchall()

    sent = 0

    for user in users:

        try:
            bot.send_message(user[0], msg)
            sent += 1

        except:
            pass

    bot.send_message(
        ADMIN_ID,
        f"✅ Broadcast Sent To {sent} Users"
    )

print("BOT RUNNING...")

bot.infinity_polling()