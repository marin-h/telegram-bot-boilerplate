from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from .store import get_slots

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

def main_menu(update, context):
    id = update.callback_query.data

    print("option chosen has callback: ", update.callback_query.data)
    
    try:
        slot = get_slots()[id]
    except KeyError:
        slot = {
            'slot_text': 'Disculpa, esa opción todavía no funciona.',
            'slot_options': []
        }
    
    append_back_button = True
    if id == 'start':
        append_back_button = False

    query = update.callback_query
    query.answer()
    update.callback_query.message.reply_text(
        text=main_slot_message(slot['slot_text']), parse_mode='html',
        reply_markup=main_slot_keyboard(slot['slot_options'], append_back_button)
    )

def get_option_index(slot_options, option):
    return str(int(slot_options.index(option)) + 1)

def main_slot_keyboard(slot_options, append_back_button):
    buttons = []
    for option in slot_options:
        buttons.append(InlineKeyboardButton(
            option['text'], callback_data=option['id']))

    if append_back_button:
        buttons.append(InlineKeyboardButton('Volver al inicio', callback_data='start'))
    slot_markup = build_menu(buttons, n_cols=1)
    reply_markup = InlineKeyboardMarkup(slot_markup)
    return reply_markup

def main_slot_message(slot_text):
    return slot_text