import os
import random
from dotenv import load_dotenv
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import time

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

games = {}

class Game:
    def __init__(self, chat_id, difficulty):
        self.chat_id = chat_id
        self.lives = 10
        self.score = 0
        self.level = 1
        self.total_questions = 0
        self.difficulty = difficulty
        self.hints_used = 0
        self.question_start_time = None

def generate_question(level, difficulty):
    ops = ['+', '-', '*']
    if difficulty == 'easy':
        a, b = random.randint(1, 5 * level), random.randint(1, 5 * level)
        op = random.choice(['+', '*'])
    elif difficulty == 'medium':
        a, b = random.randint(5 * level, 10 * level), random.randint(5 * level, 10 * level)
    else:
        a, b = random.randint(10 * level, 15 * level), random.randint(10 * level, 15 * level)
        op = random.choice(ops)
    question = f"{a} {op} {b}"
    answer = eval(question)
    if op == '/':
        a = a * b
        question = f"{a} {op} {b}"
    return question, answer

def update_game_message(chat_id):
    game = games[chat_id]
    heart_emoji = '❤️'
    empty_heart_emoji = '🤍'
    hint_emoji = '🔍'
    used_hint_emoji = '❌'
    lives_text = f"Жизни: {heart_emoji * game.lives}{empty_heart_emoji * (10 - game.lives)}"
    hints_text = f"Подсказки: {hint_emoji * (3 - game.hints_used)}{used_hint_emoji * game.hints_used}"
    message = f"{lives_text}\n{hints_text}\n🌟 Очки: {game.score}"
    return message

def create_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("Новая игра", callback_data='/start'), 
                 InlineKeyboardButton("Подсказка", callback_data='/hint'))
    return keyboard

@bot.message_handler(commands=['start'])
def start_game(message):
    chat_id = message.chat.id
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Легкий", callback_data='easy'))
    keyboard.add(InlineKeyboardButton("Средний", callback_data='medium'))
    keyboard.add(InlineKeyboardButton("Сложный", callback_data='hard'))
    bot.reply_to(message, "Выберите уровень сложности:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['easy', 'medium', 'hard'])
def set_difficulty(call):
    chat_id = call.message.chat.id
    difficulty = call.data
    games[chat_id] = Game(chat_id, difficulty)
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=f"Вы выбрали {difficulty} уровень сложности.")
    rules = "🔢 Добро пожаловать в арифметическую игру! 🎮\n\n📜 Правила:\n- У вас есть 10 жизней (❤️).\n- Вам будут даваться случайные примеры по арифметике.\n- Сложность примеров будет постепенно увеличиваться.\n- За каждый правильный ответ вы получаете очки (🌟). Чем быстрее вы отвечаете, тем больше очков получаете.\n- Если вы ошибаетесь или не отвечаете в течение 12 секунд, то теряете жизнь (❤️).\n- Игра заканчивается, когда у вас заканчиваются жизни.\n- У вас есть 3 подсказки (🔍), которые вы можете использовать."
    start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    start_keyboard.add(KeyboardButton("Начать игру"))
    bot.send_message(chat_id, rules, reply_markup=start_keyboard)

def send_question(chat_id):
    game = games[chat_id]
    question, answer = generate_question(game.level, game.difficulty)
    game.current_answer = answer
    game.total_questions += 1
    game.question_start_time = time.time()
    bot.send_message(chat_id, f"❓ Вопрос {game.total_questions}:\n{question}", reply_markup=ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: message.text == "Начать игру")
def start_game_questions(message):
    chat_id = message.chat.id
    if chat_id not in games:
        bot.reply_to(message, "Пожалуйста, выберите уровень сложности с помощью команды /start", reply_markup=ReplyKeyboardRemove())
        return
    send_question(chat_id)

def check_answer(message):
    chat_id = message.chat.id
    if chat_id not in games:
        bot.reply_to(message, "Пожалуйста, начните новую игру с помощью команды /start", reply_markup=create_keyboard())
        return
    game = games[chat_id]
    answer_time = time.time() - game.question_start_time
    
    try:
        user_answer = int(message.text)
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите целочисленный ответ.", reply_markup=create_keyboard())
        return

    if answer_time > 12 or user_answer != game.current_answer:
        game.lives -= 1
        if game.lives == 0:
            message_text = "❌ К сожалению, у вас закончились жизни. Игра окончена.\n\n"
            message_text += f"📊 Итоговая статистика:\n\n🌟 Очки: {game.score}"
            bot.send_message(chat_id, message_text, reply_markup=create_keyboard())
            del games[chat_id]
        else:
            if answer_time > 12:
                answer_correct = "❌ Вы не ответили вовремя и теряете жизнь."
            else:
                answer_correct = "❌ Неверно. Вы теряете жизнь."
            
            message_text = f"{answer_correct}\nПравильный ответ: {game.current_answer}\n\n"
            message_text += update_game_message(chat_id)
            bot.send_message(chat_id, message_text, reply_markup=create_keyboard())
            send_question(chat_id)
    else:
        score_multiplier = max(1, int(12 - answer_time))
        game.score += game.level * 10 * score_multiplier
        if game.total_questions % 5 == 0:
            game.level += 1
        message_text = f"✅ Правильно! Вы получаете {game.level * 10 * score_multiplier} очков.\n\n"
        message_text += update_game_message(chat_id)
        bot.send_message(chat_id, message_text, reply_markup=create_keyboard())
        send_question(chat_id)

@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    check_answer(message)

@bot.callback_query_handler(func=lambda call: call.data == '/start')
def start_new_game(call):
    start_game(call.message)

@bot.callback_query_handler(func=lambda call: call.data == '/hint')
def hint_callback(call):
    chat_id = call.message.chat.id
    if chat_id not in games:
        bot.answer_callback_query(callback_query_id=call.id, text="Пожалуйста, начните новую игру с помощью команды /start")
        return
    game = games[chat_id]
    if game.hints_used < 3:
        game.hints_used += 1
        bot.answer_callback_query(callback_query_id=call.id, text=f"Подсказка: {game.current_answer}")
    else:
        bot.answer_callback_query(callback_query_id=call.id, text="У вас больше нет подсказок.")

bot.polling()