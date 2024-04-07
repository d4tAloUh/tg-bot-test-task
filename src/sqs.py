import json
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import logging
import os
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', "")
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL', "")

application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

hello_regex = re.compile("hello", re.IGNORECASE)
# TODO Notes:
# - Regex could be replaced with custom 'string in' filter, because 'string in' operator is faster than pattern matching


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    echo_message = "Sorry, I don’t understand."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=echo_message)


async def hello_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = "Hi! How can i help you?"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)


def lambda_handler(event, context):
    logger.info("event: {}".format(json.dumps(event)))
    asyncio.get_event_loop().run_until_complete(main(event, context))


async def main(event, context):
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    hello_command_handler = CommandHandler('hello', hello_callback)
    application.add_handler(hello_command_handler)

    hello_handler = MessageHandler(filters.Regex(hello_regex), hello_callback)
    application.add_handler(hello_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    for record in event['Records']:
        await application.initialize()
        await application.process_update(
            Update.de_json(json.loads(record["body"]), application.bot)
        )
