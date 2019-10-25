from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters


TG_TOKEN = "822102958:AAHsgSxtLNp1FHMFXih30Rkpkx4DHFsvsFU"



def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Привет! Напиши мне!",    
    )

def message_handler(bot:Bot, update: Update):
    user = update.effective_user
    if user:
        name = user.first_name
    else:
        name = 'Аноним'

    bot.send_message(
        chat_id=update.effective_message.chat_id,
        text=reply_text,
    )
     

def main():
    print('Start')
    bot = Bot(
        token=TG_TOKEN,
        #base_url="https:telegg.ru/orig/bot"   #proxy
    )
    updater = Updater(
        bot=bot,
    )

    start_handler = CommandHandler("start", do_start)
    message_handler = MessageHandler(Filters.text, do_echo )
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.start_polling()
    updater.idle()
    print('Finish')



def do_echo(bot:Bot, update: Update):
    text = update.message.text
    bot.send_message(chat_id=update.message.chat_id,
    text=text)


'''
    handler = MessageHandler(Filters.all, message_handler)
    updater.dispatcher.add_handler(handler)

    updater.start_polling()
    updater.idle()
    print('Finish')
'''

if __name__=='__main__':
    main()