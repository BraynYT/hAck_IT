from models import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
import datetime
def addUser(username, password, email):
    db.connect()
    data = ''
    # user =
    if Users.get_or_none(Users.username == username):
        data = 'Пользователь уже зарегистрирован'
    else:
        Users.create(username = username, password = password, email = email, created_on = "1", roles = 0)
        data = None
    
    db.close()
    return data


def deleteUser(username, password):
    db.connect()
    if Users.get_or_none(Users.username == username):
        user = Users.get(Users.username == username)
        pass_check = check_password_hash(user.password, password)
        
        if (pass_check):
            user.delete_instance()
            data = "Пользователь удален!"
        else:
            data = "Неправильное имя"
    else:
        data = 2
    db.close()
    return data


def checkUserAuthorization(username, password):
    db.connect()
    user = Users.get_or_none(Users.username == username)
    user_data = None
    data = 'Пользователь не зареган'
    if (user):
        userPass = Users.get(Users.username == username)
        pass_check = check_password_hash(userPass.password, password)

        if (pass_check):
            data = 0 #"Авторизация прошла успешно!"
            user_data = userPass
        else:
            data = "Пароль введён не верно!"

    db.close()
    return data, user_data


def add_topic(title, category, content):
    topic = Topics.get_or_none(Topics.title == title)
    
    if (topic):
        return 1
        
    else:
        Topics.create(title = title, category = category, content = content)
        return 0
    
    
    

def add_message(topic, message_text, current_user):
    Messages.create(topic = topic, text=message_text, author = current_user)