from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    context.user_data[user_id] = {}
    context.user_data[user_id]['step'] = 1
    context.user_data[user_id]['answers'] = {}

   
    question = 'Привіт! Я допоможу вам підібрати вигідний тариф. Скільки ви витрачаєте хвилин на розмови щомісяця?'
    options = ['Менше 100 хв', '100-300 хв', 'Більше 300 хв']
    reply_markup = create_reply_markup(options)
    update.message.reply_text(question, reply_markup=reply_markup)

def create_reply_markup(options):
    keyboard = [[InlineKeyboardButton(option, callback_data=option)] for option in options]
    return InlineKeyboardMarkup(keyboard)

def handle_choice(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    step = context.user_data[user_id]['step']
    selected_option = update.callback_query.data

   
    context.user_data[user_id]['answers'][step] = selected_option

    if step == 1:
        
        question = 'Скільки вам потрібно гігабайт інтернету на місяць?'
        options = ['Менше 5 ГБ', '5-10 ГБ', 'Більше 10 ГБ']
        reply_markup = create_reply_markup(options)
        update.callback_query.message.reply_text(question, reply_markup=reply_markup)

    elif step == 2:
        
        question = 'Яка вам потрібна кількість SMS на місяць?'
        options = ['Менше 100 SMS', '100-500 SMS', 'Більше 500 SMS']
        reply_markup = create_reply_markup(options)
        update.callback_query.message.reply_text(question, reply_markup=reply_markup)

    elif step == 3:
        
        question = 'Чи потрібні вам послуги роумінгу?'
        options = ['Так', 'Ні']
        reply_markup = create_reply_markup(options)
        update.callback_query.message.reply_text(question, reply_markup=reply_markup)

    elif step == 4:
        
        question = 'Яку тривалість дії тарифного плану ви розглядаєте?'
        options = ['14 днів', '30 днів', '60 днів']
        reply_markup = create_reply_markup(options)
        update.callback_query.message.reply_text(question, reply_markup=reply_markup)

    elif step == 5:
        
        question = 'Чи потрібна вам безлімітна міжнародна роумінгова послуга?'
        options = ['Так', 'Ні']
        reply_markup = create_reply_markup(options)
        update.callback_query.message.reply_text(question, reply_markup=reply_markup)


    context.user_data[user_id]['step'] += 1
def finish(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    answers = context.user_data[user_id]['answers']

    minutes = answers.get(1)  # Відповідь на питання про хвилини розмови
    internet = answers.get(2)  # Відповідь на питання про інтернет

    
    recommended_tariff = select_tariff(minutes, internet)

    
    update.message.reply_text(f'Рекомендація: {recommended_tariff}')

def select_tariff(minutes, internet):

    if minutes == 'Менше 100 хв' and internet == 'Менше 5 ГБ':
        recommended_tariff = 'Тариф А'
    elif minutes == '100-300 хв' and internet == '5-10 ГБ':
        recommended_tariff = 'Тариф Б'
    else:
        recommended_tariff = 'Тариф В'

    return recommended_tariff


def main():
    updater = Updater("6292477796:AAHRMxUOC-jx7AxSRKMZU1DQD9jQ_DpxguM", use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(handle_choice))
    dispatcher.add_handler(CommandHandler("finish", finish))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

