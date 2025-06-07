import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurações do remetente
EMAIL_REMETENTE = "alertasenchentes@gmail.com"
SENHA_REMETENTE = "jpbw wcfn atnq zknz"
SMTP_SERVIDOR = "smtp.gmail.com"
SMTP_PORTA = 587


# Função para enviar e-mail
def enviar_email(destinatarios, assunto, corpo):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_REMETENTE
        msg["To"] = ", ".join(destinatarios)
        msg["Subject"] = assunto

        msg.attach(MIMEText(corpo, "plain"))

        with smtplib.SMTP(SMTP_SERVIDOR, SMTP_PORTA) as servidor:
            servidor.starttls()
            servidor.login(EMAIL_REMETENTE, SENHA_REMETENTE)
            servidor.sendmail(EMAIL_REMETENTE, destinatarios, msg.as_string())

        print("📧 E-mail enviado com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")

