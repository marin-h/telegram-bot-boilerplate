import os
import http
import json
from werkzeug.wrappers import Response

from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, Filters, CommandHandler, MessageHandler, CallbackQueryHandler, DispatcherHandlerStop

from src import store, builder
from datetime import datetime

FILE_PATH = os.path.abspath(os.environ['APP_CONFIG_PATH'])
ADMIN_USERS = os.environ['ADMIN_USERS'].split(',')
admin_users = [int(n) for n in ADMIN_USERS] if len(ADMIN_USERS) else []

app = Flask(__name__)

def start(update, context):
    menu = store.get_slots()['start']
    update.message.reply_text(
        builder.main_slot_message(menu['slot_text']), parse_mode='html',
        reply_markup=builder.main_slot_keyboard(menu['slot_options'], False))

def restore(update, context):
    # validate user
    if update.message.chat.id not in admin_users:
        raise DispatcherHandlerStop

    data = store.load_backup(context.args[0])
    store.do_config(data)
    update.message.reply_text("Configuración actualizada!")

def upload(update, context):
    # validate user
    # 206586116 -> marin
    # 648041635 -> male    
    # 368488484 -> mariano
    if update.message.chat.id not in [206586116, 648041635, 368488484]:
        print('upload not allowed for user', update)
        raise DispatcherHandlerStop

    # download received file
    file_id = context.bot.get_file(update.message.document).download()
    
    # read and process data to get slots
    with open(file_id, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print('the data', data)

    # setup
    store.do_config(json.dumps(store.process_slots(data)))

    print('uploading decoded data', data)
    # upload backup config file to drive
    uploaded = store.save_backup(file_id)
    update.message.reply_text(
        "Configuración actualizada! Archivo de backup: {}".format(json.dumps(uploaded)))

@ app.route("/", methods=["POST"])
def index() -> Response:
    dispatcher.process_update(
        Update.de_json(request.get_json(force=True), bot))

    return "", http.HTTPStatus.NO_CONTENT

bot = Bot(token=os.environ["TOKEN"])

dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('restaurar', restore))
dispatcher.add_handler(MessageHandler(Filters.caption(update=['/cargar']), upload))
dispatcher.add_handler(CallbackQueryHandler(builder.main_menu))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, start))

load_backup = False

if load_backup:
    print("init: load latest backup")
    data = json.loads(store.load_backup())
    if data:
        print("init: got data", data)
        store.do_config(json.dumps(store.process_slots(data)))
        print("init: config finished")