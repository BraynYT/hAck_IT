from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from views import registration_service, login_service
from peewee import *
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from models import Users
from operations import checkUserAuthorization

SECRET_KEY = "tipoSecretKey"
DEBUG = True


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def loader_user(user_id):
    try:
        return Users.get(Users.id == user_id)
    except Users.DoesNotExist:
        return None

@app.route('/registration/', methods = ["GET","POST"])  
def registration():
    if request.method == 'POST':
        data = registration_service()
        if data == None:
            return redirect(url_for('login'))
        return render_template('register.html', message=data)
    
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = login_service()
        print(data)
        return render_template('login.html', message = data)
        
    return render_template('login.html')

@app.route("/home")
@login_required
def home():
    return render_template("home.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
    