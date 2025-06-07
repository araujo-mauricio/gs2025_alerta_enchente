import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
from datetime import datetime, timedelta

# Configurações do remetente
EMAIL_REMETENTE = "alerta.enchente@gmail.com"
SENHA_APP = "oyip zoqz cglc ofuv"
SERVIDOR_SMTP = "smtp.gmail.com"
PORTA_SMTP = 587

def enviar_email_alerta(destinatario, nivel, chuva, risco):
    assunto = f"ALERTA: Risco {risco.upper()} de Enchente"
    corpo = f"""
    Prezado(a),

    Um alerta de risco {risco} de enchente foi detectado.

    Nível do rio: {nivel} cm
    Volume de chuva: {chuva} mm

    Por favor, adote as medidas cabíveis.

    Sistema de Monitoramento de Enchentes
    """
    enviar_email(destinatario, assunto, corpo)

def enviar_relatorio_diario_email(destinatario):
    conn = sqlite3.connect("database/banco_dados.sqlite")
    cursor = conn.cursor()

    hoje = datetime.now().date()
    inicio = datetime.combine(hoje, datetime.min.time())
    fim = datetime.combine(hoje, datetime.max.time())

    cursor.execute("""
        SELECT data_hora, nivel_cm, chuva_mm, risco 
        FROM alertas 
        WHERE data_hora BETWEEN ? AND ?
    """, (inicio, fim))

    linhas = cursor.fetchall()
    conn.close()

    if not linhas:
        corpo = "Nenhum alerta registrado no dia de hoje."
    else:
        corpo = "Relatório diário de alertas registrados hoje:\n\n"
        for linha in linhas:
            data_hora, nivel, chuva, risco = linha
            corpo += f"{data_hora} | Nível: {nivel} cm | Chuva: {chuva} mm | Risco: {risco}\n"

    assunto = "Relatório Diário - Alertas de Enchente"
    enviar_email(destinatario, assunto, corpo)

def enviar_email(destinatario, assunto, corpo):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = destinatario
    msg["Subject"] = assunto

    msg.attach(MIMEText(corpo, "plain"))

    try:
        server = smtplib.SMTP(SERVIDOR_SMTP, PORTA_SMTP)
        server.starttls()
        server.login(EMAIL_REMETENTE, SENHA_APP)
        server.sendmail(EMAIL_REMETENTE, destinatario, msg.as_string())
        server.quit()
        print(f"E-mail enviado para {destinatario}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
