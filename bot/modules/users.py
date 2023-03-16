from pymongo import MongoClient
from telegram.ext import CommandHandler

from bot import config_dict, OWNER_ID, DATABASE_URL, dispatcher
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage, sendPhoto
from bot.helper.telegram_helper.bot_commands import BotCommands


def dbusers(update, context):
    if not DATABASE_URL:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"DATABASE_URL not provided")
    else:
        client = MongoClient(DATABASE_URL)
        db = client["mltb"]
        count = db.users.count_documents({})
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Total users in database: {count}")


def get_id(update, context):
    chat_id = update.effective_chat.id
    if update.effective_chat.type == 'private':
        user_id = update.message.from_user.id
        context.bot.send_message(chat_id=user_id, text=f"Your user ID is: <code>{user_id}</code>")
    else:
        context.bot.send_message(chat_id=chat_id, text=f"This group's ID is: <code>{chat_id}</code>")

def bot_limit(update, context):
    TORRENT_DIRECT_LIMIT = config_dict['TORRENT_DIRECT_LIMIT']
    CLONE_LIMIT = config_dict['CLONE_LIMIT']
    MEGA_LIMIT = config_dict['MEGA_LIMIT']
    LEECH_LIMIT = config_dict['LEECH_LIMIT']
    ZIP_UNZIP_LIMIT = config_dict['ZIP_UNZIP_LIMIT']
    TOTAL_TASKS_LIMIT = config_dict['TOTAL_TASKS_LIMIT']
    USER_TASKS_LIMIT = config_dict['USER_TASKS_LIMIT']

    torrent_direct = 'No Limit Set' if TORRENT_DIRECT_LIMIT == '' else f'{TORRENT_DIRECT_LIMIT}GB/Link'
    clone_limit = 'No Limit Set' if CLONE_LIMIT == '' else f'{CLONE_LIMIT}GB/Link'
    mega_limit = 'No Limit Set' if MEGA_LIMIT == '' else f'{MEGA_LIMIT}GB/Link'
    leech_limit = 'No Limit Set' if LEECH_LIMIT == '' else f'{LEECH_LIMIT}GB/Link'
    zip_unzip = 'No Limit Set' if ZIP_UNZIP_LIMIT == '' else f'{ZIP_UNZIP_LIMIT}GB/Link'
    total_task = 'No Limit Set' if TOTAL_TASKS_LIMIT == '' else f'{TOTAL_TASKS_LIMIT} Total Tasks/Time'
    user_task = 'No Limit Set' if USER_TASKS_LIMIT == '' else f'{USER_TASKS_LIMIT} Tasks/user'

    if config_dict['EMOJI_THEME']: 
        limit = f"<b>🔢 Bot Limitations </b>\n"\
                f"🧲 Torrent/Direct: {torrent_direct}\n"\
                f"🔐 Zip/Unzip: {zip_unzip}\n"\
                f"🔷 Leech: {leech_limit}\n"\
                f"♻️ Clone: {clone_limit}\n"\
                f"🔰 Mega: {mega_limit}\n"\
                f"💣 Total Tasks: {total_task}\n"\
                f"🔫 User Tasks: {user_task}\n\n"
    else: 
        limit = f"<b>🔢 Bot Limitations </b>\n"\
                f"Torrent/Direct: {torrent_direct}\n"\
                f"Zip/Unzip: {zip_unzip}\n"\
                f"Leech: {leech_limit}\n"\
                f"Clone: {clone_limit}\n"\
                f"Mega: {mega_limit}\n"\
                f"Total Tasks: {total_task}\n"\
                f"User Tasks: {user_task}\n\n"

    if config_dict['PICS']:
        sendPhoto(limit, context.bot, update.message, rchoice(config_dict['PICS']))
    else:
        sendMessage(limit, context.bot, update.message)


dbusers_handler = CommandHandler("dbusers", dbusers, filters=CustomFilters.owner_filter | CustomFilters.sudo_user)
id_handler = CommandHandler("id", get_id)
limit_handler = CommandHandler(BotCommands.LimitCommand, bot_limit,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)


dispatcher.add_handler(dbusers_handler)
dispatcher.add_handler(id_handler)
dispatcher.add_handler(limit_handler)
