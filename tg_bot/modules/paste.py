from .helper_funcs.misc import upload_text
from telegram import Update
from telegram.ext import CallbackContext
from tg_bot.modules.helper_funcs.decorators import kigcmd
from io import BytesIO

@kigcmd(command='paste', pass_args=True)
def paste(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message

    if message.reply_to_message:
        data = message.reply_to_message.text or message.reply_to_message.caption
        if message.reply_to_message.document:
            file_info = context.bot.get_file(message.reply_to_message.document.file_id)
            with BytesIO() as file:
                file_info.download(out=file)
                file.seek(0)
                data = file.read().decode()

    elif len(args) >= 1:
        data = message.text.split(None, 1)[1]
    else:
        message.reply_text("What am I supposed to do with this?")
        return

    txt = ""
    paste_url = upload_text(data)
    txt = (
        f"Successfully uploaded to Privatebin: {paste_url}"
        if paste_url
        else "Failed to paste data"
    )

    message.reply_text(txt, disable_web_page_preview=True)
