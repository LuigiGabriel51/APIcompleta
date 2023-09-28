import json
import sqlite3
import jwt



conexao = conn = sqlite3.connect('BD/BDsqliteEmpresa.db', check_same_thread=False)
        
cursor = conexao.cursor()

def Login( cpf, senhaT):
    try:
        #senha = jwt.encode({'senha': senhaT}, "senha-padrão", algorithm='HS256')
        cursor.execute(f"SELECT * FROM dadosfuncionarios WHERE CPF='{cpf}' AND SENHA='{senhaT}'")
        result = cursor.fetchone()
        if result:       
            return result
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

def criaFase(ID_Projeto, Nome, Descricao, Data_Inicio, DURACAO):
    try:
        cursor.execute(
            f"INSERT INTO fase (ID_Projeto, Nome, Descricao, Data_Inicio, DURACAO) VALUES ('{ID_Projeto}', '{Nome}', '{Descricao}', '{Data_Inicio}', '{DURACAO}')",
        )
        conexao.commit()
        return "Fase criado com sucesso!"
    except:
        return "Erro ao criar Fase"

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

def Servicos(id):
    cursor.execute(f"SELECT * FROM projetos WHERE ID = {id}")
    projetos = cursor.fetchall()
    cursor.execute(f"SELECT * FROM fase WHERE ID_Projeto = {id}")
    fases = cursor.fetchall()
    
    projetos_fases = {}
    for projeto in projetos:
        id_projeto = projeto[0] # Altere aqui o índice para corresponder à posição da coluna 'ID' na tabela 'projetos'
        nome_projeto = projeto[1]
        stringIntegrantes = projeto[2]
        status = projeto[3]
        image_projeto = str(projeto[4])
        ListIntegrantes = [int(numero) for numero in stringIntegrantes.split(',')]
        Integrantes = []

        for IDintegrante in ListIntegrantes:
            print(IDintegrante)
            cursor.execute(f"SELECT NOME FROM dadosfuncionarios WHERE ID = {IDintegrante}")
            integrante = cursor.fetchall()
            Integrantes.append(integrante)

        projetos_fases['PROJETO'] = {'nome': nome_projeto, 'integrantes': Integrantes,'fases': [], 'status': status, 'image': image_projeto}
        for fase in fases:
            if fase[1] == id_projeto: # Altere aqui o índice para corresponder à posição da coluna 'id_projeto' na tabela 'fase'
                projeto_fase = {
                    'id': fase[0],
                    'id_projeto': fase[1],
                    'nome_fase': fase[2],
                    'descricao_fase': fase[3],
                    'data_inicio': fase[4],
                    'valor': fase[5],
                    'concluido': fase[6]
                }
                projetos_fases['PROJETO']['fases'].append(projeto_fase)
    return projetos_fases

def Agenda(dia):
    cursor.execute(f"SELECT * FROM agenda WHERE dia = '{dia}' ")
    result = cursor.fetchall()
    if len(result) == 0:
        return None 
    Lista = []
    for item in result:
        Lista.append({
            "Nome": item[0],
            "dia": item[1],
            "horario": item[2],
            "descricao": item[3]
        })
    return Lista

def AddAgenda(Nome, dia, horario, descricao):
    try:
        cursor.execute(
            f"INSERT INTO agenda (Nome, dia, horario, descricao) VALUES ('{Nome}', '{dia}', '{horario}', '{descricao}')",
        )
        conexao.commit()
        return "agendado!"
    except:
        return "Erro ao agendar"

def alterarSenha(cpf , senha):
    try:
        cursor.execute(f"UPDATE dadosfuncionarios SET SENHA = '{senha}' WHERE CPF = '{cpf}'")
        rows_affected = cursor.rowcount
        conexao.commit()
        if rows_affected > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return False
    
    
def SaveImage(id, imagem):
    print(id)
    cursor.execute(f"UPDATE dadosfuncionarios SET PERFIL = ? WHERE ID = ?", (imagem, id))
    conexao.commit()
    result = cursor.fetchall()
    return result

def SendImage(id):
    cursor.execute(f"SELECT PERFIL FROM dadosfuncionarios WHERE ID={id}")
    result = cursor.fetchone()
    return result

def id_user(id):
    try:
        cursor.execute(f"SELECT * FROM dadosfuncionarios WHERE ID={id}")
        result = cursor.fetchone()
        if result:       
                return result
    except: 
        return 0

def UpdateData(cpf, email, telefone, sexo, cargo):
    try:
        cursor.execute(f"UPDATE dadosfuncionarios SET EMAIL = '{email}', TELEFONE = '{telefone}', SEXO = '{sexo}', CARGO = '{cargo}' WHERE CPF = '{cpf}'")
        rows_affected = cursor.rowcount
        if rows_affected > 0:
                return True
        else:
            return False
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return False
def EnviaMensagem(usuario, *args):
    try:
        cursor.execute(
            f"INSERT INTO chat (nome, msg, horario) VALUES ('{usuario}', '{args[0]}', '{args[1]}')",
        )
        conexao.commit()
        cursor.execute(f"SELECT * FROM chat WHERE id={usuario}")
        result = cursor.fetchone()
        return result
    except:
        return 200
def ChatGeral():
    cursor.execute(f"SELECT * FROM chat")
    result = cursor.fetchall()

    res = []
    for i in result:
        res.append([i[1],i[2],i[3]])
    return result
def UpdateImageProjeto(id, image):
        cursor.execute("UPDATE projetos SET Image = ? WHERE ID = ?", (image, id))
        conexao.commit()
        result = cursor.fetchall()
        return result  
def GetImageProjeto(id):
    cursor.execute(f"SELECT Image FROM projetos WHERE ID= {id}")
    result = cursor.fetchone()
    return result
def FuncionarioProjetos(id):
    funcionarios = cursor.execute(f"SELECT id_integrante FROM projetos WHERE ID= {id}")
    funcionarios = cursor.fetchall()
    string_com_numeros = funcionarios[0][0]  # Obter o valor da tupla

    funcionariosInt = string_com_numeros.split(',')
    funcionariosInt = [int(numero) for numero in funcionariosInt]

    listFunc = []
    for i in funcionariosInt:
        cursor.execute(f"SELECT NOME FROM dadosfuncionarios WHERE ID={i}")
        user = cursor.fetchall()
        if user:  # Verifica se a lista user não está vazia
            nome = user[0][0]  # Acessa o nome na primeira tupla da primeira lista
            listFunc.append(nome)
    return listFunc
def UpdateEmail(NovoEmail, ID):
    cursor.execute(f"""UPDATE dadosfuncionarios
                      SET EMAIL = '{NovoEmail}'
                      WHERE ID = {ID};""")
    rows_affected = cursor.rowcount
    conexao.commit()
    if rows_affected > 0:
        return True
    else:
        return False
    
