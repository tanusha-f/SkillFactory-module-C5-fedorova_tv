import telebot
from config import TOKEN, available
from extensions import APIException, ExchangeRates


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_(message: telebot.types.Message):
    text = "Бот возвращает цену на определенное количество валюты. Чтобы отправить запрос, введите \
команду боту в следующем формате:\n<имя валюты, цену которой необходимо узнать> \
<имя валюты, в которую нужно перевести> <количество переводимой валюты>.\n\n/values - \
вывод списка доступных валют\n/help - вызов справки"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values_(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in available.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert_(message: telebot.types.Message):
    try:
        data_ = message.text.split(' ')
        if len(data_) != 3:
            raise APIException('Неверное количество параметров!\n/help - вызов справки')

        quote, base, amount_str = map(str.lower, data_)

        total = ExchangeRates.get_price(quote, base, amount_str)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount_str} <{quote}> в <{base}>: {total}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
