import logging
from telebot import types
from bot.settings import bot
from bot.printer import get_printers, ask_color_mode

logging.basicConfig(filename='app.log', level=logging.ERROR)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Отправьте PDF файл для печати.")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.document.mime_type == 'application/pdf':
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            file_name = message.document.file_name
            with open(file_name, 'wb') as new_file:
                new_file.write(downloaded_file)
            
            printers = get_printers(message)
            if not printers:
                return
            
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            for printer in printers:
                markup.add(printer)
            
            msg = bot.reply_to(message, "Выберите принтер для печати:", reply_markup=markup)
            bot.register_next_step_handler(msg, lambda msg: ask_color_mode(msg, file_name, msg.text))
        except Exception as e:
            logging.error(f"Ошибка при обработке PDF файла: {e}")
            bot.reply_to(message, "Произошла ошибка при обработке файла. Попробуйте снова.")
    else:
        bot.reply_to(message, "Пожалуйста, отправьте PDF файл.")
