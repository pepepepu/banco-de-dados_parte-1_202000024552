# Importação das bibliotecas necessárias
import datetime
from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields

# Definição do Flask e da API
app = Flask(__name__)
api = Api(app, version='1.0',
          title='Parte 1 - Banco de Dados - 202000024552',
          description='Desenvolvimento de uma API requerida para a primeira parte da disciplina Banco de Dados I do período letivo de 2023.1',
          doc='/doc',
          contact='Pedro Paulo Oliveira Barros Souza',
          contact_email='pedro.paulo@dcompu.ufs.br')

# Definição da classe Usuario
class Usuario:
    def __init__(self, cpf, nome, dataDeNascimento):
        self.cpf = cpf
        self.nome = nome
        self.dataDeNascimento = dataDeNascimento

    def retorna_usuario(self):
        return {
            'cpf': self.cpf,
            'nome': self.nome,
            'data': self.dataDeNascimento
        }

# Lista para armazenar os dados  
database = []
# Exemplo para consulta
database.append(Usuario(12345678910, 'Pedro Paulo', '10/07/2002'))

# Definição do modelo de usuário
modeloUsuario = api.model('Usuario', {
    'cpf': fields.Integer(required=True),
    'nome': fields.String(required=True),
    'data': fields.String(required=True)
})

# Rota para consulta de Usuário
@api.route('/usuarios/<int:cpf>')
class ConsultaDeUsuario(Resource):
    @api.doc(responses={200: 'Usuário encontrado', 404: 'Usuário não encontrado'},
             params={'cpf': {
                'description': 'Insira o CPF para realizar uma consulta de usuário',
                'example': 12345678910
             }},
             description='Consulta de usuário no Banco de Dados')
    
    def get(self, cpf):
        for user in database:
            if user.cpf == cpf:
                return jsonify(user.retorna_usuario())

        return {'message': 'O CPF inserido não corresponde a nenhum usuário existente no Banco de Dados'}, 404

# Rota para cadastro de Usuário
@api.route('/usuarios/cadastro')
class CadastroDeUsuarios(Resource):
    @api.doc(responses={201: 'Usuário cadastrado com sucesso', 400: 'Cadastro mal-sucedido'},
             params={'cpf':{'description': 'CPF do usuário', 'example': '12345678910'},
                     'nome':{'description': 'Nome do usuário', 'example': 'Nome SObrenome'},
                     'data':{'description': 'Data de nascimento do usuário', 'example': 'DD/MM/AAAA'}},
             description='Cadastro de usuário no Banco de Dados')
    
    @api.expect(modeloUsuario)
    def post(self):
        novo_usuario = request.get_json()

        cpf = novo_usuario.get('cpf')
        nome = novo_usuario.get('nome')
        data = novo_usuario.get('data')

        if not verificadorCPF(str(cpf)):
            return {'message': 'Insira um CPF válido'}, 400
        
        if not verificadorData(data):
            return {'message': 'Insira uma data válida'}, 400
        
        objeto_novo_usuario = Usuario(cpf, nome, data)

        database.append(objeto_novo_usuario)

        return {'message': 'Usuário cadastrado com sucesso'}, 201

# Função para verificar o formato do CPF
def verificadorCPF(cpf):
    return len(cpf) == 11 and cpf.isdigit()

# Função para verificar o formato da data
def verificadorData(data):
    try:
        datetime.datetime.strptime(data, '%d/%m/%Y')
        return True
    except ValueError:
        return False
    
if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)