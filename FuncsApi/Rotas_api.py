import json
from flask import Flask, make_response,request, jsonify, Response
from FuncsApi.EmailAutomatico import enviar_email, envia_email_form
from functools import wraps
import jwt 
import datetime as dt
from flask_login import LoginManager
import BD.BancoDados as classeBD
from io import BytesIO


# criar rota de de lista de funcionarios no projeto & rota da imagem do projeto
class ServidorApp():

    def __init__(self):
        self.servidor = Flask(__name__)
        self.gerenciadorLogin = LoginManager()
        self.gerenciadorLogin.init_app(self.servidor)
        self.servidor.config["SECRET_KEY"] = "senha-padrão"

    def Inicialize(self):
        def jwt_required(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                token = request.headers.get('Authorization')
                print(token)
                if not token:
                    
                    return jsonify({
                        "verification": 404
                    }), 
                try:
                    jwt.decode(token, 'bagriel51', algorithms=["HS256"])
                except jwt.exceptions.DecodeError as e:
                    return jsonify({"verification": "Signature has expired"})
                return f(*args, **kwargs)
            return decorated

        #--------------------------------------------------rota de login---------------------------------------------------
        @self.servidor.route('/login', methods= ['POST'])
        def login():

            dados = request.get_json()
            cpf = dados['cpf']
            senha = dados['senha']
            info = classeBD.Login(cpf, senha)
            if info:
                payload = {
                    'user': info[0],
                    'exp': dt.datetime.now(tz=dt.timezone.utc) + dt.timedelta(minutes=20)
    }
                Token = jwt.encode(payload, 'bagriel51')
                response = jsonify({
                    'AccessToken': Token,
                    "id": info[0],
                    "Nome": info[1],
                    "Cpf": info[2],
                    "Email": info[3],
                    "Data": info[4],
                    "Numero": info[5],
                    "Sexo": info[6],
                    "Cargo": info[7]
                })
                response.status_code = 200
                return response

            else:
                # cria uma resposta com status 400 (Bad Request) e retorna uma mensagem de erro em formato JSON
                response = jsonify({"AccessToken": "Acesso negado"})
                response.status_code = 400
                return response
                
        @self.servidor.route('/Validation')
        @jwt_required
        def Validation():
            try:
                token = request.headers.get('Authorization')
                decoded_token = jwt.decode(token, 'bagriel51', algorithms=['HS256'])
                user = decoded_token['user']
                info = classeBD.id_user(user)
                return jsonify({
                    'AccessToken': token,
                    "id": info[0],
                    "Nome": info[1],
                    "Cpf": info[2],
                    "Email": info[3],
                    "Data": info[4],
                    "Numero": info[5],
                    "Sexo": info[6],
                    "Cargo": info[7]
                })
            except jwt.InvalidTokenError:
                print("Token inválido")

        #----------------------------------------------rota de serviços-----------------------------------------------

        @self.servidor.route('/adicionarProjeto', methods=['POST'])
        #@jwt_required
        def adicionarProjeto():
            
            requisicao = request.get_json()
            nome = requisicao['nome']
            participantes = requisicao['IDs']
            
            resultado = classeBD.criarProjeto(nome, participantes)
            return resultado

        #----------------------------------------------rota de funcionarios-------------------------------------------

        @self.servidor.route("/Listafuncionarios", methods=['GET'])
        #@jwt_required
        def listaFuncionarios():
            
            TabelaFuncionarios = classeBD.Funcionarios()
            tabelaFormatada = []
            for i in TabelaFuncionarios:
                tabelaFormatada.append(
                    [{
                        "id": i[0],
                        "Nome": i[1],
                        "Cpf": i[2],
                        "Email": i[3],
                        "Data": i[4],
                        "Numero": i[5],
                        "Sexo": i[6],
                        "Cargo": i[7]
                    } 
                    ]                       
                )
            try:
                return tabelaFormatada
            except:
                return Response('Missing parameter', status=400)
                
                
        #-----------------------------------------------rota de registro-----------------------------------------------

        @self.servidor.route('/registro', methods=['POST'])
        #@jwt_required
        def registro():
            
            requisicao = request.get_json()
            nome = requisicao['nome']
            email = requisicao['email']
            cpf = requisicao['cpf']
            nasc = requisicao['nascimento']
            tel = requisicao['telefone']
            sexo = requisicao['sexo']
            cargo = requisicao['cargo']
            
            resultado = classeBD.criarUser(nome, cpf, email, nasc, tel, sexo, cargo)

            return resultado

        #---------------------------------------------rotas de recuperaçao de senha--------------------------------------

        @self.servidor.route('/pega_email_sms', methods = ['POST'])
        # @jwt_required
        def pega_email_sms():
            
            dados = request.get_json()
            cpf = dados['cpf']
            meiosDeContato = classeBD.RECemail(cpf)
            return jsonify(
                {
                    'email': meiosDeContato[0],
                    'telefone': meiosDeContato[1]
                })  
                
        @self.servidor.route('/envia_email', methods = ['POST'])
        #@jwt_required
        def envia_email():
            dados = request.get_json()
            email = dados['email']
            codigo = dados['codigo']
            status = enviar_email(email, codigo)
            return status

        #@self.servidor.route('/envia_sms', methods = ['POST'])
        #@jwt_required()
        #def envia_sms():
            dados = request.get_json()
            tel = dados['telefone']
            codigo = dados['codigo']
            status = sendMsg(tel,codigo)
            print(status)
            return Response('Missing parameter', status=400)

        #---------------------------------------------rota de mostrar serviços-------------------------------------------
        @self.servidor.route("/listaDeServicos")
        # @jwt_required
        def verServicos():
            id = request.args.get('id')
            if id == None:
                return make_response(Response(status=403))
            TabelaServicos = classeBD.Servicos(id)
            return TabelaServicos
        #---------------------------------------------rota de Agenda-----------------------------------------------------
        @self.servidor.route("/Agenda", methods = ["GET", "POST"])
        # @jwt_required
        def buscAgenda():
            dia = request.get_json()
            dia = dia['dia']
            TabelaServicos = classeBD.Agenda(dia)
            if TabelaServicos == None:
                return make_response(Response(status=400))
            return TabelaServicos
         

        #---------------------------------------------rota de chat-------------------------------------------
        @self.servidor.route("/chat", methods=["POST", 'GET'])
        # @jwt_required
        def Chat():
            dic = {}
            if request.method == 'POST':
                bodyMessage = request.get_json()
                mensagem = bodyMessage['Msgs']
                usuario = bodyMessage['Nome']
                agora = dt.datetime.now()
                dataFormatada = agora.strftime("%Y-%m-%d %H:%M:%S")
                resultado = classeBD.EnviaMensagem(usuario, mensagem, dataFormatada) 
                chat = classeBD.ChatGeral()
                if chat != None:
                    chat1 = []
                    for i in chat:
                        chat1.append(
                            [
                                {
                                    "id": i[0],
                                    "Nome": i[1],
                                    "Msgs": i[2],
                                    "Horario": i[3]
                                }
                            ]
                        )
                    return chat1
                else: return make_response(Response(status=400))
            
            chat = classeBD.ChatGeral()
            print(chat)
            if chat != None:
                chat1 = []
                for i in chat:
                    chat1.append(
                        [
                            {
                                "id": i[0],
                                "Nome": i[1],
                                "Msgs": i[2],
                                "Horario": i[3]
                            }
                        ]
                    )
                return chat1
            return make_response(Response(status=400))
        
        #---------------------------------------------rota para alterar a senha-------------------------------------------
        @self.servidor.route("/NovaSenha", methods=['POST'])
        def novaSenha():
            dados = request.get_json()
            cpf = dados['cpf']
            senha = dados['senha']
            #Senha = jwt.encode({'senha': senha}, "senha-padrão", algorithm='HS256')
            sstatus = classeBD.alterarSenha(cpf, senha)
            if sstatus: return make_response(Response(status=200))
            return make_response(Response(status=400))
             
        #---------------------------------------------rota para receber imagem-------------------------------------------
        @self.servidor.route('/uploadImage', methods=['POST'])
        def upload_file():
            
            
            if 'file' not in request.files:
                return {'error': 'Nenhum arquivo enviado'}

            file = request.files['file']
            id = request.form['id']
            image = file.read()
            
            if file.filename == '':
                return {'error': 'O arquivo não possui um nome válido'}
            
            res = classeBD.SaveImage(id, image)

            return {'message': 'Arquivo enviado com sucesso'}
        
        #---------------------------------------------rota para buscar imagem-------------------------------------------
        @self.servidor.route('/sendImagePerfil', methods = ['POST'])
        #@jwt_required
        def sendImagePerfil():
            id = request.get_json()
            id = id['id']
            print(id)
            image = classeBD.SendImage(id)

            if image:
                image_data = image[0]

                # Cria um objeto BytesIO para armazenar a imagem como um fluxo de bytes
                img_io = BytesIO(image_data)

                # Define os cabeçalhos HTTP para a resposta
                response = make_response(img_io.getvalue())
                response.headers.set('Content-Type', 'image/jpeg')
                response.headers.set('Content-Disposition', 'attachment', filename='image.jpg')

                return response
            return Response(status=401)

        #---------------------------------------------rota para editar dados-------------------------------------------
        
        @self.servidor.route("/editData", methods = ["POST"])
        def editData():
            json = request.get_json()
            cpf = json['cpf']
            email = json['email']
            telefone = json['telefone']
            sexo = json['sexo']
            cargo = json['cargo']
            status = classeBD.UpdateData(cpf,email,telefone,sexo,cargo)
            if status: return make_response(Response(status=200))
            return make_response(Response(status=400))
        
        #---------------------------------------------rota de suporte--------------------------------------------------
        @self.servidor.route('/suporteForms', methods= ['POST'])
        def suporteForms():
            req = request.get_json()
            nome = req['nome']
            email = req['email']
            tel = req['tel']
            cargo = req['cargo']
            motivo = req['motivo']
            mensagem = req['mensagem']
            email_sup = 'luigiskyline4@gmail.com'
            msg = envia_email_form(email_sup,nome, email,tel,cargo, motivo, mensagem)
            return make_response(Response(status=200))
        
        @self.servidor.route("/ListaFuncionariosProjeto", methods= ['POST'])
        def listFuncionarios():
            projeto = request.get_json()
            idProjto = projeto["ID"]
            funcionarios = classeBD.FuncionarioProjetos(idProjto)
            
            return funcionarios

        @self.servidor.route('/uploadImageProjeto', methods=['POST'])
        def uploadImageProjeto():
            
            
            if 'file' not in request.files:
                return {'error': 'Nenhum arquivo enviado'}

            file = request.files['file']
            id = request.form['id']
            image = file.read()
            
            if file.filename == '':
                return {'error': 'O arquivo não possui um nome válido'}
            
            res = classeBD.UpdateImageProjeto(id, image)

            return {'message': 'Arquivo enviado com sucesso'}

        @self.servidor.route('/sendImageProjeto', methods = ['POST'])
        #@jwt_required
        def sendImageProjeto():
            id = request.get_json()
            id = id['id']
            print(id)
            image = classeBD.GetImageProjeto(id)

            if image:
                image_data = image[0]

                # Cria um objeto BytesIO para armazenar a imagem como um fluxo de bytes
                img_io = BytesIO(image_data)

                # Define os cabeçalhos HTTP para a resposta
                response = make_response(img_io.getvalue())
                response.headers.set('Content-Type', 'image/jpeg')
                response.headers.set('Content-Disposition', 'attachment', filename='image.jpg')

                return response
            return Response(status=401)
        
        @self.servidor.route('/UpdateEmail', methods = ['POST'])
        #@jwt_required
        def UpdateEmail():
            dados = request.get_json()
            NovoEmail = dados['email']
            id = dados['id']
            state = classeBD.UpdateEmail(NovoEmail, id)
            if state: 
                return make_response(Response(status=200))
            return make_response(Response(status=401))
        
        self.servidor.run(host="0.0.0.0", debug=True)
