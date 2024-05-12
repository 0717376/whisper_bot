import os
import random
from dotenv import load_dotenv
import telebot

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

games = {}

class Game:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.lives = 10
        self.score = 0
        self.level = 1
        self.total_questions = 0

def generate_question(level):
    ops = ['+', '-', '*', '/']
    if level == 1:
        a, b = random.randint(1, 10), random.randint(1, 10)
    elif level == 2:
        a, b = random.randint(10, 50), random.randint(10, 50)
    else:
        a, b = random.randint(50, 100), random.randint(50, 100)
    op = random.choice(ops)
    question = f"{a} {op} {b}"
    answer = eval(question)
    return question, answer

def update_game_message(chat_id):
    game = games[chat_id]
    message = f"Вопрос {game.total_questions}\nЖизни: {game.lives}\nОчки: {game.score}"
    return message

@bot.message_handler(commands=['start'])
def start_game(message):
    chat_id = message.chat.id
    games[chat_id] = Game(chat_id)
    rules = "Добро пожаловать в арифметическую игру!\n\nПравила:\n- У вас есть 10 жизней.\n- Вам будут даваться случайные примеры по арифметике.\n- Сложность примеров будет постепенно увеличиваться.\n- За каждый правильный ответ вы получаете очки.\n- Если вы ошибаетесь, то теряете жизнь.\n- Игра заканчивается, когда у вас заканчиваются жизни.\n\nДавайте начнем!"
    bot.reply_to(message, rules)
    question, answer = generate_question(games[chat_id].level)
    games[chat_id].current_answer = answer
    games[chat_id].total_questions += 1
    bot.send_message(chat_id, f"Вопрос {games[chat_id].total_questions}: {question}")

@bot.message_handler(func=lambda message: True)
def check_answer(message):
    chat_id = message.chat.id
    if chat_id not in games:
        bot.reply_to(message, "Пожалуйста, начните новую игру с помощью команды /start")
        return
    game = games[chat_id]
    try:
        user_answer = float(message.text)
    except ValueError:
        bot.reply_to(message, "Пожалуйста, введите числовой ответ.")
        return
    if user_answer == game.current_answer:
        game.score += game.level * 10
        game.level += 1
        question, answer = generate_question(game.level)
        game.current_answer = answer
        game.total_questions += 1
        message_text = f"Правильно! Вы получаете {game.level * 10} очков.\n\n"
        message_text += update_game_message(chat_id)
        message_text += f"\n\nВопрос {game.total_questions}: {question}"
        bot.reply_to(message, message_text)
    else:
        game.lives -= 1
        if game.lives == 0:
            message_text = "К сожалению, у вас закончились жизни. Игра окончена.\n\n"
            message_text += f"Итоговая статистика:\nВопросов отвечено: {game.total_questions}\nОчки: {game.score}"
            bot.reply_to(message, message_text)
            del games[chat_id]
        else:
            message_text = f"Неверно. Правильный ответ: {game.current_answer}. Вы теряете жизнь.\n\n"
            message_text += update_game_message(chat_id)
            question, answer = generate_question(game.level)
            game.current_answer = answer
            game.total_questions += 1
            message_text += f"\n\nВопрос {game.total_questions}: {question}"
            bot.reply_to(message, message_text)

bot.polling()