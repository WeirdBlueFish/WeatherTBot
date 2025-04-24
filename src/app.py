import telebot
import base
import requestWEATHER as rw
from data import *

bot = telebot.TeleBot(base.TOKEN)
admin_bot = telebot.TeleBot(base.ADMIN_TOKEN)

print("Bot is running...")
username = ""
password = ""   
city = ""

# ----------------- back ----------------- #
def back_to_menu(message):
    
    key_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = telebot.types.KeyboardButton('⏪')
    key_markup.add(back)
    
def send_log_to_admin(message: str):
    admin_bot = telebot.TeleBot(base.ADMIN_TOKEN)
    admin_bot.send_message(base.ADMIN_CHAT_ID, message)

# ----------------- start ----------------- #
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Weather Better Bot!\n\nUse /help to see the available commands.")
    send_log_to_admin(f'User {message.from_user.username} connected to the bot!')
    add_user(message.chat.id, message.chat.username)
    show_menu(message)

@admin_bot.message_handler(commands=['start'])
def send_welcome(message):
    admin_bot.reply_to(message, "Connected to the admin bot!")
    log_message(message)

   
# ----------------- help ----------------- #
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Commands:\n\n/start - Start the bot\
                 \n/help - Show the available commands\
                 \n/InsertCity - Insert a city\
                 \n/MyCities - Show your favorite cities and Check the weather\
                 \n/DeleteCity - Delete a city")
    show_menu(message)

# ----------------- InsertCity ----------------- #
@bot.message_handler(commands=['InsertCity'])
def set_city(message):
    key_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = telebot.types.KeyboardButton('⏪')
    key_markup.add(back)
    city = bot.send_message(message.chat.id, "Insert City:", reply_markup=key_markup)
    bot.register_next_step_handler(city, save_city)
def save_city(message):
    log_message(message)
    global city
    city = message.text
    if city == '⏪':
        show_menu(message)
    else:
        add_favorite_city(message.chat.id, city)
        bot.send_message(message.chat.id, "City has been saved!")

# ----------------- MyCities ----------------- #
@bot.message_handler(commands=['MyCities'])
def show_city(message):
    key_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for city in get_favorite_cities(message.chat.id):
        key_markup.add(city)
    back = telebot.types.KeyboardButton('⏪')
    key_markup.add(back)
    bot.send_message(message.chat.id, "Your cities:", reply_markup=key_markup)
    bot.register_next_step_handler(message, get_weather)
    
# ----------------- DeleteCity ----------------- #
@bot.message_handler(commands=['DeleteCity'])
def delete_city(message):
    key_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = telebot.types.KeyboardButton('⏪')
    key_markup.add(back)
    for city in get_favorite_cities(message.chat.id):
        key_markup.add(city)
    city = bot.send_message(message.chat.id, "Enter the city name you want to delete:", reply_markup=key_markup)
    bot.register_next_step_handler(city, remove_city)
def remove_city(message):
    global city
    city = message.text
    if city == '⏪':
        show_menu(message)
    else:
        remove_favorite_city(message.chat.id, city)
        bot.send_message(message.chat.id, "City has been deleted!")
        show_menu(message)
        
# ----------------- menu ----------------- #
@bot.message_handler(commands=['menu'])
def show_menu(message):
    key_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    Insert_City = telebot.types.KeyboardButton('Insert City')
    My_Cities = telebot.types.KeyboardButton('My Cities')
    delete_city = telebot.types.KeyboardButton('Delete City')
    key_markup.add(Insert_City, My_Cities, delete_city)
    bot.send_message(message.chat.id, "Choose an option:", reply_markup=key_markup)

# ----------------- CheckWeather ----------------- #
@bot.message_handler(commands=['CheckWeather'])
def get_weather(message):
    log_message(message)
    global city
    city = message.text
    if city == '⏪':
        show_menu(message)
    elif city == 'Insert City':
        set_city(message)
    elif city == 'My Cities':
        show_city(message)
    else:
        response = rw.get_city(city)
        result = rw.show_all(response)
        bot.send_message(message.chat.id, result)
        show_city(message)
        
# ----------------- other messages ----------------- #
@bot.message_handler(func = lambda message:True)
def log_message(message):
    user_message = message.text
    log_text = f"username @{message.from_user.username} said: {user_message}"
    send_log_to_admin(log_text)
    handle_other_message(message)

def handle_other_message(message):
    if message.text == 'start':
        send_welcome(message)
    elif message.text == 'Insert City':
        set_city(message)
    elif message.text == 'My Cities':
        show_city(message)  
    elif message.text == 'Delete City':
        delete_city(message)
    elif message.text == '⏪':  
        show_menu(message)

def log_message(message):
    user_message = message.text
    log_text = f"username {message.from_user.username} said: {user_message}"
    send_log_to_admin(log_text)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()