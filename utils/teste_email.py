from utils.emails import enviar_email_alerta, enviar_relatorio_diario_email

# Teste de envio de alerta
destinatario = "dimensoes@gmail.com"
nivel = 250  # cm
chuva = 80   # mm
risco = "alto"  # Pode ser "baixo", "medio" ou "alto"

# Envia e-mail de alerta
enviar_email_alerta(destinatario, nivel, chuva, risco)

# Envia relatório diário
# enviar_relatorio_diario_email(destinatario)
