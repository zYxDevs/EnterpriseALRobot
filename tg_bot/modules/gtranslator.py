from gpytranslate import Translator
from tg_bot.modules.language import gs


def get_help(chat):
    return gs(chat, "gtranslate_help")


__mod_name__ = "Translator"

trans = Translator()
from telegram.constants import ParseMode
from telegram import Update
from telegram.ext import CallbackContext
from tg_bot.modules.helper_funcs.decorators import kigcmd


@kigcmd(command=["tr", "tl"])
async def translate(update: Update, context: CallbackContext) -> None:
    global to_translate
    bot = context.bot
    message = update.effective_message
    reply_msg = message.reply_to_message
    if not reply_msg:
        await message.reply_text("Reply to a message to translate it!")
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = await message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "en"
    translation = await trans.translate(to_translate, sourcelang=source, targetlang=dest)
    reply = (
        f"<b>Translated from {source} to {dest}</b>:\n"
        f"<code>{translation.text}</code>"
    )

    await bot.send_message(
        text=reply, chat_id=message.chat.id, parse_mode=ParseMode.HTML
    )


@kigcmd(command="langs")
async def languages(update: Update, context: CallbackContext) -> None:
    message = update.effective_message
    bot = context.bot
    await bot.send_message(
        text="Click [here](https://cloud.google.com/translate/docs/languages) to see the list of supported language "
        "codes!",
        chat_id=message.chat.id,
        disable_web_page_preview=True,
        parse_mode=ParseMode.MARKDOWN,
    )
