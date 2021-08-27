import os
import http
from werkzeug.wrappers import Response

from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, Filters, CommandHandler, MessageHandler, CallbackQueryHandler

app = Flask(__name__)

@ app.route("/", methods=["POST"])
def index() -> Response:
    dispatcher.process_update(
        Update.de_json(request.get_json(force=True), bot))

    return "", http.HTTPStatus.NO_CONTENT

def echo(update: Update, context) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


bot = Bot(token=os.environ["TOKEN"])

dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
