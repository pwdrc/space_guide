from flask import Flask, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from forms import LoginForm
from flask import request
from services import SpaceGuideServices
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
        self.role = action.get_role(user_id)
        self.name = action.get_name(user_id)
        self.faccao = action.get_faccao(user_id)
        self.nacao = action.get_nacao(user_id)

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
            session['role'] = user.role
            session['name'] = user.name
            session['faccao'] = user.faccao
            print(f">>>>> Role: {user.role}")
            action.register_access(username, f'acesso em {datetime.now()}')
            return redirect(url_for('home'))

        flash('An impostor! The Sideral Big Brother are staring your acts...', 'error')
        action.register_access(username, f'acesso negado em {datetime.now()}')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    user_role = session.get('role')
    # eliminar espaço em branco
    user_name = session.get('name')
    if(user_role == 'LIDER_FACCAO'):
        user_faccao = session.get('faccao')
        return render_template('home.html', role=user_role, name=user_name, faccao=user_faccao)
    if(user_role == 'OFICIAL'):
        return render_template('home.html', role=user_role, name=user_name)
    if(user_role == 'COMANDANTE'):
        user_nacao = session.get('nacao')
        return render_template('home.html', role=user_role, name=user_name, nacao=user_nacao)
    return render_template('home.html', role=user_role, name=user_name)

@app.route('/relatorios')
@login_required
def relatorios():
    user_role = session.get('role')
    user_name = session.get('name')
    return render_template('relatorios.html', role=user_role, name=user_name)

# lider
@app.route('/lider/alterar_nome', methods=['POST'])
@login_required
def alterar_nome_faccao():
    if session.get('role') == 'LIDER_FACCAO':
        # Lógica para alterar o nome da facção
        novo_nome = request.form['novo_nome']
        action.alterar_nome_facacao(session.get('name'), novo_nome)
        flash('Nome da facção alterado com sucesso!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Acesso não autorizado', 'error')
        return redirect(url_for('home'))

@app.route('/lider/indicar_lider', methods=['POST'])
@login_required
def indicar_lider():
    if session.get('role') == 'LIDER_FACCAO':
        novo_lider = request.form['novo_lider']
        action.indicar_novo_lider(session.get('name'), novo_lider)
        flash('Novo líder indicado com sucesso!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Acesso não autorizado', 'error')
        return redirect(url_for('home'))

@app.route('/lider/credenciar_comunidade', methods=['POST'])
@login_required
def credenciar_comunidade():
    if session.get('role') == 'LIDER_FACCAO':
        comunidade = request.form['comunidade']
        planeta = request.form['planeta']
        action.credenciar_comunidade(session.get('name'), comunidade, planeta)
        flash('Comunidade credenciada com sucesso!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Acesso não autorizado', 'error')
        return redirect(url_for('home'))

@app.route('/lider/remover_nacao', methods=['POST'])
@login_required
def remover_nacao():
    if session.get('role') == 'LIDER_FACCAO':
        nacao = request.form['nacao']
        action.remover_nacao(session.get('name'), nacao)
        flash('Facção removida da nação com sucesso!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Acesso não autorizado', 'error')
        return redirect(url_for('home'))
    
@app.route('/comandante/add_nacao_federacao', methods=['POST'])
@login_required
def add_nacao_federacao():
    pass

@app.route('/comandante/rm_nacao_federacao', methods=['POST'])
@login_required
def rm_nacao_federacao():
    pass

@app.route('/comandante/criar_federacao', methods=['POST'])
@login_required
def criar_federacao():
    pass

# CRUD CIENTISTA para gerenciar estrelas
    
if __name__ == '__main__':
    app.run(debug=True)
