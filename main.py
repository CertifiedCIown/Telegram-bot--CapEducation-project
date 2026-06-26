import telebot, re, sys, json
from telebot import types
from pathlib import Path

pattern = re.compile(r"/(start|about|goal|story|mentor|progress|hobby|projects)\b", re.IGNORECASE)

try:
    script_dir = Path(__file__).parent.resolve()
    file_path = script_dir / "MainText.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Проверьте целостность файлов и текстовых документов, а так же местонахождение json файла")

if len(sys.argv) < 2:
    print("Использование: python bot.py <TOKEN>")
    exit()
TOKEN = sys.argv[1]
bot = telebot.TeleBot(TOKEN)

#Стартовое сообщение и inline кнопки к нему
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(    
        types.InlineKeyboardButton('Обо мне', callback_data="about"),
        types.InlineKeyboardButton('Цель', callback_data="goal"), 
        types.InlineKeyboardButton('Знакомство с IT', callback_data="story"),
        types.InlineKeyboardButton('Ментор', callback_data="mentor"),
        types.InlineKeyboardButton('Прогресс', callback_data="progress"),
        types.InlineKeyboardButton('Хобби', callback_data="hobby"),
        types.InlineKeyboardButton('Лучшие проекты', callback_data="projects"))
    bot.send_message(message.chat.id, data['start'], reply_markup=markup)

#Исполнительные команды и текста сообщений
def send_section(message, section):
    bot.send_message(message.chat.id, data[section])

#Словарь
handlers = {
    "start": start, 
    "about": lambda msg: send_section(msg, "about"),
    "goal": lambda msg: send_section(msg, "goal"),
    "story": lambda msg: send_section(msg, "story"),
    "mentor": lambda msg: send_section(msg, "mentor"),
    "progress": lambda msg: send_section(msg, "progress"),
    "hobby": lambda msg: send_section(msg, "hobby"),
    "projects": lambda msg: send_section(msg, "projects")
}

#Проверка наличия комманд в сообщении
@bot.message_handler(func=lambda message:True)
def message_text(message):
    text = message.text
    any_commands = pattern.findall(text)
    if any_commands:
        for cmd in dict.fromkeys(any_commands):
            Cmd = cmd.lower()
            if Cmd in handlers:
                handlers[cmd](message)

#Доработка inline кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data in handlers:
        handlers[call.data](call.message)
    bot.answer_callback_query(call.id)

bot.infinity_polling()