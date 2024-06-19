# Documentação Séria do Projeto

## Visão Geral

### Tecnologias
- Python
- Flask
- Oracle SQL
- Tailwind CSS
- HTML
- JavaScript

### Estrutura de Pastas e Arquivos
- `app.py`: Arquivo principal do projeto. Contém a lógica de roteamento e renderização de páginas. 

- `config.py`: Arquivo com as configurações do projeto. Contém a classe `Config` que permite a configuração das variáveis para se conectar ao banco de dados.

- `dao.py`: Arquivo com as funções que fazem a comunicação direta com o banco de dados, como as chamadas dos pacotes e procedures, bem como trata a realização da comunicação em si.

- `services.py`: Arquivo com as funções que fazem a comunicação com o banco de dados, utilizando as funções do `dao.py`. É responsável por tratar os dados e retornar para o `app.py`. Funciona como uma camada intermediária entre o `app.py` e o `dao.py`.

- `requirements.txt`: Arquivo com as dependências do projeto, utilizado no processo de instalação.

- `templates/`: Pasta com os arquivos HTML.

- `static/`: Pasta com os arquivos estáticos (CSS).

- `scripts/`: Pasta com os scripts SQL.

### Arquitetura

- O projeto foi estruturado para permitir que diferentes usuários possam rodá-lo em suas próprias máquinas.

- O acesso ao banco de dados só está parcialmente pré-configurado, permitido que, em cada execução, o usuário possa informar suas próprias credenciais.

## Como instalar e rodar o projeto
- Instalar dependências
```bash
pip install -r requirements.txt
```
- Rodar os scripts no banco de dado

- Estar na rede USP ou VPN

- Executar
python app.py