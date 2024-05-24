from flask import Flask, render_template, redirect, url_for, flash
from forms import LoginForm
from services import SpaceGuideServices
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

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
        # role = action.login(username, password)
        # if role:
        #     return redirect(url_for('home', user_id=username))
        # else:
        #     flash('Login inválido. Tente novamente.', 'error')

        if action.login(username, password):
            return redirect(url_for('home', user_id=username))
        else:
            flash('Login inválido. Tente novamente.', 'error')
    # Renderiza o template de login se a requisição for um GET ou se os dados do formulário não passarem nas validações
    return render_template('login.html', form=form)


@app.route('/home/<user_id>')
def home(user_id):
    return render_template('home.html', user_id=user_id)

if __name__ == '__main__':
    app.run(debug=True)