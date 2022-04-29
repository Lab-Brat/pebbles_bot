from telegram.ext import *

def test_response(input_text):
    user_message = str(input_text).lower()

    if user_message == 'hi':
        return 'im here to help with Linux and chew bubblegum'

print("The bot is starting")

def start_command(update, context):
    return update.message.reply_text("Pebbles at your service!")

def handle_message(update, context):
    text = str(update.message.text).lower()
    response = test_response(text)

    update.message.reply_text(response)

def main(api_key):
    updater = Updater(api_key, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    updater.idle()


with open('/home/labbrat/bot_api.txt') as f:
    api_key = f.read().rstrip('\n')
# print(api_key)
main(api_key)


