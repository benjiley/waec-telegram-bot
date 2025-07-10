import telebot
from telebot import types
import csv
import os

bot = telebot.TeleBot("PASTE_YOUR_TOKEN_HERE")

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'step': 'name'}
    bot.send_message(chat_id, "Welcome to WAEC Tutorial Bot!\nWhat is your full name?")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    chat_id = message.chat.id
    text = message.text

    if chat_id not in user_data:
        bot.send_message(chat_id, "Please type /start to begin registration.")
        return

    step = user_data[chat_id]['step']

    if step == 'name':
        user_data[chat_id]['name'] = text
        user_data[chat_id]['step'] = 'class'

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("SS1", "SS2", "SS3")
        bot.send_message(chat_id, "Which class are you in?", reply_markup=markup)

    elif step == 'class':
        user_data[chat_id]['class'] = text
        user_data[chat_id]['step'] = 'subjects'
        bot.send_message(chat_id, "List your subjects of interest (separated by commas).")

    elif step == 'subjects':
        user_data[chat_id]['subjects'] = text
        user_data[chat_id]['step'] = 'done'

        name = user_data[chat_id]['name']
        level = user_data[chat_id]['class']
        subjects = user_data[chat_id]['subjects']

        save_student_info(name, level, subjects)

        bot.send_message(chat_id, f"✅ Registration complete!\n\n👤 Name: {name}\n🏫 Class: {level}\n📚 Subjects: {subjects}")

    else:
        bot.send_message(chat_id, "You're already registered. Type /start to update your info.")

# Function to save student info to a CSV file
def save_student_info(name, student_class, subjects):
    file_exists = os.path.isfile("students.csv")

    with open("students.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Name", "Class", "Subjects"])
        writer.writerow([name, student_class, subjects])

# Start polling
bot.polling()
