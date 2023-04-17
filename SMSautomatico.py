from twilio.rest import Client

def sendMsg(numero, codigo):

    account_sid = 'ACae5f4f29ca4174e8d01634d392e65427'
    auth_token = 'ecf3afb8873437b43784ecf528c501e4'


    twilio_phone_number = '+13855267150' 


    client = Client(account_sid, auth_token)

    # Envia a mensagem
    try:
        message = client.messages.create(
            body=f'Olá, seu código de verificação é: {codigo}!',
            from_=twilio_phone_number,
            to= f"+55{numero}"
        )
        return 200
    except: return "erro"
