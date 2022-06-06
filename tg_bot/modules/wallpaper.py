from random import randint

import requests as r
from tg_bot import WALL_API
from telegram import Update
from telegram.ext import CallbackContext
from tg_bot.modules.helper_funcs.decorators import kigcmd

# Wallpapers module by @TheRealPhoenix using wall.alphacoders.com

@kigcmd(command='wall')
def wall(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = update.effective_message
    args = context.args
    msg_id = update.effective_message.message_id
    bot = context.bot
    if query := " ".join(args):
        term = query.replace(" ", "%20")
        json_rep = r.get(
            f"https://wall.alphacoders.com/api2.0/get.php?auth={WALL_API}&method=search&term={term}"
        ).json()
        if not json_rep.get("success"):
            msg.reply_text("An error occurred! Report this @YorkTownEagleUnion")
        elif wallpapers := json_rep.get("wallpapers"):
            index = randint(0, len(wallpapers) - 1)  # Choose random index
            wallpaper = wallpapers[index]
            wallpaper = wallpaper.get("url_image")
            wallpaper = wallpaper.replace("\\", "")
            bot.send_photo(
                chat_id,
                photo=wallpaper,
                caption="Preview",
                reply_to_message_id=msg_id,
                timeout=60,
            )
            caption = query
            bot.send_document(
                chat_id,
                document=wallpaper,
                filename="wallpaper",
                caption=caption,
                reply_to_message_id=msg_id,
                timeout=60,
            )
        else:
            msg.reply_text("No results found! Refine your search.")
            return
    else:
        msg.reply_text("Please enter a query!")
        return
