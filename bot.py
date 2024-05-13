import os
import random
from dotenv import load_dotenv
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
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
        self.correct_streak = 0  # добавляем счетчик правильных ответов подряд

def generate_question(level, difficulty):
    if difficulty == 'easy':
        if level == 1:
            a, b = random.randint(0, 9), random.randint(0, 9)
            question = f"{a} + {b}"
        elif level == 2:
            a, b = random.randint(0, 9), random.randint(0, 9)
            while b > a:
                a, b = random.randint(0, 9), random.randint(0, 9)
            question = f"{a} - {b}"
        elif level == 3:
            a, b = random.randint(10, 20), random.randint(0, 9)
            while (a % 10 + b) >= 10:
                a, b = random.randint(10, 20), random.randint(0, 9)
            question = f"{a} + {b}"
        elif level == 4:
            a, b = random.randint(10, 20), random.randint(0, 9)
            while (a % 10 - b) < 0:
                a, b = random.randint(10, 20), random.randint(0, 9)
            question = f"{a} - {b}"
        elif level == 5:
            a, b = random.randint(10, 20), random.randint(0, 9)
            question = f"{a} + {b}"
        elif level == 6:
            a, b = random.randint(10, 20), random.randint(0, 9)
            question = f"{a} - {b}"
        elif level == 7:
            a, b = random.randint(1, 5), random.randint(1, 5)
            question = f"{a} * {b}"
        elif level == 8:
            a, b = random.randint(1, 5), random.randint(1, 5)
            question = f"{a * b} / {b}"
        elif level == 9:
            a, b = random.randint(10, 50), random.randint(10, 50)
            while (a % 10 + b % 10) >= 10:
                a, b = random.randint(10, 50), random.randint(10, 50)
            question = f"{a} + {b}"
        elif level == 10:
            a, b = random.randint(20, 50), random.randint(10, 20)
            while (a % 10 - b % 10) < 0:
                a, b = random.randint(20, 50), random.randint(10, 20)
            question = f"{a} - {b}"
        elif level == 11:
            a, b = random.randint(20, 50), random.randint(10, 50)
            question = f"{a} + {b}"
        elif level == 12:
            a, b = random.randint(30, 70), random.randint(10, 50)
            question = f"{a} - {b}"
        elif level == 13:
            a, b = random.randint(1, 9), random.randint(1, 9)
            question = f"{a} * {b}"
        elif level == 14:
            a, b = random.randint(1, 9), random.randint(1, 9)
            question = f"{a * b} / {b}"
        elif level == 15:
            a, b, c = random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)
            question = f"{a} + {b} + {c}"
    elif difficulty == 'medium':
        if level == 10:
            a, b = random.randint(20, 50), random.randint(10, 20)
            while (a % 10 - b % 10) < 0:
                a, b = random.randint(20, 50), random.randint(10, 20)
            question = f"{a} - {b}"
        elif level == 11:
            a, b = random.randint(20, 50), random.randint(10, 50)
            question = f"{a} + {b}"
        elif level == 12:
            a, b = random.randint(30, 70), random.randint(10, 50)
            question = f"{a} - {b}"
        elif level == 13:
            a, b = random.randint(1, 9), random.randint(1, 9)
            question = f"{a} * {b}"
        elif level == 14:
            a, b = random.randint(1, 9), random.randint(1, 9)
            question = f"{a * b} / {b}"
        elif level == 15:
            a, b, c = random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)
            question = f"{a} + {b} + {c}"
        elif level == 16:
            a, b = random.randint(10, 20), random.randint(0, 9)
            question = f"{a} + {b}"
        elif level == 17:
            a, b = random.randint(10, 20), random.randint(0, 9)
            question = f"{a} - {b}"
        elif level == 18:
            a, b = random.randint(10, 20), random.randint(1, 9)
            question = f"{a} * {b}"
        elif level == 19:
            a, b = random.randint(10, 50), random.randint(1, 9)
            while a % b != 0:
                a, b = random.randint(10, 50), random.randint(1, 9)
            question = f"{a} / {b}"
        elif level == 20:
            a, b = random.randint(0, 50), random.randint(0, 50)
            question = f"{a} + {b}"
        elif level == 21:
            a, b = random.randint(0, 50), random.randint(0, 50)
            while b > a:
                a, b = random.randint(0, 50), random.randint(0, 50)
            question = f"{a} - {b}"
        elif level == 22:
            a, b, c = random.randint(10, 20), random.randint(10, 20), random.randint(10, 20)
            question = f"{a} + {b} + {c}"
        elif level == 23:
            a, b, c = random.randint(10, 20), random.randint(10, 20), random.randint(10, 20)
            question = f"{a} - {b} + {c}"
        elif level == 24:
            a, b, c = random.randint(10, 30), random.randint(10, 20), random.randint(0, 10)
            question = f"{a} + {b} - {c}"
        elif level == 25:
            a, b = random.randint(0, 10), random.randint(0, 10)
            question = f"{a} * {b}"
    else:  # difficulty == 'hard'
        if level == 20:
            a, b = random.randint(0, 50), random.randint(0, 50)
            question = f"{a} + {b}"
        elif level == 21:
            a, b = random.randint(0, 50), random.randint(0, 50)
            while b > a:
                a, b = random.randint(0, 50), random.randint(0, 50)
            question = f"{a} - {b}"
        elif level == 22:
            a, b, c = random.randint(10, 20), random.randint(10, 20), random.randint(10, 20)
            question = f"{a} + {b} + {c}"
        elif level == 23:
            a, b, c = random.randint(10, 20), random.randint(10, 20), random.randint(10, 20)
            question = f"{a} - {b} + {c}"
        elif level == 24:
            a, b, c = random.randint(10, 30), random.randint(10, 20), random.randint(0, 10)
            question = f"{a} + {b} - {c}"
        elif level == 25:
            a, b = random.randint(0, 10), random.randint(0, 10)
            question = f"{a} * {b}"
        elif level == 26:
            a, b = random.randint(1, 10), random.randint(1, 10)
            while a % b != 0:
                a, b = random.randint(1, 10), random.randint(1, 10)
            question = f"{a} / {b}"
        elif level == 27:
            a, b = random.randint(0, 100), random.randint(0, 100)
            question = f"{a} + {b}"
        elif level == 28:
            a, b = random.randint(0, 100), random.randint(0, 100)
            while b > a:
                a, b = random.randint(0, 100), random.randint(0, 100)
            question = f"{a} - {b}"
        elif level == 29:
            a, b = random.randint(1, 20), random.randint(1, 20)
            question = f"{a} * {b}"
        elif level == 30:
            a, b = random.randint(1, 20), random.randint(1, 20)
            while a % b != 0:
                a, b = random.randint(1, 20), random.randint(1, 20)
            question = f"{a} / {b}"
        elif level == 31:
            a, b, c = random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)
            question = f"{a} + {b} - {c}"
        elif level == 32:
            a, b = random.randint(10, 20), random.randint(10, 20)
            question = f"{a} * {b}"
        elif level == 33:
            a, b = random.randint(10, 100), random.randint(10, 100)
            while a % b != 0:
                a, b = random.randint(10, 100), random.randint(10, 100)
            question = f"{a} / {b}"
        elif level == 34:
            a, b = random.randint(100, 999), random.randint(1, 9)
            question = f"{a} * {b}"
        elif level == 35:
            a, b = random.randint(100, 999), random.randint(1, 9)
            while a % b != 0:
                a, b = random.randint(100, 999), random.randint(1, 9)
            question = f"{a} / {b}"

    answer = eval(question)
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
    rules = "🔢 Добро пожаловать в арифметическую игру! 🎮\n\n📜 Правила:\n- У вас есть 10 жизней (❤️).\n- Вам будут даваться случайные примеры по арифметике.\n- Сложность примеров будет постепенно увеличиваться.\n- За каждый правильный ответ вы получаете очки (🌟). Чем быстрее вы отвечаете, тем больше очков получаете.\n- Если вы ошибаетесь или не отвечаете в течение 12 секунд, то теряете жизнь (❤️).\n- Игра заканчивается, когда у вас заканчиваются жизни.\n- У вас есть 3 подсказки (💡), которые вы можете использовать."
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Начать игру", callback_data='start_game'))
    bot.send_message(chat_id, rules, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'start_game')
