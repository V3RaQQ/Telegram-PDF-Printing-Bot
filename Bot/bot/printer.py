import win32print
import logging
from telebot import types
from bot.settings import bot

logging.basicConfig(filename='app.log', level=logging.ERROR)

def get_printers(message):
    try:
        printers = [printer[2] for printer in win32print.EnumPrinters(2)]
        return printers
    except Exception as e:
        logging.error(f"Ошибка при получении списка принтеров: {e}")
        bot.reply_to(message, "Не удалось получить список принтеров. Попробуйте позже.")
        return []

def ask_color_mode(message, file_name, printer_name):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Чёрно-белая', 'Цветная')
    msg = bot.reply_to(message, "Выберите режим печати:", reply_markup=markup)
    bot.register_next_step_handler(msg, lambda msg: ask_duplex_mode(msg, file_name, printer_name, msg.text))

def ask_duplex_mode(message, file_name, printer_name, color_mode):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Односторонняя', 'Двухсторонняя (по длинному краю)', 'Двухсторонняя (по короткому краю)')
    msg = bot.reply_to(message, "Выберите тип печати:", reply_markup=markup)
    bot.register_next_step_handler(msg, lambda msg: print_pdf(message, file_name, printer_name, color_mode, msg.text))

def print_pdf(message, file_name, printer_name, color_mode, duplex_mode):
    try:
        hPrinter = win32print.OpenPrinter(printer_name)
        print_settings = win32print.GetPrinter(hPrinter, 2)
        devmode = print_settings['pDevMode']

        devmode.Color = 1 if color_mode == 'Чёрно-белая' else 2
        devmode.Duplex = {
            'Односторонняя': 1,
            'Двухсторонняя (по длинному краю)': 2,
            'Двусторонняя (по короткому краю)': 3
        }.get(duplex_mode, 1)

        win32print.SetPrinter(hPrinter, 2, print_settings, 0)

        job = win32print.StartDocPrinter(hPrinter, 1, (file_name, None, "RAW"))
        win32print.StartPagePrinter(hPrinter)
        with open(file_name, 'rb') as file:
            win32print.WritePrinter(hPrinter, file.read())
        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
        win32print.ClosePrinter(hPrinter)

        bot.send_message(message.chat.id, "Файл отправлен на печать!")
    except Exception as e:
        logging.error(f"Ошибка при печати PDF: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка при печати. Попробуйте снова.")
