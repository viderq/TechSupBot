import telebot
import dict_db
from telebot import types

dict = dict_db.DB()

bot = telebot.TeleBot('BOT-API-TOKEN')

admin_id = 'user_id'
second_admin_id = 'user_id'


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.send_message(message.chat.id, text='Здравствуйте, отправьте нам свой вопрос.')


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):

    if '✍️ Ответить' in callback.data:
        data = callback.data.split()
        user_id = data[2]
        dict.data = {user_id: None}

        if callback.from_user.id == admin_id:

            send = bot.send_message(admin_id, text='Напиши ответ')
            bot.register_next_step_handler(send, wait_response)

        elif callback.from_user.id == second_admin_id:
            send = bot.send_message(second_admin_id, text='Напиши ответ')
            bot.register_next_step_handler(send, wait_response)


@bot.message_handler(content_types=['text'])
def get_send_message(message):
    markup = types.InlineKeyboardMarkup()
    button_response = types.InlineKeyboardButton(text=f'✍️ Ответить {message.from_user.id}', callback_data=f'✍️ Ответить {message.from_user.id}')

    markup.add(button_response)

    if message.from_user.id == admin_id:
        pass
    else:
        bot.send_message(admin_id, text=f'<b>user_name:</b> <code>{message.from_user.username}</code>\n<b>user_id:</b> <code>{message.from_user.id}</code>\nВопрос: {message.text}', parse_mode='html', reply_markup=markup)
        bot.send_message(second_admin_id, text=f'<b>user_name:</b> <code>{message.from_user.username}</code>\n<b>user_id:</b> <code>{message.from_user.id}</code>\nВопрос: {message.text}', parse_mode='html', reply_markup=markup)
        bot.send_message(message.from_user.id, text='Постараемся ответить в ближайшее время.')


def wait_response(message):
    remove_buttons = telebot.types.ReplyKeyboardRemove()

    user_id = list(dict.data)
    try:
        bot.send_message(user_id[0], message.text)
    except:
        if message.from_user.id == admin_id:
            bot.send_message(admin_id, text='Ответ уже былан или такого пользователя нет.')
        elif message.from_user.id == second_admin_id:
            bot.send_message(second_admin_id, text='Ответ уже былан или такого пользователя нет, во всяком случае не мои проблемы)')

    if message.from_user.id == admin_id:
        bot.send_message(admin_id, text=f'Ответ отправлен пользователю <code>{user_id[0]}</code>', reply_markup=remove_buttons, parse_mode='html')
        bot.send_message(second_admin_id, text=f'<b>Был дан ответ пользователю</b> <code>{user_id[0]}</code> <b>от другого оператора.</b>\n<b>Текст ответа:</b> {message.text}', parse_mode='html')
    elif message.from_user.id == second_admin_id:
        bot.send_message(second_admin_id, text=f'Ответ отправлен пользователю <code>{user_id[0]}</code>', reply_markup=remove_buttons, parse_mode='html')
        bot.send_message(admin_id, text=f'<b>Был дан ответ пользователю</b> <code>{user_id[0]}</code> <b>от другого оператора.</b>\n<b>Текст ответа:</b> {message.text}', parse_mode='html')
    dict.data = {}


bot.polling(none_stop=True, interval=0, timeout=600)
