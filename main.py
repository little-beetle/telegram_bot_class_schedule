import telebot
import os
from telebot import types
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('token')

bot = telebot.TeleBot(token)


@bot.message_handler(commands = ['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    item = types.InlineKeyboardButton('Меню', callback_data='main_menu')
    markup.add(item)

    bot.send_message(message.chat.id, 'Привіт! Це початкове повідомлення.', reply_markup=markup)


@bot.callback_query_handler(func = lambda call: call.data == 'main_menu')
def main_menu_callback(call):
    # Обробка натискання кнопки ʼменюʼ і перехід до головного меню
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Поділитися ->", callback_data='share')
    item2 = types.InlineKeyboardButton("Визначити свою групу", callback_data='your_group')
    markup.add(item1, item2)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Головне меню', reply_markup=markup)


@bot.callback_query_handler(func = lambda call: call.data == 'share')
def share_bot(call):
    markup = types.InlineKeyboardMarkup()
    share_button = types.InlineKeyboardButton('Share Bot', switch_inline_query='t.me/class_on_time_bot')
    markup.add(share_button)

    bot.send_message(call.from_user.id, 'Натисни кнопку нижче, щоб поділитися ботом зі своїм другом',
                     reply_markup=markup)


@bot.callback_query_handler(func = lambda call: call.data == 'your_group')
def choice_group(call):
    bot.send_message(call.message.chat.id, 'Введіть своє ім\'я')
    bot.register_next_step_handler(call.message, get_name)


def get_name(message):
    name = message.text
    bot.send_message(message.chat.id, f'Ваше ім\'я: {name}')
    bot.send_message(message.chat.id, 'Введіть свій факультет: ')
    bot.register_next_step_handler(message, get_faculty)


def get_faculty(message):
    faculty = message.text
    bot.send_message(message.chat.id, f'Ваш факультет: {faculty}')
    bot.send_message(message.chat.id, 'Введіть свою групу: ')
    bot.register_next_step_handler(message, get_group)


def get_group(message):
    group = message.text
    bot.send_message(message.chat.id, f'Ваша група: {group}')



bot.infinity_polling()