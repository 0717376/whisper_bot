import os
import random
from dotenv import load_dotenv
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

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

def generate_question(level, difficulty):
    ops = ['+', '-', '*']
    if difficulty == 'easy':
        a, b = random.randint(1, 10), random.randint(1, 10)
    elif difficulty == 'medium':
        a, b = random.randint(10, 100), random.randint(10, 100)
    else:
        a, b = random.randint(100, 1000), random.randint(100, 1000)
    op = random.choice(ops)
    question = f"{a} {op} {b}"
    answer = eval(question)
    if op == '/' and a % b == 0:  # Ensure division is feasible
        question = f"{a} {op} {b}"
    else:  # If not feasible, regenerate question
        return generate_question(level, difficulty)
    return question, answer

def update_game_message(chat_id):
    game = games[chat_id]
    message = f"📊 Статистика игры:\n\n➡️ Вопрос: {game.total_questions}\n❤️ Жизни: {game.lives}\n🌟 Очки: {game.score}\n💡 Подсказки: {game.hints_used}/3"
    return message

def create_keyboard():
    keyboard = InlineKeyboardMarkup()
    # keyboard.add(InlineKeyboardButton("Новая игра", callback_data='/start'))
    # keyboard.add(InlineKeyboardButton("Правила и помощь", callback_data='/help'))
    # keyboard.add(InlineKeyboardButton("Подсказка", callback_data='/hint'))
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
    rules = "🔢 Добро пожаловать в арифметическую игру! 🎮\n\n📜 Правила:\n- У вас есть 10 жизней (❤️).\n- Вам будут даваться случайные примеры по арифметике.\n- Сложность примеров будет постепенно увеличиваться.\n- За каждый правильный ответ вы получаете очки (🌟).\n- Если вы ошибаетесь, то теряете жизнь (❤️).\n- Игра заканчивается, когда у вас заканчиваются жизни.\n- У вас есть 3 подсказки (💡), которые вы можете использовать.\n\nДавайте начнем! 😄"
    bot.send_message(chat_id, rules)
    ask_question(chat_id)

def ask_question(chat_id):
    game = games[chat_id]
    question, answer = generate_question(game.level, game.difficulty)
    game.current_answer = answer
    game.total_questions += 1
    bot.send_message(chat_id, f"❓ Вопрос {game.total_questions}:\n{question}", reply_markup=create_keyboard())

@bot.message_handler(commands=['help'])
def show_help(message):
    chat_id = message.chat.id
    help_text = "📜 Правила и помощь:\n\n- У вас есть 10 жизней (❤️).\n- Вам будут даваться случайные примеры по арифметике.\n- Сложность примеров будет постепенно увеличиваться.\n- За каждый правильный ответ вы получаете очки (🌟).\n- Если вы ошибаетесь, то теряете жизнь (❤️).\n- Игра заканчивается, когда у вас заканчиваются жизни.\n- У вас есть 3 подсказки (💡), которые вы можете использовать.\n\nЕсли у вас возникли вопросы, не стесняйтесь обращаться!"
    bot.reply_to(message, help_text)

@bot.message_handler(func=lambda message: True)
def check_answer(message):
    chat_id = message.chat.id
    if chat_id not in games:
        bot.reply_to(message, "Пожалуйста, начните новую игру с помощью команды /start")
        return
    game = games[chat_id]
    try:
        user_answer = int(message.text)
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите целочисленный ответ.")
        return
    if user_answer == game.current_answer:
        game.score += game.level * 10
        game.level += 1
        bot.reply_to(message, f"✅ Правильно! Вы получаете {game.level * 10} очков.")
        ask_question(chat_id)
    else:
        game.lives -= 1
        if game.lives == 0:
            bot.reply_to(message, "❌ К сожалению, у вас закончились жизни. Игра окончена.")
            del games[chat_id]
        else:
            bot.reply_to(message, f"❌ Неверно. Правильный ответ: {game.current_answer}. Вы теряете жизнь.")

@bot.callback_query_handler(func=lambda call: call.data == '/start')
def start_new_game(call):
    start_game(call.message)

@bot.callback_query_handler(func=lambda call: call.data == '/help')
def show_help_inline(call):
    show_help(call.message)

bot.polling()