def start_game_questions(call):
    chat_id = call.message.chat.id
    if chat_id not in games:
        bot.answer_callback_query(callback_query_id=call.id, text="Пожалуйста, выберите уровень сложности с помощью команды /start")
        return
    question, answer = generate_question(games[chat_id].level, games[chat_id].difficulty)
    games[chat_id].current_answer = answer
    games[chat_id].total_questions += 1
    games[chat_id].question_start_time = time.time()
    bot.send_message(chat_id, f"❓ Вопрос {games[chat_id].total_questions}:\n{question}", reply_markup=ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: True)
def check_answer(message):
    chat_id = message.chat.id
    if chat_id not in games:
        bot.reply_to(message, "Пожалуйста, начните новую игру с помощью команды /start", reply_markup=create_keyboard())
        return
    game = games[chat_id]
    answer_time = time.time() - game.question_start_time
    if answer_time > 12:
        game.lives -= 1
        game.correct_streak = 0  # сбрасываем счетчик правильных ответов подряд при ошибке или пропуске
        if game.lives == 0:
            message_text = "❌ К сожалению, у вас закончились жизни. Игра окончена.\n\n"
            message_text += f"📊 Итоговая статистика:\n\n🌟 Очки: {game.score}"
            bot.send_message(chat_id, message_text, reply_markup=create_keyboard())
            del games[chat_id]
        else:
            try:
                user_answer = int(message.text)
                if user_answer == game.current_answer:
                    answer_correct = "✅ Ваш ответ был правильным, но время истекло."
                else:
                    answer_correct = "❌ Ваш ответ был неверным, и время истекло."
            except ValueError:
                answer_correct = "❌ Вы не ввели целочисленный ответ, и время истекло."
            
            message_text = f"{answer_correct} Вы теряете жизнь.\n\nПравильный ответ: {game.current_answer}\n\n"
            message_text += update_game_message(chat_id)
            bot.send_message(chat_id, message_text, reply_markup=create_keyboard())
            question, answer = generate_question(game.level, game.difficulty)
            game.current_answer = answer
            game.total_questions += 1
            game.question_start_time = time.time()
            bot.send_message(chat_id, f"❓ Вопрос {game.total_questions}:\n{question}", reply_markup=ReplyKeyboardRemove())
    else:
        try:
            user_answer = int(message.text)
        except ValueError:
            bot.reply_to(message, "Пожалуйста, введите целочисленный ответ.", reply_markup=create_keyboard())
            return
        if user_answer == game.current_answer:
            game.correct_streak += 1
            if game.correct_streak == 3:
                game.level += 1
                game.correct_streak = 0  # сбрасываем счетчик после перехода на следующий уровень
            score_multiplier = max(1, int(12 - answer_time))
            game.score += game.level * 10 * score_multiplier
            message_text = f"✅ Правильно! Вы получаете {game.level * 10 * score_multiplier} очков.\n\n"
            message_text += update_game_message(chat_id)
            bot.send_message(chat_id, message_text, reply_markup=create_keyboard())
            question, answer = generate_question(game.level, game.difficulty)
            game.current_answer = answer
            game.total_questions += 1
            game.question_start_time = time.time()
            bot.send_message(chat_id, f"❓ Вопрос {game.total_questions}:\n{question}", reply_markup=ReplyKeyboardRemove())
        else:
            game.lives -= 1
            game.correct_streak = 0  # сбрасываем счетчик правильных ответов подряд при ошибке
            if game.lives == 0:
                message_text = "❌ К сожалению, у вас закончились жизни. Игра окончена.\n\n"
                message_text += f"📊 Итоговая статистика:\n\n🌟 Очки: {game.score}"
                bot.send_message(chat_id, message_text, reply_markup=create_keyboard())
                del games[chat_id]
            else:
                message_text = f"❌ Неверно. Правильный ответ: {game.current_answer}. Вы теряете жизнь.\n\n"
                message_text += update_game_message(chat_id)
                bot.send_message(chat_id, message_text, reply_markup=create_keyboard())
                question, answer = generate_question(game.level, game.difficulty)
                game.current_answer = answer
                game.total_questions += 1
                game.question_start_time = time.time()
                bot.send_message(chat_id, f"❓ Вопрос {game.total_questions}:\n{question}", reply_markup=ReplyKeyboardRemove())

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

def hint_handler(message):
    chat_id = message.chat.id
    if chat_id not in games:
        bot.reply_to(message, "Пожалуйста, начните новую игру с помощью команды /start")
        return
    hint_callback(message)

@bot.message_handler(commands=['hint'])
def handle_hint_command(message):
    hint_handler(message)

bot.polling()
