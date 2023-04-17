import json
import mysql.connector
from mysql.connector import Error
import jwt



conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    database="empresa"
)
        
cursor = conexao.cursor()

def Login( cpf, senhaT):
    senha = jwt.encode({'senha': senhaT}, "senha-padrão", algorithm='HS256')
    cursor.execute(f"SELECT ID FROM dadosfuncionarios WHERE CPF='{cpf}' AND SENHA='{senha}'")
    result = cursor.fetchone()
    if result:       
        return result[0]
    else:
        return None

def criarProjeto(nome, integrantes, ID_Projeto, Nome, Descricao, Data_Inicio, DURACAO):
    try:
        cursor.execute(
            f"INSERT INTO projetos (NOME_PROJETO, Id_integrante) VALUES ({nome}, {integrantes})",
        )
        conexao.commit()
        cursor.execute(
            f"INSERT INTO fase (ID_Projeto, Nome, Descricao, Data_Inicio, DURACAO) VALUES ({ID_Projeto},{Nome}, {Descricao}, {Data_Inicio}, {DURACAO} )",
        )
        return "Projeto criado com sucesso!"
    except Error as e:
        return f"Erro ao criar projeto: {e}"

def Funcionarios():
    cursor.execute("SELECT * FROM dadosfuncionarios")
    result = cursor.fetchall()
    return result

def InfoUser(id):
    cursor.execute(f"SELECT * FROM dadosfuncionarios Where ID={id}")
    result = cursor.fetchall()
    return result[0]

def criarUser(ID, NOME, CPF, EMAIL, NASCIMENTO, TELEFONE, SEXO, CARGO, SENHA):
    try:
        cursor.execute(
            "INSERT INTO usuarios (ID, NOME, CPF, EMAIL, NASCIMENTO, TELEFONE, SEXO, CARGO, SENHA) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (ID, NOME, CPF, EMAIL, NASCIMENTO, TELEFONE, SEXO, CARGO, SENHA)
        )
        conexao.commit()
        return "Usuário criado com sucesso!"
    except Error as e:
        return f"Erro ao criar usuário: {e}"

def RECemail( cpf):
    cursor.execute(f"SELECT email, TELEFONE FROM dadosfuncionarios WHERE CPF='{cpf}'")
    result = cursor.fetchone()
    if result:
        return result
    else:
        return -1

def Servicos():
    cursor.execute("SELECT * FROM dadosfuncionarios")
    result = cursor.fetchall()
    return result

def Agenda(dia):
    cursor.execute(f"SELECT * FROM agenda WHERE dia = '{dia}' ")
    result = cursor.fetchall()
    agenda_dict = {}
    for item in result:
        agenda_dict['Nome'] = item[0]
        agenda_dict['dia'] = item[1]
        agenda_dict['horario'] = item[2]
        agenda_dict['descricao'] = item[3]
    return json.dumps(agenda_dict)

def alterarSenha(email , senha):
    try:
        status = cursor.execute(f"UPDATE dadosfuncionarios SET SENHA = '{senha}' WHERE EMAIL = '{email}'")
        return 200
    except: 
        print(TypeError)
        return 400
def SaveImage(id, imagem):
    print(id)
    cursor.execute(f"UPDATE dadosfuncionarios SET PERFIL = %s WHERE ID = %s", (imagem, id))
    conexao.commit()
    result = cursor.fetchall()
    return result

def SendImage(id):
    cursor.execute(f"SELECT PERFIL FROM dadosfuncionarios WHERE ID={id}")
    result = cursor.fetchone()

    return result
