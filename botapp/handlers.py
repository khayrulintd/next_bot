from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler
import logging
from telegram import ReplyKeyboardRemove


def greet_user(bot: Bot, update: Update, user_data):
    text = 'Привет! Данный бот предназначен для взаимодействия с сервисом \
Blood_pressure. Если вы зарегистрированы нажмите Login, если не \
зарегистрированы нажмите Signup.'
    my_keybord = ReplyKeyboardMarkup([['Login'], ['Signup']])
    update.message.reply_text(text, reply_markup=my_keybord)


def do_echo(bot: Bot, update: Update):
    text = update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=text)


def signup_start(bot, update, user_data):
    update.message.reply_text('Пожалуйста введите ваше имя и фамилию',
                              reply_markup=ReplyKeyboardRemove())
    logging.info('Запущена  signup_start')
    user_data['id'] = 0
    return "name_and_surname"


def signup_get_name_and_surname(bot, update, user_data):
    forbidden_digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    logging.info('Запущена  signup_get_name_and_surname')
    name = update.message.text
    if len(name.split(' ')) < 2:
        input = len(name.split(' '))
        update.message.reply_text(f'{input} Пожалуйста введите ваше имя и \
фамилию через пробел')
        logging.info(f'input {input} Запущена  signup_get_name_and_surname \
юзер ввел не 2 строки')
        return "name_and_surname"
    elif len(list(set(list(name)) & set(forbidden_digits))) != 0:
        check_forbidden_digits = (list(set(list(name))
                                       & set(forbidden_digits)))
        update.message.reply_text(f'ваш ввод {name} содержит цифры \
символы {check_forbidden_digits}. Попробуйте снова')
        logging.info(f'ввод {check_forbidden_digits} содержит цифры')
        return "name_and_surname"
    else:
        user_data['name'] = name.split(' ')[0]
        user_data['surname'] = name.split(' ')[1]
        logging.info(f'Запущена  signup_get_name_and_surname  юзер ввел  2 \
строки. Имя и фамилия сохранены {user_data}')
        update.message.reply_text(f'{name} Имя и фамилия сохранены. \
Пожалуйста введите ваш возраст')
        return "get_age"


def get_age(bot, update, user_data):
    logging.info(f'Запущена get_age {user_data}')
    age = update.message.text
    try:
        if 0 > int(age) or int(age) >= 110:
            update.message.reply_text(f'{age} введенный возраст вне \
нормального диапазона. Попробуйте ввести возраст снова')
            return "get_age"
        else:
            update.message.reply_text(f'{age} Возраст сохранен Пожалуйста \
введите желаемый логин, затем пароль через пробел')
            user_data['age'] = int(age)
            logging.info(f' get_age введен возраст {user_data}')
            return "login_pas"
    except ValueError:
        update.message.reply_text(f'{age} Вы ввели не число. Попробуйте \
снова')
        return "get_age"


def signup_get_login_and_pas(bot, update, user_data):
    username = update.message.text  # check недопустимые символы, наличие в БД
    if len(username.split(' ')) < 2:
        input1 = len(username.split(' '))  # TO-do добавить запись в БД
        update.message.reply_text(f' {input1} Пожалуйста введите желаемый \
логин. Логин должен начинаться с буквы и состоять не менее чем из 5 символов \
и  не более чем из 20 символов, затем пароль через пробел')
        logging.info(f'{input1} signup_get_login_and_pas юзер ввел не 2строки')
        return "login_pas"
    else:    # TO-do добавить запись в БД
        user_data['username'] = username.split(' ')[0]
        user_data['password'] = username.split(' ')[1]
        user_data['role'] = 'user'
        logging.info(f'Запущена signup_get_login_and_pas Учетная запись \
        создана. user_data {user_data}')
        update.message.reply_text(f'Учетная запись создана')
        return "account_created"


def signup_account_created(bot, update, user_data):
    logging.info(f'Запущена signup_get_login_and_pas Учетная запись создана. \
    user_data:{user_data}')
    update.message.reply_text(f'Запись создана')         
    return user_data, ConversationHandler.END


def login_start(bot, update, user_data):
    user_data['user_id'] = 1
    logging.info('Запущена login_start ')
    update.message.reply_text('Введите логин')
    return "login_check"


def login_check(bot, update, user_data):
    user_list = ['Vasya', 'admin', 'testuser', 'god96']
    forbidden_chars = ['@', ' ']  # можно дополнить список запрещенных символов
    username = update.message.text
    logging.info(f'Запущена login_check пользователь ввел {username} \
    {user_data}')
    if len(list(username)) < 5 or len(list(username)) > 20:
        update.message.reply_text('Логин должен начинаться с буквы и состоять \
не менее чем из 5 символов и не более чем из 20 символов. Попробуйте ввести \
логин ешё раз')
        return "login_check"
    elif len(list(set(list(username)) & set(forbidden_chars))) != 0:
        check_forbidden_chars = (list(set(list(username))
                                      & set(forbidden_chars)))
        update.message.reply_text(f'Введенный логин содержит недопустимые \
символы {check_forbidden_chars}. Введите другой логин')
        logging.info(f'login_check Введенный логин содержит недопустимые \
символы {check_forbidden_chars}')
        return "login_check"
    elif username not in user_list:  # допилить проверку наличия в БД:
        check_user_list = (list(set(list(username)) & set(user_list)))
        update.message.reply_text(f'Пользователя с логином {username} не \
существует. Зарегистрируйтесь или введите другой логин')
        logging.info(f'{check_user_list} Пользователя с логином {username} \
не существует. Зарегистрируйтесь или введите другой логин')
        return "login_check"
    else:
        user_data['username'] = str(username)
        update.message.reply_text(f'{username}, введите пароль')
        logging.info(f' ввод логина корректный {user_data}')
        return "pas_start"


