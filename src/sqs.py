import json
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, Application
import logging
import os
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', "1234567890:TEST_TOKEN")
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL', "")

hello_regex = re.compile("hello", re.IGNORECASE)


async def echo_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    echo_message = "Sorry, I don’t understand."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=echo_message)


async def hello_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = "Hi! How can i help you?"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)


def lambda_handler(event, context):
    logger.info("event: {}".format(json.dumps(event)))
    asyncio.get_event_loop().run_until_complete(main(event, context))


def setup_handlers() -> Application:
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    hello_command_handler = CommandHandler('hello', hello_callback)
    application.add_handler(hello_command_handler)

    hello_handler = MessageHandler(filters.Regex(hello_regex), hello_callback)
    application.add_handler(hello_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo_callback)
    application.add_handler(echo_handler)

    return application


async def main(event, context):
    application = setup_handlers()
    await application.initialize()

    for record in event['Records']:
        await application.process_update(
            Update.de_json(json.loads(record["body"]), application.bot)
        )
    await application.shutdown()
