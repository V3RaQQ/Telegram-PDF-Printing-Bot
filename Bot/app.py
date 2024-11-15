from bot import handlers 
from bot.settings import bot

if __name__ == "__main__":
    try:
        bot.polling()
    except Exception as e:
        import logging
        logging.basicConfig(filename='app.log', level=logging.ERROR)
        logging.error(f"Ошибка при запуске бота: {e}")