def pas_start(bot, update, user_data):
    pas_list = ['qwerty', '123456', 'godlike']  # сравнить с паролем юзера в бд
    logging.info(f"запущена pas_start  user_data: {user_data}")
    pas = update.message.text
    if len(list(pas)) < 6:   # проверка длина пароля не менее 6 не более 20
        update.message.reply_text('Пароль должен состоять не менее чем из 6 \
символов и не более чем из 20 символов. Попробуйте ввести пароль ешё раз')
        logging.info(f'Пароль должен состоять не менее чем из 6 символов. \
        Попробуйте ввести пароль ешё раз')
        return "pas_start"
    elif pas not in pas_list:   # допилить сравнение с БД
        update.message.reply_text(f'Введенный пароль неверный. Попробуйте \
        ввести ешё раз')
        logging.info(f'Введенный пароль неверный.')
        return "pas_start"
    elif pas in pas_list:  # допилить сравнение с БД
        update.message.reply_text('Пароль корректный. Введите данные \
давления. Пример ввода: 120 80')
        logging.info(f'Введенный пароль корректный. user_data: {user_data}')
        return "start_blood_pressure"


def start_blood_pressure(bot, update, user_data):
    '''
    Артериальное давление   Систолическое АД         Диастолическое АД
     Норма                  120                      80
     Нормальное             121-130                  81-85
     Повышенное нормальное  131-140                  86-89
     1 стадия гипертонии    141-160                  90-100
     2 стадия               161-180                  101-110
     тяжелая гипертензия    Свыше 180                Свыше 110
    '''
    pressure = update.message.text
    logging.info(f"запущена start_blood_pressure user_data: {user_data}")
    try:
        sis_pressure = int(pressure.split(' ')[0])
        dias_pressure = int(pressure.split(' ')[1])
        if len(pressure.split(' ')) > 2:
            update.message.reply_text('Введено более 2х значений. Пример \
ввода: 120 80 Введите снова')
            logging.info(f'start_blood_pressure {pressure} Введено более 2х \
значений. Пример валидного ввода: 120 80  Введите снова')
            return "start_blood_pressure"
        else:
            user_data['sis_pressure'] = int(pressure.split(' ')[0])
            user_data['dias_pressure'] = int(pressure.split(' ')[1])
            # допилить запись в бд
            if sis_pressure == 120 and dias_pressure == 80:
                update.message.reply_text('Данные записаны, у вас идеальные \
показатели')
                logging.info(f'Данные записаны. user_data: {user_data}')
                return user_data, ConversationHandler.END
            elif (121 <= sis_pressure <= 130 and
                  81 <= dias_pressure <= 85):
                update.message.reply_text('Данные записаны, ваши показатели в \
норме')
                logging.info(f'Данные записаны. user_data: {user_data}')
                return user_data, ConversationHandler.END
            elif (131 <= sis_pressure <= 140 and
                  86 <= dias_pressure <= 89):
                update.message.reply_text('Данные записаны, ваши показатели \
слегка выше нормы')
                logging.info(f'Данные записаны. user_data: {user_data}')
                return user_data, ConversationHandler.END
            elif (141 <= sis_pressure <= 160 and
                  90 <= dias_pressure <= 100):
                update.message.reply_text('Данные записаны, у вас 1я стадия \
гипертонии')
                logging.info(f'Данные записаны. user_data: {user_data}')
                return user_data, ConversationHandler.END
            elif (161 <= sis_pressure <= 180 and
                  101 <= dias_pressure <= 110):
                update.message.reply_text('Данные записаны, у вас 2я стадия \
гипертонии ')
                logging.info(f'Данные записаны. user_data: {user_data}')
                return user_data, ConversationHandler.END
            elif (180 < sis_pressure and 110 < dias_pressure):
                update.message.reply_text('Данные записаны, у вас \
гипертонический криз')
                logging.info(f'Данные записаны. user_data: {user_data}')
                return user_data, ConversationHandler.END
            else:
                update.message.reply_text('Ваши данные не входят в \
стандартные категории. Попробуйте ввести снова')
                logging.info(f' start_blood_pressure user ввел {pressure} \
данные не входят в стандартные категории user_data: {user_data}')
                return "start_blood_pressure"
    except ValueError:
        update.message.reply_text(f'{pressure} Вы ввели не числа. Попробуйте \
снова')
        return "start_blood_pressure"
