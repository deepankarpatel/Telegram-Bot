from typing import Final

import requests
import schedule
import time
from telegram import Bot
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
from telegram import *

TOKEN: Final = '6501527937:AAElhrscI8mRzlPBld96EVR87LBu83blP3E'
BOT_USERNAME: Final = '@manaa1_bot'

API_KEY = "f1031ee2558b210bfb3ab0deb68ad20a"


# commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Hello! Thanks for coming here... Im filled with mana magic. What can i do for you?')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Wait help is on the way!!')


async def weather(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        await update.message.reply_text("Please provide a city name. e.g., /weather London")
        return

    city = " ".join(context.args)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&app-id={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data["cod"] != 200:
        await update.message.reply_text("City not found. Please try again.")
        return

    weather_description = data["weather"][0]["description"]
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]

    message = f"Weather in {city}: {weather_description}\nTemperature: {temperature}°C\nHumidity: {humidity}%"
    await update.message.reply_text(message)


# Responses
def handle_responses(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'hey there!'

    if 'how are you' in processed:
        return "i am good!"

    if 'what can you do' in processed:
        return 'i can create magic!'

    return 'i do not understand what you wrote...'


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'user({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            responses: str = handle_responses(new_text)
        else:
            return
    else:
        responses = handle_responses(text)

    print('Bot:', responses)
    await update.message.reply_text(responses)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('weather', weather))
    app.add_handler(CommandHandler('send weather', send_weather))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_messages))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)


# Automation
async def send_weather(bot):
    city = "Ghaziabad"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&app-id={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        message = f"Weather in {city}: {weather_description}\nTemperature: {temperature}°C\nHumidity: {humidity}%"
        bot.send_message(chat_id="firehawks_7", text=message)
    else:
        print("City not found. Please try again.")


def job():
    bot = Bot(TOKEN)
    send_weather(bot)


# Schedule the job to run every day at 9 am
schedule.every().day.at("22:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
