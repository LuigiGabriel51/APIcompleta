from flask import Flask, make_response,request, jsonify, Response
from FuncsApi.EmailAutomatico import enviar_email
from FuncsApi.SMSautomatico import sendMsg
from functools import wraps
import jwt 
import datetime as dt
from flask_login import LoginManager
import BD.BancoDados as classeBD
from io import BytesIO



class ServidorApp():

    def __init__(self):
        self.servidor = Flask(__name__)
        self.gerenciadorLogin = LoginManager()
        self.gerenciadorLogin.init_app(self.servidor)
        self.servidor.config["SECRET_KEY"] = "senha-padrão"

    def InicializaServidor(self):
    
        def jwt_required(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                token = request.args.get('token')
                print(token)
                if not token:
                    
                    return jsonify({
                        "verification": 404
                    }), 
                try:
                    data = jwt.decode(token, 'bagriel51', algorithms=["HS256"])
                except: return jsonify({ "verification": 403})
                return f(*args, **kwargs)
            return decorated

        #--------------------------------------------------rota de login---------------------------------------------------
        @self.servidor.route('/login', methods= ['POST'])
        def login():

            requisicao = request.get_json()
            cpf = requisicao['cpf']
            senha = requisicao['senha']
            UserID = classeBD.Login(cpf, senha)

            if UserID:
                agora = dt.datetime.now()
                tempoExpiracao = dt.timedelta(weeks=8)
                
                Token = jwt.encode({'user': UserID,'exp': agora+tempoExpiracao}, 'bagriel51')
                return jsonify({
                        'UserID':UserID,
                        'AcessToken': Token
                        })

            else:
                return jsonify({
                "AcessToken": "acesso negado"
                }), 401
                
            
            # return redirect(login)
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
            except TypeError:
                return Response('Missing parameter', status=400)
            
        @self.servidor.route("/informacoesDoUsuario", methods=['POST'])
        #@jwt_required
        def InfoUser():
            
            req = request.get_json()
            id = req['id']
            info = classeBD.InfoUser(id)
            try:
                return jsonify({
                    "id": info[0],
                        "Nome": info[1],
                        "Cpf": info[2],
                        "Email": info[3],
                        "Data": info[4],
                        "Numero": info[5],
                        "Sexo": info[6],
                        "Cargo": info[7],
                })
            except TypeError:
                return Response('Missing parameter', status=400)
                
                
        #-----------------------------------------------rota de registro-----------------------------------------------

        @self.servidor.route('/registro', methods=['POST'])
        #@jwt_required()
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

        #---------------------------------------------rota de recuperaçao de senha--------------------------------------


        @self.servidor.route('/pega_email_sms', methods = ['POST'])
        # @jwt_required()
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
        #@jwt_required()
        def envia_email():
            dados = request.get_json()
            email = dados['email']
            codigo = dados['codigo']
            status = enviar_email(email, codigo)
            return status

        @self.servidor.route('/envia_sms', methods = ['POST'])
        #@jwt_required()
        def envia_sms():
            dados = request.get_json()
            tel = dados['telefone']
            codigo = dados['codigo']
            status = sendMsg(tel,codigo)
            print(status)
            return Response('Missing parameter', status=400)



        #---------------------------------------------rota de mostrar serviços-------------------------------------------
        @self.servidor.route("/listaDeServicos")
        # @jwt_required()
        def verServicos():
            
            
            TabelaServicos = classeBD.Servicos()
            TabelaServicos
            return jsonify(
                {
                    "Servicos": TabelaServicos
                }
            )
        
        @self.servidor.route("/Agenda", methods = ["GET", "POST"])
        # @jwt_required()
        def buscAgenda():
            dia = request.get_json()
            dia = dia['dia']
            TabelaServicos = classeBD.Agenda(dia)
            print(TabelaServicos)
            return TabelaServicos
         


        @self.servidor.route("/chat", methods=["POST", 'GET'])
        # @jwt_required()
        def Chat():
            dic = {}
            if request.method == 'POST':
                bodyMessage = request.get_json()
                mensagem = bodyMessage['msg']
                usuario = bodyMessage['user']
                agora = dt.datetime.now()
                dataFormatada = agora.strftime("%Y-%m-%d %H:%M:%S")
                resultado = classeBD.EnviaMensagem(usuario, mensagem, dataFormatada) 
                chat = classeBD.ChatGeral()
                j=1
                for i in chat:
                    chave = f'Mensagem{j}'
                    valor = [i[0],i[1],i[2]]
                    dic[chave] = valor
                    j+=1
                return resultado
                
            else:
                chat = classeBD.ChatGeral()
                j=1
                for i in chat:
                    chave = f'Mensagem{j}'
                    valor = [i[0],i[1],i[2]]
                    dic[chave] = valor
                    j+=1
                return dic
            return dic
         
        @self.servidor.route("/NovaSenha", methods=['POST'])
        def novaSenha():
            try:
                dados = request.get_json()
                cpf = dados['cpf']
                senha = dados['senha']
                Senha = jwt.encode({'senha': senha}, "senha-padrão", algorithm='HS256')
                print(Senha)
                sstatus = classeBD.alterarSenha(cpf, Senha)
                return Response(status=sstatus)
            except: 
                return Response(status=sstatus)
               
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
        
        # @self.servidor.route('/sendImagePerfil', methods = ['POST'])
        # def sendImagePerfil():
        #     id = request.get_json()
        #     id = id['id']

        #     image = classeBD.SendImage(id)

        #     if image:
        #         image_data = image[0]

        #         # Cria um objeto BytesIO para armazenar a imagem como um fluxo de bytes
        #         img_io = BytesIO(image_data)

        #         # Define os cabeçalhos HTTP para a resposta
        #         response = make_response(img_io.getvalue())
        #         response.headers.set('Content-Type', 'image/jpeg')
        #         response.headers.set('Content-Disposition', 'attachment', filename='image.jpg')

        #         return response
        #     return Response(status=400)
        self.servidor.run(host="0.0.0.0", debug=True)
        