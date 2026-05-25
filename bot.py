import telebot
from telebot import types

TOKEN = "8899354895:AAGDhY-1DT4vQIbcWpR4u2h7MS4radBeNA4"

bot = telebot.TeleBot(TOKEN)

users = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if user_id not in users:
        users[user_id] = {
            "balance": 0,
            "referrals": 0
        }

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📋 Tasks", "💰 Balance")
    markup.add("👥 Refer", "🏆 Leaderboard")
    markup.add("💸 Withdraw")

    bot.send_message(
        message.chat.id,
        f"🎉 Welcome {message.from_user.first_name} to UBD TASKS!\n\nEarn rewards by completing tasks.",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: True)
def menu(message):

    user_id = message.from_user.id

    if message.text == "📋 Tasks":
        bot.send_message(message.chat.id,
        "✅ Join Telegram Channel\n✅ Watch Ads\n✅ Invite Friends")

    elif message.text == "💰 Balance":
        balance = users[user_id]["balance"]
        bot.send_message(message.chat.id,
        f"💰 Your Balance: {balance} coins")

    elif message.text == "👥 Refer":
        ref_link = f"https://t.me/ubdtasksbot?start={user_id}"

        bot.send_message(message.chat.id,
        f"👥 Invite friends using your link:\n{ref_link}")

    elif message.text == "🏆 Leaderboard":
        bot.send_message(message.chat.id,
        "🏆 Top Users Coming Soon")

    elif message.text == "💸 Withdraw":
        bot.send_message(message.chat.id,
        "💸 Minimum withdraw: 100 coins")

bot.infinity_polling()