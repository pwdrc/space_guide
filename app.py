from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from forms import LoginForm
from services import SpaceGuideServices
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
        self.role = action.get_role_by_leader_id(user_id)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

action = SpaceGuideServices()
action.init_environment()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        login_successful = action.login(username, password)
        if login_successful:
            user = User(username)
            login_user(user)
            return redirect(url_for('home'))

        flash('An impostor! The Sideral Big Brother are staring your acts...', 'error')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)