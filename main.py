from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = TeleBot("6292477796:AAHRMxUOC-jx7AxSRKMZU1DQD9jQ_DpxguM")

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    bot_data[user_id] = {}
    bot_data[user_id]['step'] = 1
    bot_data[user_id]['answers'] = {}

    question = 'Привіт! Я допоможу вам підібрати вигідний тариф. Скільки ви витрачаєте хвилин на розмови щомісяця?'
    options = ['Менше 100 хв', '100-300 хв', 'Більше 300 хв']
    reply_markup = create_reply_markup(options)
    bot.send_message(message.chat.id, question, reply_markup=reply_markup)


def create_reply_markup(options):
    keyboard = InlineKeyboardMarkup()
    for option in options:
        button = InlineKeyboardButton(option, callback_data=option)
        keyboard.add(button)
    return keyboard


@bot.callback_query_handler(func=lambda call: True)
def handle_choice(call):
    user_id = call.from_user.id
    step = bot_data[user_id]['step']
    selected_option = call.data

    bot_data[user_id]['answers'][step] = selected_option

    if step == 1:
        question = 'Скільки вам потрібно гігабайт інтернету на місяць?'
        options = ['Менше 5 ГБ', '5-10 ГБ', 'Більше 10 ГБ']
        reply_markup = create_reply_markup(options)
        bot.send_message(call.message.chat.id, question, reply_markup=reply_markup)

    elif step == 2:
        question = 'Яка вам потрібна кількість SMS на місяць?'
        options = ['Менше 100 SMS', '100-500 SMS', 'Більше 500 SMS']
        reply_markup = create_reply_markup(options)
        bot.send_message(call.message.chat.id, question, reply_markup=reply_markup)

    elif step == 3:
        question = 'Чи потрібні вам послуги роумінгу?'
        options = ['Так', 'Ні']
        reply_markup = create_reply_markup(options)
        bot.send_message(call.message.chat.id, question, reply_markup=reply_markup)

    elif step == 4:
        question = 'Яку тривалість дії тарифного плану ви розглядаєте?'
        options = ['14 днів', '30 днів', '60 днів']
        reply_markup = create_reply_markup(options)
        bot.send_message(call.message.chat.id, question, reply_markup=reply_markup)

    elif step == 5:
        question = 'Чи потрібна вам безлімітна міжнародна роумінгова послуга?'
        options = ['Так', 'Ні']
        reply_markup = create_reply_markup(options)
        bot.send_message(call.message.chat.id, question, reply_markup=reply_markup)

    bot_data[user_id]['step'] += 1


@bot.callback_query_handler(func=lambda call: True)
def handle_roaming_choice(call):
    user_id = call.from_user.id
    step = bot_data[user_id]['step']
    selected_option = call.data

    bot_data[user_id]['answers'][step] = selected_option

    if step == 6:
        question = 'Яка тривалість дії безлімітного міжнародного роумінгу ви розглядаєте?'
        options = ['7 днів', '14 днів', '30 днів']
        reply_markup = create_reply_markup(options)
        bot.send_message(call.message.chat.id, question, reply_markup=reply_markup)

    bot_data[user_id]['step'] += 1


@bot.message_handler(commands=['finish'])
def finish(message):
    user_id = message.from_user.id
    answers = bot_data[user_id]['answers']

    minutes = answers.get(1)
    internet = answers.get(2)
    sms = answers.get(3)
    roaming = answers.get(4)
    roaming_duration = answers.get(6)

    recommended_tariff = select_tariff(minutes, internet, sms, roaming, roaming_duration)

    bot.send_message(message.chat.id, f'Рекомендація: {recommended_tariff}')


def select_tariff(minutes, internet, sms, roaming, roaming_duration):
    if minutes == 'Менше 100 хв' and internet == 'Менше 5 ГБ':
        return 'Тарифний план А: Опис тарифу А'
    elif minutes == '100-300 хв' and internet == '5-10 ГБ':
        return 'Тарифний план Б: Опис тарифу Б'
    elif minutes == 'Більше 300 хв' and internet == 'Більше 10 ГБ':
        return 'Тарифний план В: Опис тарифу В'
    else:
        return 'Тарифний план не знайдено'


if __name__ == '__main__':
    bot_data = {}
    bot.polling()

