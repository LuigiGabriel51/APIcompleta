import json
import sqlite3
import jwt



conexao = conn = sqlite3.connect('BD/BDsqliteEmpresa.db', check_same_thread=False)
        
cursor = conexao.cursor()

def Login( cpf, senhaT):
    try:
        #senha = jwt.encode({'senha': senhaT}, "senha-padrão", algorithm='HS256')
        cursor.execute(f"SELECT ID FROM dadosfuncionarios WHERE CPF='{cpf}' AND SENHA='{senhaT}'")
        result = cursor.fetchone()
        if result:       
            return result[0]
    except: 
        return 0

def criarProjeto(nome, integrantes):
    try:
        cursor.execute(
            f"INSERT INTO projetos (NOME_PROJETO, Id_integrante) VALUES ('{nome}', '{integrantes}')",
        )
        conexao.commit()
        return "Projeto criado com sucesso!"
    except:
        return f"Erro ao criar projeto"

def Funcionarios():
    cursor.execute("SELECT * FROM dadosfuncionarios")
    result = cursor.fetchall()
    return result

def InfoUser(id):
    cursor.execute(f"SELECT * FROM dadosfuncionarios Where ID={id}")
    result = cursor.fetchall()
    return result[0]

def criarUser(NOME, CPF, EMAIL, NASCIMENTO, TELEFONE, SEXO, CARGO, SENHA):
    try:
        cursor.execute(
                f"INSERT INTO dadosfuncionarios (NOME, CPF, EMAIL, NASCIMENTO, TELEFONE, SEXO, CARGO, SENHA) VALUES ('{NOME}', '{CPF}', '{EMAIL}', '{NASCIMENTO}', '{TELEFONE}', '{SEXO}', '{CARGO}', '{SENHA}')"
        )
        conexao.commit()


        return "Usuário criado com sucesso!"
    except:
        return f"Erro ao criar usuário"

def RECemail( cpf):
    cursor.execute(f"SELECT email, TELEFONE FROM dadosfuncionarios WHERE CPF='{cpf}'")
    result = cursor.fetchone()
    if result:
        return result
    else:
        return -1

def Servicos():
    cursor.execute("SELECT * FROM projetos")
    projetos = cursor.fetchall()
    cursor.execute("SELECT * FROM fase")
    fases = cursor.fetchall()
    
    projetos_fases = {}
    for projeto in projetos:
        id_projeto = projeto[0] # altere aqui o índice para corresponder à posição da coluna 'ID' na tabela 'projetos'
        nome_projeto = projeto[1]
        projetos_fases[nome_projeto] = []
        for fase in fases:
            if fase[1] == id_projeto: # altere aqui o índice para corresponder à posição da coluna 'id_projeto' na tabela 'fase'
                projetos_fases[nome_projeto].append(fase)
    
    return projetos_fases

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

def alterarSenha(cpf , senha):
    try:
        status = cursor.execute(f"UPDATE dadosfuncionarios SET SENHA = '{senha}' WHERE CPF = '{cpf}'")
        conexao.commit()


        return 200
    except: 
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
