from flask import Flask, render_template, redirect, url_for, flash
from forms import LoginForm
from services import SpaceGuideServices
import os

app = Flask(__name__)

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

        # Autenticação do usuário
        user = user_dao.get_user_by_id(username)
        if user and user.password == password:
            # Simples autenticação de senha; em produção, use hashes seguros
            return redirect(url_for('home', user_id=user.user_id))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html', form=form)

@app.route('/home/<user_id>')
def home(user_id):
    user = user_dao.get_user_by_id(user_id)
    if not user:
        return redirect(url_for('login'))
    return render_template('home.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)