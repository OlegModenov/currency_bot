import telebot
from config import currencies, TOKEN
from utils import ConversionException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате: \n ' \
           '<имя валюты> <в какую валюту перевести> <количество переводимой валюты> \n' \
           'Например: доллар рубль 2 \n Увидеть список всех доступных валют можно по команде /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currencies:
        text += '\n' + key
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        user_input = message.text.split(' ')

        if len(user_input) != 3:
            raise ConversionException('Нужно 3 параметра')

        currency1, currency2, amount = user_input
        text = f'Цена {amount} {currencies[currency1]} - {Converter.convert(currency1, currency2, amount)} ' \
               f'{currencies[currency2]}'
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)  # Запуск бота
