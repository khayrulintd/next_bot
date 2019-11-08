from telegram import Bot
from telegram.ext import Updater, MessageHandler, CommandHandler
from telegram.ext import ConversationHandler, RegexHandler, Filters
import logging
import config
from handlers import greet_user, signup_start
from handlers import signup_get_name_and_surname, signup_get_login_and_pas
from handlers import signup_account_created, login_start, login_check
from handlers import pas_start, start_blood_pressure, get_age

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO, filename='bot.log')


def main():
    print('Start')
    logging.info('Бот стартанул')
    bot = Bot(token=config.TG_TOKEN)
    updater = Updater(bot=bot)
    dp = updater.dispatcher

    login = ConversationHandler(
        entry_points=[RegexHandler('^(Login)$', login_start,
                                   pass_user_data=True)],
        states={            
            "login_check": [MessageHandler(Filters.text, login_check,
                                           pass_user_data=True)],
            "pas_start": [MessageHandler(Filters.text, pas_start,
                                         pass_user_data=True)],
            "start_blood_pressure": [MessageHandler(Filters.text,
                                                    start_blood_pressure,
                                                    pass_user_data=True)]
            },
        fallbacks=[]
    )

    signup = ConversationHandler(
        entry_points=[RegexHandler('^(Signup)$', signup_start,
                                   pass_user_data=True)],
        states={
            "name_and_surname": [MessageHandler(Filters.text,
                                                signup_get_name_and_surname,
                                                pass_user_data=True)],
            "get_age": [MessageHandler(Filters.text, get_age,
                                       pass_user_data=True)],
            "login_pas": [MessageHandler(Filters.text,
                                         signup_get_login_and_pas,
                                         pass_user_data=True)],
            "account_created": [MessageHandler(Filters.text,
                                               signup_account_created,
                                               pass_user_data=True)]
            },
        fallbacks=[]
    )

    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(signup)
    dp.add_handler(login)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
