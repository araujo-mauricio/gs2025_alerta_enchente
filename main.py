from flask import Flask, request, jsonify
from modelo_ml.preditor import prever_risco
from utils.alertas import exibir_alerta
from utils.email_utils import enviar_email
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route("/nivel", methods=["POST"])
def receber_nivel():
    dados = request.get_json()

    # Validação de entrada
    try:
        nivel = float(dados.get("nivel_cm"))
        chuva = float(dados.get("chuva_mm"))
    except (TypeError, ValueError):
        return jsonify({"erro": "Dados de entrada inválidos. Envie 'nivel_cm' e 'chuva_mm' numéricos."}), 400

    # Chama modelo preditivo
    previsao = prever_risco(nivel, chuva)

    # Conecta ao banco e registra
    conn = sqlite3.connect("database/banco_dados.sqlite")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO alertas (data_hora, nivel_cm, chuva_mm, risco, probabilidade_baixo, probabilidade_medio, probabilidade_alto, tendencia)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now(),
        nivel,
        chuva,
        previsao['risco'],
        previsao['probabilidades'].get('baixo'),
        previsao['probabilidades'].get('médio'),
        previsao['probabilidades'].get('alto'),
        previsao['tendencia']
    ))

    conn.commit()
    conn.close()

    # Exibe alerta com informações preditivas
    exibir_alerta(
        nivel,
        chuva,
        previsao['risco'],
        previsao['probabilidades'],
        previsao['tendencia']
    )

    from utils.alertas import enviar_sms_alerta

    mensagem = "🚨 Alerta de enchente: nível de água elevado detectado!"
    enviar_sms_alerta(mensagem, destino='+5511999929940')

    # Envia e-mail se risco for alto
    if previsao['risco'] == 'alto':
        corpo = f"""🚨 Alerta de Enchente 🚨

    Nível da água: {nivel:.1f} cm
    Precipitação: {chuva:.1f} mm
    Nível de risco: ALTO

    Recomendações: acione a defesa civil, oriente moradores de áreas de risco e monitore o nível constantemente.
    """
        enviar_email(["dimensoes@gmail.com"], "🚨 Alerta de Enchente 🚨", corpo)

    return jsonify(previsao)

if __name__ == "__main__":
    app.run(debug=True)
