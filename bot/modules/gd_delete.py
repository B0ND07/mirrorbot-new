#!/usr/bin/env python3
from pyrogram.handlers import MessageHandler
from pyrogram.filters import command

from bot import bot, LOGGER
from bot.helper.telegram_helper.message_utils import auto_delete_message, sendMessage
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.ext_utils.bot_utils import is_gdrive_link, is_folder_link, sync_to_async, new_task


@new_task
async def deletefile(client, message):
    args = message.text.split()
    link = ''
    if len(args) > 1:
        link = args[1]
    elif message.reply_to_message and message.reply_to_message.text:
        link = message.reply_to_message.text.split(maxsplit=1)[0].strip()

    drive = GoogleDriveHelper()

    if is_folder_link(link):
        msg = await sync_to_async(drive.delete_all_files_in_folder)(link)
    else:
        msg = await sync_to_async(drive.deletefile)(link)

    await sendMessage(message, msg)
    reply_message = await sendMessage(message, msg)
    await auto_delete_message(message, reply_message)


bot.add_handler(MessageHandler(deletefile, filters=command(
    BotCommands.DeleteCommand) & CustomFilters.authorized))
