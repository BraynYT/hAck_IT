from flask import Flask, render_template, request, redirect, url_for
from views import registration_service, login_service, topic_create
from operations import add_message
from peewee import *
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import Users, Topics

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
        global current_user
        login_service()
        return redirect(url_for("home"))
        
    return render_template('login.html')

@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        data = topic_create()
        print(data)
    
    topics = Topics.select()
    print(topics)
    topics_by_category = {}
    for topic in topics:
        if topic.category not in topics_by_category:
            topics_by_category[topic.category] = []
        topics_by_category[topic.category].append(topic)
    return render_template("home.html", topics_by_category = topics_by_category)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/topic/<int:topic_id>', methods=['GET', 'POST'])
def topic(topic_id):
    topic = Topics.get_by_id(topic_id)

    if request.method == 'POST':
        add_message(topic, request.form['messageText'], current_user)
        return redirect(url_for('topic', topic_id=topic.id))
    return render_template('topic.html', topic=topic)

@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = Users.get_by_id(user_id)
    return render_template('profile.html', user=user)

if __name__ == "__main__":
    app.run(debug=True)
    