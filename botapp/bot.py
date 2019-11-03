from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, CommandHandler, ConversationHandler, RegexHandler, Filters
import logging
from telegram import ReplyKeyboardRemove, ParseMode
import settings 
from handlers import *
#from botapp.config import SECRET_KEY
#from botapp.db import Session

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
level = logging.INFO,
filename ='bot.log')

def main():
    print('Start')
    logging.info ('Бот стартанул')
        
    bot = Bot(token=settings.TG_TOKEN)
    updater = Updater(bot=bot)
    dp = updater.dispatcher
    
    '''login = ConversationHandler(
        entry_points=[RegexHandler('^(login)$', login_start, pass_user_data=True)],
        states={
            "login_start": [RegexHandler('^(login_start)$', login_start, pass_user_data=True)],
            "login_check": [RegexHandler('^(login_check)$', login_check, pass_user_data=True)],
            "pas_start": [RegexHandler('^(pas_start)$', pas_start, pass_user_data=True)],
            "pas_check": [RegexHandler('^(pas_start)$', pas_start, pass_user_data=True)]
            },
        fallbacks=[]
    )'''
            
    signup = ConversationHandler(
        entry_points=[RegexHandler('^(Signup)$', signup_start, pass_user_data=True)],
        states={
            "name_and_surname": [MessageHandler(Filters.text, signup_get_name_and_surname, pass_user_data=True)],    #"name_and_surname": [RegexHandler(^(name_and_surname)$, signup_get_name_and_surname, pass_user_data=True)]
            "login_pas": [RegexHandler('^(login_pas)$', signup_get_login_and_pas, pass_user_data=True)],
            "account_created": [RegexHandler('^(account_created)$', signup_account_created, pass_user_data=True)]
            },
        fallbacks=[]
    )
    
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))    
    dp.add_handler(RegexHandler('^(Login)$', login_start, pass_user_data=True))
    #dp.add_handler(RegexHandler('^(Signup)$', signup, pass_user_data=True))
    #dp.add_handler(RegexHandler('^(name_and_surname)$', signup_get_name_and_surname, pass_user_data=True))
    #dp.add_handler(RegexHandler('^(login_pas)$', signup_get_login_and_pas, pass_user_data=True))
    #dp.add_handler(RegexHandler('^(account_created)$', signup_account_created, pass_user_data=True))
    
    dp.add_handler(signup)
    #dp.add_handler(login)
    
    #dp.add_handler(MessageHandler(Filters.text, do_echo) )
    updater.start_polling()
    updater.idle()




if __name__=='__main__':
    main()