from flask import Flask, g, redirect, url_for, request, session, render_template
from operations import addUser, deleteUser, checkUserAuthorization, add_topic
# from app import oid
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user

def registration_service():
    if request.method == 'POST':
        data = addUser(request.form['username'], generate_password_hash(request.form['password']), request.form['email'])

        return data
    
def login_service():
    if request.method == 'POST':
        status, user = checkUserAuthorization(request.form['username'], request.form['password'])
        print(status, user)
        if status == 0:
            login_user(user, remember=True)
            if (user.roles == 1):
                return user, redirect(url_for("admin"))
            return user, redirect(url_for("home"))
            
        else:
            return status


def topic_create():
    if request.method == 'POST':
        data = add_topic(request.form['topicTitle'], request.form['topicCategory'], request.form['topicContent'])
        return data