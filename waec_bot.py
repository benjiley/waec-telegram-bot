import telebot
from telebot import types

bot = telebot.TeleBot("8092089557:AAFU69n7rcDEuSb92_rwb_OBJAbIJlf6roo")

# Dictionary to track users and store data
user_data = {}

# Start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'step': 'name'}
    bot.send_message(chat_id, "Welcome to WAEC Tutorial Bot!\nWhat is your full name?")

# General message handler
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    chat_id = message.chat.id
    text = message.text

    # If user hasn't started the flow
    if chat_id not in user_data:
        bot.send_message(chat_id, "Please type /start to begin.")
        return

    step = user_data[chat_id].get('step')

    if step == 'name':
        user_data[chat_id]['name'] = text
        user_data[chat_id]['step'] = 'class'

        # Ask for class using buttons
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("SS1", "SS2", "SS3")
        bot.send_message(chat_id, "Which class are you in?", reply_markup=markup)

    elif step == 'class':
        user_data[chat_id]['class'] = text
        user_data[chat_id]['step'] = 'subjects'
        bot.send_message(chat_id, "List your subjects of interest (separated by commas).\nExample: Math, English, Chemistry")

    elif step == 'subjects':
        user_data[chat_id]['subjects'] = text
        user_data[chat_id]['step'] = 'done'

        # Show confirmation
        name = user_data[chat_id]['name']
        level = user_data[chat_id]['class']
        subjects = user_data[chat_id]['subjects']

        bot.send_message(chat_id, f"✅ Registration complete!\n\n👤 Name: {name}\n🏫 Class: {level}\n📚 Subjects: {subjects}")

    else:
        bot.send_message(chat_id, "You're already registered. Type /start to restart or update your info.")

# Start the bot
bot.polling()
