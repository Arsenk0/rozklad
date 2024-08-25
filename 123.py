import telebot
from telebot import types

TOKEN = '7347174271:AAGYJhZHNnxt7jO2dSlUMnIaHw84KLCIXvY'
bot = telebot.TeleBot(TOKEN)

# Оновлений розклад для 1-го та 2-го тижнів
schedule = {
    '1 тиждень': {
        'Понеділок': ('3 пара: Веб-технології та веб-дизайн лекція 8-117\n'
                      '4 пара: Веб-технології та веб-дизайн практика 8-117\n'
                      '5 пара: Операційні системи практика 8-103'),
        'Вівторок': ('1 пара: Теорія ймовірності, ймовірнісні процеси та математична статистика лекція 9-3\n'
                     '2 пара: Веб-технології та веб-дизайн практика 8-112\n'
                     '3 пара: Організація баз даних та знань лекція 8-117\n'),
        'Середа': ('2 пара: Організація баз даних та знань практика 8-112\n'
                   '3 пара: Об`єктно-орієнтоване програмування практика 8-112\n'
                   '4 пара: Об`єктно-орієнтоване програмування лекція 8-221'),
        'Четвер': ('1 пара: Об`єктно-орієнтоване програмування практика 8-112\n'
                   '2 пара: Операційні системи лекція 8-117\n'
                   '3 пара: Теорія ймовірності, ймовірнісні процеси та математична статистика практика 8-211\n'
                   '4 пара: Англійська мова 8-106')
    },
    '2 тиждень': {
        'Понеділок': ('3 пара: Філософія лекція 8-117\n'
                      '4 пара: Філософія практика 8-117\n'
                      '5 пара: Операційні системи практика 8-103'),
        'Вівторок': ('1 пара: Теорія ймовірності, ймовірнісні процеси та математична статистика лекція 9-3\n'
                     '2 пара: Веб-технології та веб-дизайн практика 8-112\n'
                     '3 пара: Організація баз даних та знань лекція 8-117'
                     '4 пара: Веб-технології та веб-дизайн лекція 8-117'),
        'Середа': ('2 пара: Організація баз даних та знань практика 8-112\n'
                   '3 пара: Об`єктно-орієнтоване програмування практика 8-112\n'
                   '4 пара: Об`єктно-орієнтоване програмування лекція 8-221'),
        'Четвер': ('2 пара: Операційні системи лекція 8-117\n'
                   '3 пара: Теорія ймовірності, ймовірнісні процеси та математична статистика практика 8-211\n'
                   '4 пара: Англійська мова 8-106')
    }
}

# Змінна для зберігання вибору тижня
user_week_choice = {}

# Створення клавіатури для вибору тижня
def create_week_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('1 тиждень')
    item2 = types.KeyboardButton('2 тиждень')
    markup.add(item1, item2)
    return markup

# Створення клавіатури для вибору дня тижня + можливість повернутись до вибору тижня
def create_day_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Понеділок')
    item2 = types.KeyboardButton('Вівторок')
    item3 = types.KeyboardButton('Середа')
    item4 = types.KeyboardButton('Четвер')
    back = types.KeyboardButton('Повернутися до вибору тижня')
    markup.add(item1, item2, item3, item4, back)
    return markup

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привіт! Я твій бот для розкладу уроків.\nОберіть, будь ласка, який це тиждень:", reply_markup=create_week_markup())

# Обробка вибору тижня
@bot.message_handler(func=lambda message: message.text in ['1 тиждень', '2 тиждень'])
def choose_week(message):
    user_week_choice[message.chat.id] = message.text  # Збереження вибору тижня для користувача
    bot.send_message(message.chat.id, "Оберіть день тижня:", reply_markup=create_day_markup())

# Обробка вибору дня тижня або повернення до вибору тижня
@bot.message_handler(func=lambda message: message.text in ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'Повернутися до вибору тижня'])
def send_schedule(message):
    if message.text == 'Повернутися до вибору тижня':
        bot.send_message(message.chat.id, "Оберіть тиждень:", reply_markup=create_week_markup())
    else:
        week = user_week_choice.get(message.chat.id)  # Отримання збереженого вибору тижня для користувача
        if week:
            day = message.text
            bot.send_message(message.chat.id, f"Розклад на {day} ({week}):\n{schedule[week][day]}")
        else:
            bot.send_message(message.chat.id, "Спочатку оберіть тиждень, використовуючи команду /start")

# Запуск бота
bot.polling(none_stop=True)
