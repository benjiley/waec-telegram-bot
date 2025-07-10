import telebot from telebot import types import random

bot = telebot.TeleBot("8092089557:AAFU69n7rcDEuSb92_rwb_OBJAbIJlf6roo")

Store user info and quiz state

user_data = {} quiz_state = {}

Sample questions

questions = [ { "question": "What is the capital of Nigeria?", "options": ["Accra", "Nairobi", "Abuja", "Lagos"], "answer": "c" }, { "question": "Simplify: 2(3x - 4) = ?", "options": ["6x - 4", "6x - 8", "5x - 2", "3x - 4"], "answer": "b" }, { "question": "Which gas do plants use for photosynthesis?", "options": ["Oxygen", "Hydrogen", "Carbon Dioxide", "Nitrogen"], "answer": "c" } ]

Sample lectures

lectures = { "Math": "\ud83d\udcd8 Math - BODMAS Rule\n\nWhen solving expressions like 2 + 3 \u00d7 4, remember:\n\nBODMAS = Brackets, Orders (powers), Division, Multiplication, Addition, Subtraction.\n\nSo: 2 + 3 \u00d7 4 = 2 + 12 = 14", "English": "\ud83d\udcd8 English - Parts of Speech\n\nThere are 8 parts of speech: noun, pronoun, verb, adjective, adverb, preposition, conjunction, interjection.", "Biology": "\ud83d\udcd8 Biology - Photosynthesis\n\nPhotosynthesis is the process by which green plants make their food using sunlight, carbon dioxide, and water." }

Start command with menu

def main_menu(chat_id): markup = types.ReplyKeyboardMarkup(resize_keyboard=True) markup.row("📝 Register", "📚 Take Quiz") markup.row("🎓 Take Lecture", "📄 My Info") bot.send_message(chat_id, "Choose an option:", reply_markup=markup)

@bot.message_handler(commands=['start']) def start(message): chat_id = message.chat.id main_menu(chat_id) bot.send_message(chat_id, "\ud83d\udc4b Welcome to WAEC Tutorial Bot!")

Registration flow

@bot.message_handler(func=lambda m: m.text == "📝 Register") def register(message): chat_id = message.chat.id user_data[chat_id] = {"step": "name"} bot.send_message(chat_id, "What is your full name?")

Quiz command

@bot.message_handler(func=lambda m: m.text == "📚 Take Quiz") def quiz(message): chat_id = message.chat.id question = random.choice(questions) quiz_state[chat_id] = question q_text = f"\ud83d\udcd6 Quiz Time!\n\n{question['question']}\n" q_text += f"(a) {question['options'][0]}\n(b) {question['options'][1]}\n(c) {question['options'][2]}\n(d) {question['options'][3]}\n\nReply with a/b/c/d" bot.send_message(chat_id, q_text, parse_mode='Markdown')

Lecture command

@bot.message_handler(func=lambda m: m.text == "🎓 Take Lecture") def send_lecture_menu(message): chat_id = message.chat.id markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) for subject in lectures: markup.add(subject) bot.send_message(chat_id, "Choose a subject:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in lectures.keys()) def lecture_content(message): chat_id = message.chat.id subject = message.text bot.send_message(chat_id, lectures[subject], parse_mode="Markdown") main_menu(chat_id)

My Info

@bot.message_handler(func=lambda m: m.text == "📄 My Info") def my_info(message): chat_id = message.chat.id data = user_data.get(chat_id) if data and "name" in data: name = data.get("name", "

