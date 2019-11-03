from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, CommandHandler, ConversationHandler, RegexHandler, Filters
import logging
from telegram import ReplyKeyboardRemove, ParseMode
import settings 

def greet_user(bot: Bot, update: Update, user_data):
    text = '''Привет! Данный бот предназначен для взаимодействия с сервисом Blood_pressure. Если вы зарегистрированы нажмите Login, если не зарегистрированы нажмите Signup."
           '''
    my_keybord = ReplyKeyboardMarkup([['Login','Signup']])       #,['/input pressure data']
    update.message.reply_text(text, reply_markup=my_keybord)

def do_echo(bot:Bot, update: Update):
    text = update.message.text
    bot.send_message(chat_id=update.message.chat_id,
    text=text)

def get_keybord():
    pass

def signup_start(bot, update, user_data):
    update.message.reply_text("Пожалуйста введите ваше имя и фамилию ", reply_markup=ReplyKeyboardRemove())
    logging.info('Запущена  signup_start')
    return "name_and_surname"

def signup_get_name_and_surname(bot, update, user_data):  #добавить проверку 
    logging.info('Запущена  signup_get_name_and_surname')
    name = update.message.text
    
    if len(name.split(' ')) < 2:
        vvod = len(name.split(' '))
        update.message.reply_text(f'  {vvod} Пожалуйста введите ваше имя и фамилию через пробел')
        logging.info(f' vvod {vvod} Запущена  signup_get_name_and_surname  юзер ввел не 2 строки')
        return "name_and_surname"
    else:
        user_data['name and surname'] = name
        logging.info('Запущена  signup_get_name_and_surname  юзер ввел  2 строки. Имя и фамилия сохранены')
        update.message.reply_text(f'{name} Имя и фамилия сохранены. Пожалуйста введите желаемый логин, затем пароль через пробел')
        return "login_pas"
    '''
    user_data['name and surname'] = name
    logging.info('Запущена  signup_get_name_and_surname  юзер ввел  2 строки. Имя и фамилия сохранены')
    update.message.reply_text('Имя и фамилия сохранены. Пожалуйста введите желаемый логин, затем пароль через пробел')
    return "login_pas"
    '''

def signup_get_login_and_pas(bot, update, user_data):
    username = update.message.text    # добавить проверка недопустимые символы #проверка существования в БД
    if len(username.split(' ')) < 2:
        vvod1 = len(username.split(' '))
        update.message.reply_text(f' {vvod1} Пожалуйста введите желаемый логин, затем пароль через пробел')  #TO-do добавить экспорт в БД
        logging.info(f' {vvod1} Запущена signup_get_login_and_pas юзер ввел не 2 строки')
        return "login_pas"
    else:
        user_data['username and pas'] = username
        logging.info('Запущена signup_get_login_and_pas Учетная запись создана .')
        update.message.reply_text('Учетная запись создана .')    #TO-do добавить экспорт в БД
        return "account_created"    

def signup_account_created(bot, update, user_data):
    logging.info('Запущена signup_get_login_and_pas Учетная запись создана.')
    text ='''    
    <b>Имя Фамилия</b> {signup_get_name_and_surname}
    <b>Логин</b> {signup_get_login_and_pas}'''.format(**user_data)
    update.message.reply_text(text, reply_markup = get_keybord(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END
   

def login_start(bot, update, user_data):
    logging.info('Запущена login_start ')
    #text = 'Введите логин'           
    #my_keybord = ReplyKeyboardMarkup([['Password'],['Ok'],['Cancel']])       #,['/input pressure data']
    #update.message.reply_text(text, reply_markup=my_keybord)
    update.message.reply_text('Введите логин')
    return "login_check"

def login_check(bot, update, user_data):
    user_list = ['Vasya', 'admin', 'testuser', 'god96']
    forbidden_chars = ['@', ' ']
    username = update.message.text
    logging.info(f'Запущена login_check пользователь ввел {username}')
    if len(username.split) < 5 or len(username.split) > 20:   #проверка пустой\не пустой, длина логина не менее 6 не более 20
        update.message.reply_text("Логин должен начинаться с буквы и состоять не менее чем из 5 символов и не более чем из 20 символов. Попробуйте ввести логин ешё раз")
        return "login_check"
    elif len(list(set(username.split) & set(forbidden_chars))) != 0:   #проверка недопустимые символы ("@" " ")
        check_forbidden_chars=list(set(username.split) & set(forbidden_chars))
        update.message.reply_text(f"Введенный логин содержит недопустимые символы {check_forbidden_chars}. Введите другой логин")
        logging.info(f'login_check Введенный логин содержит недопустимые символы {check_forbidden_chars}')
        return "login_check" 
    elif username in user_list != True: #допилить проверку наличия в БД:
        update.message.reply_text(f"Пользователя с логином {username} не существует. Зарегистрируйтесь или введите другой логин")
        logging.info(f"Пользователя с логином {username} не существует. Зарегистрируйтесь или введите другой логин")
        return "login_check"
    else:
        update.message.reply_text(f"{username}, введите  пароль")
        return "pas_start"       
   
def pas_start(bot, update, user_data):
    pas_list = ['qwerty', '123456','godlike']
    logging.info(f"запущена pas_start")
    pas =  update.message.text  
    if len(pas.split) < 6 or len(pas.split) > 20:   #проверка пустой\не пустой, длина пароля не менее 6 не более 20
        update.message.reply_text("Пароль должен состоять не менее чем из 6 символов и не более чем из 20 символов. Попробуйте ввести пароль ешё раз")
        logging.info(f"Пароль должен состоять не менее чем из 6 символов и не более чем из 20 символов. Попробуйте ввести пароль ешё раз")
        return "pas_start"
    elif pas in pas_list == False:   
        update.message.reply_text("Введенный пароль неверный. Попробуйте ввести ешё раз")
        logging.info(f"Введенный пароль неверный.")
        return "pas_start"
    else:
        update.message.reply_text("Введите данные")
        logging.info(f"Введенный пароль корректный.")
        return "start_blood_pressure"
