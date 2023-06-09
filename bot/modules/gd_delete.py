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
    if len(args) > 1:
        link = args[1]
    elif reply_to := message.reply_to_message:
        link = reply_to.text.split(maxsplit=1)[0].strip()
    else:
        link = ''
    if is_gdrive_link(link):
        LOGGER.info(link)
        drive = GoogleDriveHelper()
        if is_folder_link(link):
            msg = await asyncio.create_task(drive.delete_all_files_in_folder(link))
        else:
            msg = await asyncio.create_task(drive.deletefile(link))
    else:
        msg = 'Send Gdrive link along with command or by replying to the link by command'


    await sendMessage(message, msg)
    reply_message = await sendMessage(message, msg)
    await auto_delete_message(message, reply_message)


bot.add_handler(MessageHandler(deletefile, filters=command(
    BotCommands.DeleteCommand) & CustomFilters.authorized))
