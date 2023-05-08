from utils import temp_utils
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, UsernameInvalid, UsernameNotModified
from pyrogram.errors import FloodWait
from script import scripts
from vars import ADMINS, TARGET_DB
import asyncio
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
lock = asyncio.Lock()

@Client.on_message(filters.command("start"))
async def start_message(bot, message):
    btn = [[
        InlineKeyboardButton("About", callback_data="about"),
        InlineKeyboardButton("Souce Code", callback_data="source")
    ],[
        InlineKeyboardButton("Close", callback_data="close")
    ]]
    await message.reply_text(
        text=scripts.START_TXT.format(message.from_user.mention, temp_utils.USER_NAME, temp_utils.BOT_NAME),
        reply_markup=InlineKeyboardMarkup(btn)
    )

@Client.on_message(filters.command("forward") & filters.user(ADMINS))
async def forward_cmd(bot, message):
    cmd = message.text
    if lock.locked():
        return await message.reply_text('<b>Wait until previous process complete.</b>')
    try:
        cmd_name, source_chat_id, last_msg_id = cmd.split(" ")
    except:
        return await message.reply_text("<b>Give me the source chat ID and last message ID of that chat along with this command !\n\nFor Example:\n/forward -1001xxxxxx 93793</b>")

    btn = [[
        InlineKeyboardButton("CANCEL", callback_data="cancel_forward")
    ]]
    active_msg = await message.reply_text(
        text="<b>Starting Forward Process...</b>",
        reply_markup = InlineKeyboardMarkup(btn)
    )
    forwarded = 0
    empty = 0
    left = 0
    async with lock:
        try:
            current = temp_utils.CURRENT
            temp_utils.CANCEL = False
            async for msg in bot.iter_messages(source_chat_id, last_msg_id, temp_utils.CURRENT):
                if temp_utils.CANCEL:
                    await active_msg.edit(f"<b>Successfully Cancelled!\n\nForwarded: {forwarded}\nEmpty Message: {empty}\nMessages Left: {left}</b>")
                    break
                left = int(last_msg_id)-int(forwarded)
                current += 1
                if current % 20 == 0:
                    btn = [[
                        InlineKeyboardButton("CANCEL", callback_data="cancel_forward")
                    ]]
                    await active_msg.edit(
                        text=f"<b>Forwarding on progress...\n\nForwarded: {forwarded}\nEmpty Message: {empty}\nMessages Left: {left}</b>",
                        reply_markup=InlineKeyboardMarkup(btn)
                    )
                if message.empty:
                    empty+=1
                    continue
                try:
                    await msg.copy(chat_id=int(TARGET_DB))
                    forwarded+=1
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(chat_id=int(TARGET_DB))
                    forwarded+=1
                    continue
        except Exception as e:
            logger.exception(e)
            await active_msg.edit(f'Error: {e}')
        else:
            await active_msg.edit(f"<b>Successfully Completed Forward Process !\n\nForwarded: {forwarded}\nEmpty Message: {empty}\nMessages Left: {left}</b>")

@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('Logs.txt')
    except Exception as e:
        await message.reply(str(e))
