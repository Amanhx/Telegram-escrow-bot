from telegram import Update, ChatPermissions, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# ✅ Hardcoded Bot Token aur Group IDs
BOT_TOKEN = '7594065240:AAG18BJ3jixepKept3-mDJjcBtaV4LE71xg'
MAIN_GROUP_ID = -1002342410399
ESCROW_GROUP_ID = -1002899093990

# ❌ Default: No message allowed
default_restriction = ChatPermissions(can_send_messages=False)

# ✅ Full chat permission after verify
full_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True
)

# ✅ /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Bot is active and monitoring.")

# 🚫 New member = restrict + ask to verify
def new_member(update: Update, context: CallbackContext):
    for user in update.message.new_chat_members:
        context.bot.restrict_chat_member(
            chat_id=update.message.chat.id,
            user_id=user.id,
            permissions=default_restriction
        )
        update.message.reply_text(
            f"👋 Welcome {user.first_name}!\n\n🛑 Please join the Escrow Group first:\n👉 https://t.me/+YOUR_ESCROW_GROUP_LINK\n\nThen type /verify here to unlock chat access.",
            parse_mode=ParseMode.HTML
        )

# ✅ /verify command
def verify(update: Update, context: CallbackContext):
    user = update.effective_user
    bot = context.bot

    try:
        member = bot.get_chat_member(chat_id=ESCROW_GROUP_ID, user_id=user.id)
        if member.status in ["member", "administrator", "creator"]:
            bot.restrict_chat_member(
                chat_id=MAIN_GROUP_ID,
                user_id=user.id,
                permissions=full_permissions
            )
            update.message.reply_text("✅ Verified! You can now chat.")
        else:
            update.message.reply_text("❌ Please join the Escrow group first.")
    except Exception as e:
        update.message.reply_text("❌ Could not verify. Make sure you've joined the Escrow group.")

# 🚫 Auto-delete links in messages
def block_links(update: Update, context: CallbackContext):
    if update.message.entities:
        for entity in update.message.entities:
            if entity.type in ["url", "text_link"]:
                try:
                    update.message.delete()
                except:
                    pass
                break

# ✅ Bot starter
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("verify", verify))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))
    dp.add_handler(MessageHandler(Filters.entity("url") | Filters.entity("text_link"), block_links))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
