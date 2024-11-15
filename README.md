# **Telegram PDF Printing Bot**

This project is a Telegram bot designed to enable users to send PDF files for printing. The bot interacts with printers connected to the system and provides options for printer selection, color mode, and duplex printing.

## **Features**
- **PDF File Handling**: 
  - Accepts PDF files uploaded by users via Telegram.
- **Printer Selection**: 
  - Displays a list of available printers for users to choose from.
- **Customizable Print Settings**: 
  - Choose between **black-and-white** or **color printing**.
  - Select **single-sided** or **double-sided printing** (long or short edge).
- **Error Handling**:
  - Logs errors in `app.log` and notifies users if issues occur.
- **Modular Design**: 
  - Well-structured codebase for easy maintenance and feature extension.

## **Technologies Used**
- **Python**: Core programming language.
- **[pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)**: Telegram bot API wrapper.
- **[pywin32](https://github.com/mhammond/pywin32)**: Windows-specific printer management library.
- **Logging**: Built-in Python logging for debugging and error tracking.

## **Installation and Setup**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/telegram-pdf-printing-bot.git
   cd telegram-pdf-printing-bot
