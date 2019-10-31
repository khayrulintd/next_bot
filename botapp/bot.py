from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, CommandHandler, ConversationHandler, RegexHandler, Filters
import logging
from telegram import ReplyKeyboardRemove, ParseMode
#from handlers import *

TG_TOKEN = "822102958:AAHsgSxtLNp1FHMFXih30Rkpkx4DHFsvsFU"

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
level = logging.INFO,
filename ='bot.log')

def greet_user(bot: Bot, update: Update, user_data):
    text = '''Привет! Данный бот предназначен для взаимодействия с сервисом Blood_pressure. Если вы зарегистрированы нажмите Login, если не зарегистрированы нажмите Signup."
           '''
    my_keybord = ReplyKeyboardMarkup([['Login'],['Signup']])       #,['/input pressure data']
    update.message.reply_text(text, reply_markup=my_keybord)



def main():
    print('Start')
    logging.info ('Бот стартанул')
        
    bot = Bot(
        token=TG_TOKEN,        
    )
    updater = Updater(
        bot=bot,
    )      
       
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    
    
    signup = ConversationHandler(
    entry_points=[dp.add_handler(RegexHandler('^(Signup)$', signup_start, pass_user_data=True))],
    states={
        "name": [MessageHandler(Filters.text, signup_get_name_and_surname, pass_user_data=True)],
        "login_pas": [MessageHandler(Filters.text, signup_get_login_and_pas, pass_user_data=True)],
        "account_created": [MessageHandler(Filters.text, signup_account_created, pass_user_data=True)]
        },
    fallbacks=[]
    )
    dp.add_handler(CommandHandler('Signup', signup, pass_user_data=True))
    
    #updater.dispatcher.add_handler(CommandHandler("login", login, pass_user_data=True))
    #updater.dispatcher.add_handler(MessageHandler(Filters.text, do_echo) )
    updater.start_polling()
    updater.idle()


def do_echo(bot:Bot, update: Update):
    text = update.message.text
    bot.send_message(chat_id=update.message.chat_id,
    text=text)
  

def signup_start(bot, update, user_data):
    update.message.reply_text("Пожалуйста введите ваше имя и фамилию ", reply_markup=ReplyKeyboardRemove())
    return "name"

def signup_get_name_and_surname(bot, update, user_data):
    name = update.message.text
    if len(name.split(' ')) != 2:
        update.message.reply_text('Пожалуйста введите ваше имя и фамилию через пробел')
        return "name"
    else:
        user_data['name and surname'] = name
        update.message.reply_text('Имя и фамилия сохранены. Пожалуйста введите желаемый логин, затем пароль через пробел')
    
    return "login_pas"

def signup_get_login_and_pas(bot, update, user_data):
    username = update.message.text
    if len(username.split(' ')) != 2:
        update.message.reply_text('Пожалуйста введите желаемый логин, затем пароль через пробел')
        return "login_pas"
    else:
        user_data['username and pas'] = username
        update.message.reply_text('Учетная запись создана .')    #TO-do
    
    return "account_created"


def signup_account_created(bot, update, user_data):
    text ='''    
    <b>Имя Фамилия</b> {signup_get_name_and_surname}
    <b>Логин</b> {signup_get_login_and_pas}'''.format(**user_data)
    update.message.reply_text(text, reply_markup = get_keybord(), parse_mode=ParseMode.HTML)
    


if __name__=='__main__':
    main()