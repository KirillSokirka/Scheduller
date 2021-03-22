import config
import excel
import dao

import re
import telebot
from telebot import types

bot = telebot.TeleBot(config.Token)
db = dao.meta

db.create_all(dao.engine)


@bot.message_handler(commands=['start'])
def start_answer(message):
    animation = open(config.Animation1, 'rb')
    bot.send_animation(message.from_user.id, animation)
    bot.send_message(message.from_user.id,
                     "Доброго дня!\nЯ - <b>ScheduleBot</b>, був створений, щоб допомогати вам слідкувати за розкладом пар.\n"
                     "Для того, щоб користуватися ботом, спочатку оберіть команду /setgroup, а потім команду /setday",
                     parse_mode='html')


@bot.message_handler(commands=['setgroup'])
def set_group(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    button1 = types.KeyboardButton("11 група")
    keyboard.add(button1)
    bot.send_message(message.from_user.id, "Оберіть свою групу", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in ["11 група"])
def student_add(message):
    dao.add_student(message.from_user.id, message.text, False)
    bot.send_message(message.from_user.id,
                     "Тепер оберіть потрібний вам день використовуючи команду /setday")


@bot.message_handler(commands=['setday'])
def set_day(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    button1 = types.KeyboardButton("Понеділок")
    button2 = types.KeyboardButton("Вівторок")
    button3 = types.KeyboardButton("Середа")
    button4 = types.KeyboardButton("Четвер")
    button5 = types.KeyboardButton("П'ятниця")
    keyboard.add(button1, button2, button3, button4, button5)

    bot.send_message(message.from_user.id, "Оберіть день, розклад якого хочете побачити", reply_markup=keyboard)


def group_convert_to_int(group):
    text_group = str(group[0])
    group_num = re.split(' ', text_group)
    return int(group_num[0])


@bot.message_handler(func=lambda message: message.text in ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця"])
def one_day_schedule(message):
    #group_one = dao.get_group(message.from_user.id)
    #if  group_one == None:
     #   bot.send_message(message.from_user.id, "Оберіть спочатку вашу групу використовуючи команду /setgroup")
        #group = group_convert_to_int(group_one)
    information = excel.ExcelOneDay(11, message.text)
    for i in range(len(information)):
        bot.send_message(message.from_user.id, information[i], parse_mode="MarkdownV2")

@bot.message_handler(content_types=['text'])
def undefined_text_reaction(message):
    animation = open(config.Animation2, 'rb')
    bot.send_animation(message.from_user.id, animation)
    bot.send_message(message.from_user.id, 'Перевірте коректність введеного тексту')


if __name__ == '__main__':
    bot.polling(none_stop=True)
