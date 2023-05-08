from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client
from script import scripts
from utils import temp_utils
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

@Client.on_callback_query()
async def query_handler(bot: Client, query: CallbackQuery):
    if query.data == "close":
        await query.message.reply_to_message.delete()
        await query.message.delete()
    elif query.data == "about":
        btn = [[
            InlineKeyboardButton("Go Back", callback_data="home"),
            InlineKeyboardButton("Close", callback_data="close")
        ]]
        await query.message.edit_text(
            text=scripts.ABOUT_TXT.format(temp_utils.BOT_NAME),
            reply_markup=InlineKeyboardMarkup(btn)
        )
    elif query.data == "home":
        btn = [[
            InlineKeyboardButton("About", callback_data="about"),
            InlineKeyboardButton("Souce Code", callback_data="source")
        ],[
            InlineKeyboardButton("Close", callback_data="close")
        ]]
        await query.message.edit_text(
            text=scripts.START_TXT.format(query.from_user.mention, temp_utils.USER_NAME, temp_utils.BOT_NAME),
            reply_markup=InlineKeyboardMarkup(btn)
        )
    elif query.data == "source":
        btn = [[
            InlineKeyboardButton("Go Back", callback_data="home"),
            InlineKeyboardButton("Close", callback_data="close")
        ]]
        await query.message.edit_text(
            text=scripts.SOURCE_TXT,
            reply_markup=InlineKeyboardMarkup(btn)
        )
    elif query.data == "cancel_forward":
        temp_utils.CANCEL = True
