from flask import Flask, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from forms import LoginForm
from flask import request
from services import SpaceGuideServices
from dao import DataBaseActions
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

action = SpaceGuideServices()
action.init_environment()

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
        self.role = action.get_role(user_id)
        self.name = action.get_name(user_id)
        self.faccao = action.get_faccao(user_id)
        self.nacao = action.get_nacao(user_id)
        self.is_leader = action.is_leader(user_id)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

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
            session['is_leader'] = user.is_leader
            print(f">>>>> Role: {user.role}")
            print(f">>>>> Lider: {user.is_leader}")
            action.register_access(username, f'acesso em {datetime.now()}')
            
            if session.get('is_leader') is True:
                return redirect(url_for('select_profile', role=session.get('role')))
            return redirect(url_for('home'))

        flash('An impostor! The Sideral Big Brother are staring your acts...', 'error')
        action.register_access(username, f'acesso negado em {datetime.now()}')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('role', None)
    session.pop('name', None)
    session.pop('faccao', None)
    session.pop('is_leader', None)
    return redirect(url_for('login'))

@app.route('/select_profile', methods=['GET', 'POST'])
@login_required
def select_profile():
    if request.method == 'POST':
        profile = request.form.get('profile')
        print(f"Perfil selecionado: {profile}")  # Log para verificar o valor de profile

        if profile == 'leader':
            # Redirecione para a rota correspondente ao perfil de líder
            name = session.get('name')
            faccao = session.get('faccao')
            print(f"Redirecionando para /leader com name: {name}, faccao: {faccao}")  # Log para depuração
            return redirect(url_for('leader', name=name, faccao=faccao))
        
        elif profile == 'outro_perfil':
            # Redirecione para a rota correspondente ao outro perfil
            name = session.get('name')
            print(f"Redirecionando para /home com name: {name}")  # Log para depuração
            return redirect(url_for('home', name=name))
        
        else:
            flash('Perfil inválido selecionado.', 'error')
            print("Perfil inválido selecionado.")  # Log para perfil inválido

    # Se não for um POST, simplesmente renderize o template de seleção de perfil
    role = session.get('role')  # Use um valor padrão caso 'role' não esteja na sessão
    return render_template('select_profile.html', role=role)

@app.route('/leader')
@login_required
def leader():
    return render_template('leader.html')

@app.route('/home')
@login_required
def home():
    user_role = session.get('role')
    #is_leader = session.get('is_leader', False)  # Assume False como padrão se não estiver definido
    #if is_leader:
    #    return redirect(url_for('select_profile'))    
    
    user_name = session.get('name')
    if(user_role == 'CIENTISTA'):
        return render_template('home.html', role=user_role, name=user_name)
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
    if user_role == 'LIDER_FACCAO':

# Para cada tipo de usuário, deve ser possível gerar relatórios claros e informativos, pensando na
# utilidade de cada relatório para seus respectivos usuários finais. É interessante, por exemplo,
# aplicar alguma ordenação/agrupamento que faça sentido em cada um dos relatórios.
# 1. Líder de facção:
# a. Informações sobre comunidades da própria facção: um líder de facção está
# interessado em recuperar informações sobre as comunidades participantes,
# facilitando a tomada de decisões de expansão da própria facção.
# i. Comunidades podem ser agrupadas por nação, espécie, planeta, e/ou
# sistema.

        user_faccao = session.get('faccao')
        # gerar um dict de comunidades só para teste
        comunidade = {'nome': 'comunidade1', 'nacao': 'nacao1', 'especie': 'especie1', 'planeta': 'planeta1', 'sistema': 'sistema1'}
        comunidades = [comunidade, comunidade, comunidade]
        return render_template('relatorios.html', role=user_role, name=user_name, faccao=user_faccao, comunidades=comunidades)

# # download_report lider_faccao
# @app.route('/download_report')
# @login_required
# def download_report():
#     user_role = session.get('role')
#     user_name = session.get('name')
#     if user_role == 'LIDER_FACCAO':
#         # gerar um relatório em excel
        

####################### lider faccao ######################

@app.route('/lider/alterar_nome', methods=['POST'])
@login_required
def alterar_nome_faccao():
    if session.get('role') == 'LIDER_FACCAO':
        # Lógica para alterar o nome da facção
        try:
            # pegar novo_nome do formulario em da pagina
            novo_nome = request.form['novo_nome']
            action.update_faccao(session.get('name'), novo_nome)
            flash('Nome da facção alterado com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao alterar nome da facção: {e}', 'error')
            return redirect(url_for('leader'))
    else:
        flash('Acesso não autorizado', 'error')
        return redirect(url_for('leader'))

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
