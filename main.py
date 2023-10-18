import telebot

from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State

state_storage = StateMemoryStorage()
bot = telebot.TeleBot('6316747957:AAGwwZuCAF0MBV2rcVHUryOP5BU-sfmGYZc',
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    key = State()
    cipher = State()
    caesar = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = 'Шифр Цезаря'
text_button_1 = 'Об алгоритме шифрования'
text_button_2 = 'Другие алгоритмы шифрования'
text_button_3 = 'Связь с разработчиком'

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(telebot.types.KeyboardButton(text_poll))
menu_keyboard.add(telebot.types.KeyboardButton(text_button_1))
menu_keyboard.add(telebot.types.KeyboardButton(text_button_2))
menu_keyboard.add(telebot.types.KeyboardButton(text_button_3))


@bot.message_handler(state="*", commands=['start'])
def start_bot(message):
    bot.send_message(message.chat.id, 'Привет! Хотите _зашифровать_ или _расшифровать_ сообщение, '
                                      'узнать больше о *шифрах* или связаться с *разработчиком*?',
                     reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def crypt(message):
    bot.send_message(message.chat.id, 'Вы собираетесь _расшифровать_ или _зашифровать_ ваше сообщение? '
                                      'Напишите *encrypt* или *decrypt*')
    bot.set_state(message.from_user.id, PollState.key, message.chat.id)


@bot.message_handler(state=PollState.key)
def key(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['crypt'] = message.text

    bot.send_message(message.chat.id, 'Напишите ваш *ключ шифрования*. Он необходим, '
                                      'чтобы _зашифровать_ или _расшифровать_ сообщение')
    bot.set_state(message.from_user.id, PollState.cipher, message.chat.id)


@bot.message_handler(state=PollState.cipher)
def cipher(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['key'] = message.text

    bot.send_message(message.chat.id, 'Напишите *ваше сообщение*. Тогда я '
                                      '_расшифрую_ или _зашифрую_ его с помощью ключа')
    bot.set_state(message.from_user.id, PollState.caesar, message.chat.id)


@bot.message_handler(state=PollState.caesar)
def caesar(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['cipher'] = message.text

        # А здесь я зашифрую или расшифрую ваше сообщение!

        alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        message_text = data['cipher'].upper()
        translated_text = ''

        for symbol in message_text:
            if symbol in alphabet:
                num = alphabet.find(symbol)

                if data['crypt'] == 'encrypt':
                    num = num + int(data['key'])
                elif data['crypt'] == 'decrypt':
                    num = num - int(data['key'])

                if num >= len(alphabet):
                    num = num - len(alphabet)
                elif num < 0:
                    num = num + len(alphabet)

                translated_text = translated_text + alphabet[num]

            else:
                translated_text = translated_text + symbol

        print(translated_text)

    bot.send_message(message.chat.id, f'А вот ваше сообщение: {translated_text}', reply_markup=menu_keyboard)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, '*Шифр Цезаря* — это вид _шифра подстановки_, '
                                      'в котором каждый _символ_ в открытом тексте _заменяется символом_, '
                                      'находящимся на некотором постоянном числе позиций _левее или правее_ '
                                      'него в алфавите. Например, в шифре со сдвигом _вправо на 3_, *А* была бы '
                                      'заменена на *Г*, *Б* станет *Д*, и так далее. Величину сдвига можно '
                                      'рассматривать как *ключ шифрования*. '
                                      '[Подробнее о Шифре Цезаря](https://ru.wikipedia.org/wiki/Шифр_Цезаря)',
                     reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, '*Примеры шифров простой замены*: Атбаш, _Шифр Цезаря_, Шифр с '
                                      'использованием кодового слова. *Примеры омофонических шифров*: '
                                      'Номенклатор, Великий Шифр Россиньоля, Книжный шифр. *Примеры '
                                      'полиалфавитных шифров*: _Шифр Виженера_, Одноразовый блокнот. '
                                      '*Примеры полиграммных шифров*: Шифр Плейфера, Шифр Хилла. '
                                      '[Подробнее о других шифрах](https://ru.wikipedia.org/wiki/Шифр_подстановки)',
                     reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, 'Я учусь на *2* курсе магистратуры. Факультет вычислительной техники. '
                                      'Направление: _"Информатика и вычислительная техника"_. '
                                      '[Написать мне](https://t.me/KlimchukNik)',
                     reply_markup=menu_keyboard)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())
bot.infinity_polling()