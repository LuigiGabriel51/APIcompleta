import smtplib
import email.message


def enviar_email(eemail, codigo):  
    corpo_email = f"""
    <p>bom dia, este é seu código de redefinição de senha {codigo}</p>
    """

    msg = email.message.Message()
    msg['Subject'] = "Recuperação de Senha"
    msg['From'] = 'luigiskyline4@gmail.com'
    msg['To'] = f'{eemail}'
    password = 'rzdrwbvgjgbudmko' 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    return 'email enviado com sucesso'

def envia_email_form(email_sup, nome, eemail, tel, cargo, motivo, msge):  
    corpo_email = f"""
    <html>
    <body>
        <p>Olá {nome},</p>
        
        
        <p><strong>Motivo:</strong> {motivo}</p>

        <p>Nome: {nome}</p>
        <p>Email: {eemail}</p>
        <p>Telefone: {tel}</p>
        <p>Cargo: {cargo}</p>
        
        <p>Detalhes do problema:</p>
        <p>{msge}</p>

        <p>O problema está me causando alguns inconvenientes e estou confiante de que a equipe de suporte poderá me ajudar a resolvê-lo.</p>
        
        <p>Por favor, se vocês precisarem de mais informações ou detalhes adicionais, fiquem à vontade para entrar em contato comigo pelo email {email} ou pelo telefone {tel}.</p>
        
        <p>Agradeço antecipadamente pela atenção e pelo suporte na resolução desse problema.</p>
        
    </body>
    </html>
    """

    msg = email.message.Message()
    msg['Subject'] = "Suporte Técnico"
    msg['From'] = 'luigiskyline4@gmail.com'
    msg['To'] = f'{email_sup}'
    password = 'rzdrwbvgjgbudmko' 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    return 'email enviado com sucesso'