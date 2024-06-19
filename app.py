from time import sleep
from flask import Flask, render_template, redirect, send_file, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from forms import LoginForm
from flask import request
from services import SpaceGuideServices
from datetime import datetime
import csv
from io import StringIO
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
            session['user_id'] = username
            print(f">>>>> Role: {user.role}")
            print(f">>>>> Lider: {user.is_leader}")
            
            if session.get('is_leader') is True:
                return redirect(url_for('select_profile', role=session.get('role')))
            return redirect(url_for('home'))

        flash('An impostor! The Sideral Big Brother are staring your acts...', 'error')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('role', None)
    session.pop('name', None)
    session.pop('faccao', None)
    session.pop('is_leader', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/select_profile', methods=['GET', 'POST'])
@login_required
def select_profile():
    if request.method == 'POST':
        profile = request.form.get('profile')
        print(f"Perfil selecionado: {profile}")  # Log para verificar o valor de profile

        is_leader = session.get('is_leader', False)  # Assume False como padrão se não estiver definido

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
            return redirect(url_for('home', name=name, is_leader=is_leader))
        
        else:
            flash('Perfil inválido selecionado.', 'error')
            print("Perfil inválido selecionado.")  # Log para perfil inválido

    # Se não for um POST, simplesmente renderize o template de seleção de perfil
    role = session.get('role')  # Use um valor padrão caso 'role' não esteja na sessão
    return render_template('select_profile.html', role=role)

@app.route('/leader')
@login_required
def leader():
    nome = session.get('name')
    faccao = session.get('faccao')
    return render_template('leader.html', name=nome, faccao=faccao)

@app.route('/home')
@login_required
def home():
    # registrar acesso
    user_role = session.get('role')
    #is_leader = session.get('is_leader', False)  # Assume False como padrão se não estiver definido
    #if is_leader:
    #    return redirect(url_for('select_profile'))    
    is_leader = session.get('is_leader', False)
    user_name = session.get('name')
    if(user_role == 'CIENTISTA'):
        return render_template('home.html', role=user_role, name=user_name, is_leader=is_leader)
    if(user_role == 'OFICIAL'):
        return render_template('home.html', role=user_role, name=user_name, is_leader=is_leader)
    if(user_role == 'COMANDANTE'):
        user_nacao = session.get('nacao')
        return render_template('home.html', role=user_role, name=user_name, nacao=user_nacao, is_leader=is_leader)
    return render_template('home.html', role=user_role, name=user_name)

@app.route('/relatorios')
@login_required
def relatorios():
    user_role = session.get('role')
    user_name = session.get('name')
    is_leader = session.get('is_leader', False)

    # comunidades = action.get_comunidades_by_faccao(session.get('faccao')) if is_leader else []
    r_habitacoes = action.relatorio_habitacao(session.get('user_id')) if user_role == 'OFICIAL' else []
    r_comunidades = action.relatorio_comunidades(session.get('user_id')) if is_leader else []
    r_nacoes = action.relatorio_nacoes(session.get('user_id')) if user_role == 'COMANDANTE' else []
    r_planetas_potenciais = action.relatorio_planetas_potenciais(session.get('user_id'), 100) if user_role == 'COMANDANTE' else []
    r_estrelas_sem_classificacao = action.relatorio_estrela_sem_classificacao() if user_role == 'CIENTISTA' else []
    r_planetas_sem_classificacao = action.relatorio_planeta_sem_classificacao() if user_role == 'CIENTISTA' else []

    print(f">>>>> Relatório de Habitacoes: {r_habitacoes}")
    print(f">>>>> Relatório de comunidades: {r_comunidades}")
    print(f">>>>> Relatório de nações: {r_nacoes}")
    print(f">>>>> Relatório de planetas potenciais: {r_planetas_potenciais}")
    print(f">>>>> Relatório de estrelas sem classificação: {r_estrelas_sem_classificacao}")
    print(f">>>>> Relatório de planetas sem classificação: {r_planetas_sem_classificacao}")
    
    #return render_template('relatorios.html', is_leader=is_leader, role=user_role, name=user_name,comunidades=comunidades, habitantes=habitantes, planetas=planetas)
    return render_template(
        'relatorios.html',
        is_leader=is_leader,
        role=user_role,
        name=user_name,
        habitacoes=r_habitacoes,
        comunidades=r_comunidades,
        nacoes=r_nacoes,
        planetas_potenciais=r_planetas_potenciais,
        estrelas_sem_classificacao=r_estrelas_sem_classificacao,
        planetas_sem_classificacao=r_planetas_sem_classificacao
    )

# @login_required
# def relatorios():
#     user_role = session.get('role')
#     user_name = session.get('name')
#     is_leader = session.get('is_leader', False)  # Assume False como padrão se não estiver definido
#     # if user_role == 'LIDER_FACCAO':

#     #     user_faccao = session.get('faccao')
#     #     # gerar um dict de comunidades só para teste
#     comunidade = {'nome': 'comunidade1', 'nacao': 'nacao1', 'especie': 'especie1', 'planeta': 'planeta1', 'sistema': 'sistema1'}
#     comunidades = [comunidade, comunidade, comunidade]
#     return render_template('relatorios.html', is_leader=is_leader, role=user_role, name=user_name, comunidades=comunidades)

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
    try:
        novo_nome = request.form['novo_nome']
        action.update_faccao(session.get('user_id'), novo_nome)
        flash('Ação realizada com sucesso!', 'SUCESSO_1')

        #session['msg'] = 'Nome da facção alterado com sucesso!'
        return redirect(url_for('leader'))
    except Exception as e:
        print(f'Erro ao alterar nome da facção: {e}')
        flash('Erro ao realizar ação.', 'ERRO_1')
        #session['msg'] = f'Erro ao alterar nome da facção: {e}'
        return redirect(url_for('leader'))

@app.route('/lider/indicar_lider', methods=['POST'])
@login_required
def indicar_lider():
    try:
        novo_lider = request.form['novo_lider']
        action.update_lider(session.get('user_id'), novo_lider)
        flash('Ação realizada com sucesso! Você foi deslogado...', 'SUCESSO_2')
        sleep(2)
        logout_user()

        return redirect(url_for('leader'))
    except Exception as e:
        flash('Erro ao realizar ação.', 'ERRO_2')
        return redirect(url_for('leader'))

@app.route('/lider/credenciar_comunidade', methods=['POST'])
@login_required
def credenciar_comunidade():
    try:
        especie = request.form['especie']
        comunidade = request.form['comunidade']
        action.add_comunidade(session.get('user_id'), especie, comunidade)
        flash('Ação realizada com sucesso!', 'SUCESSO_3')
        return redirect(url_for('leader'))
    except Exception as e:
        flash('Erro ao realizar ação.', 'ERRO_3')
        return redirect(url_for('leader'))

@app.route('/lider/remover_nacao', methods=['POST'])
@login_required
def remover_nacao():
    try:
        nacao = request.form['nacao']
        action.rm_nacao(session.get('user_id'), nacao)
        flash('Ação realizada com sucesso!', 'SUCESSO_4')
        return redirect(url_for('leader'))
    except Exception as e:
        flash('Erro ao realizar ação.', 'ERRO_4')
        return redirect(url_for('leader'))

# COMANDANTE

@app.route('/comandante/add_nacao_federacao', methods=['POST'])
@login_required
def add_nacao_federacao():
    try:
        federacao = request.form['add_federacao']
        action.add_nacao_federacao(session.get('user_id'), federacao)
        flash('Ação realizada com sucesso!', 'SUCESSO_5')
        return redirect(url_for('home'))
    except Exception as e:
        flash('Erro ao realizar ação.', 'ERRO_5')
        return redirect(url_for('home'))

@app.route('/comandante/rm_nacao_federacao', methods=['POST'])
@login_required
def rm_nacao_federacao():
    try:
        excluir = request.form['rm_federacao']
        if excluir == 'EXCLUIR':
            action.rm_nacao_federacao(session.get('user_id'))
            flash('Ação realizada com sucesso!', 'SUCESSO_6')
        else:
            flash('Erro ao realizar ação.', 'ERRO_6')
        return redirect(url_for('home'))
    except Exception as e:
        flash('Erro ao realizar ação.', 'ERRO_6')
        return redirect(url_for('home'))

@app.route('/comandante/criar_federacao', methods=['POST'])
@login_required
def criar_federacao():
    try:
        nome = request.form['nova_federacao']
        action.criar_nacao_federacao(session.get('user_id'), nome)
        flash('Ação realizada com sucesso!', 'SUCESSO_7')
        return redirect(url_for('home'))
    except Exception as e:
        flash('Erro ao realizar ação.', 'ERRO_7')
        return redirect(url_for('home'))
    
@app.route('/comandante/inserir_dominacao', methods=['POST'])
@login_required
def inserir_dominacao():
    try:
        nome = request.form['nova_dominacao']
        action.add_dominancia(session.get('user_id'), nome)
        flash('Ação realizada com sucesso!', 'SUCESSO_7')
        return redirect(url_for('home'))
    except Exception as e:
        flash('Erro ao realizar ação.', 'ERRO_7')
        return redirect(url_for('home'))

# CRUD CIENTISTA para gerenciar estrelas
# def add_estrela(self,ID,Nome,Classificao,Massa,X,Y,Z):
#         self.service.Cria_Estrela(ID,Nome,Classificao,Massa,X,Y,Z)

#     def add_sistema(self,Estrela,Nome):
#         self.service.Cria_Sistema(Estrela,Nome)
    
#     def add_orbita_estrela(self,Orbitante,Orbitada,Dist_Min,Dist_Max,Periodo):
#         self.service.Cria_Oribta_Estrela(Orbitante,Orbitada,Dist_Min,Dist_Max,Periodo)
    
#     def relatorio_estrela_sem_classificacao(self):
#         return self.service.Estrelas_Sem_Classificao()
    
#     def relatorio_planeta_sem_classificacao(self):
#         return self.service.Planetas_Sem_Classificao()
@app.route('/cientista/add_estrela', methods=['POST'])
@login_required
def add_estrela():
    try:
        id = request.form['ID']
        nome = request.form['nome']
        classificacao = request.form['classificacao']
        massa = request.form['massa']
        x = request.form['X']
        y = request.form['Y']
        z = request.form['Z']
        action.add_estrela(id, nome, classificacao, massa, x, y, z)
        flash('Ação realizada com sucesso!', 'SUCESSO_8')
        return redirect(url_for('home'))
    except Exception as e:
        flash('Erro ao realizar ação.', 'ERRO_8')
        return redirect(url_for('home'))
    
@app.route('/cientista/add_sistema', methods=['POST'])
@login_required
def add_sistema():
    try:
        estrela = request.form['estrela']
        nome = request.form['sistema']
        action.add_sistema(estrela, nome)
        flash('Ação realizada com sucesso!', 'SUCESSO_9')
        return redirect(url_for('home'))
    except Exception as e:
        flash('Erro ao realizar ação.', 'ERRO_9')
        return redirect(url_for('home'))

@app.route('/cientista/add_orbita_estrela', methods=['POST'])
@login_required
def add_orbita_estrela():
    try:
        orbitante = request.form['orbitante']
        orbitada = request.form['orbitada']
        dist_min = request.form['distancia_min']
        dist_max = request.form['distancia_max']
        periodo = request.form['periodo']
        action.add_orbita_estrela(orbitante, orbitada, dist_min, dist_max, periodo)
        flash('Ação realizada com sucesso!', 'SUCESSO_10')
        return redirect(url_for('home'))
    except Exception as e:
        flash('Erro ao realizar ação.', 'ERRO_10')
        return redirect(url_for('home'))
    
if __name__ == '__main__':
    app.run(debug=True)
