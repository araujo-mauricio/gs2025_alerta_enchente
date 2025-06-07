import os
import sqlite3
from flask import Flask, request, jsonify
from modelo_ml.preditor import prever_risco
from utils.alertas import exibir_alerta
from datetime import datetime, timedelta

# Cria pasta 'database' se não existir
if not os.path.exists("database"):
    os.makedirs("database")

# Conexão com banco de dados
conn = sqlite3.connect("database/banco_dados.sqlite", check_same_thread=False)
cursor = conn.cursor()

# Criação da tabela (se não existir)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS alertas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nivel_cm REAL,
        chuva_mm REAL,
        risco TEXT,
        probabilidade_baixo REAL,
        probabilidade_medio REAL,
        probabilidade_alto REAL,
        tendencia REAL,
        data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# Inicia app Flask
app = Flask(__name__)

def obter_historico_recente(horas=6):
    """Obtém histórico dos últimos níveis de água das últimas horas"""
    cursor.execute("""
        SELECT nivel_cm FROM alertas 
        WHERE data_hora >= datetime('now', ?)
        ORDER BY data_hora ASC
    """, (f'-{horas} hours',))
    return [row[0] for row in cursor.fetchall()]

@app.route("/nivel", methods=["POST"])
def receber_nivel():
    dados = request.get_json()
    nivel = dados.get("nivel_cm")
    chuva = dados.get("chuva_mm")

    # Obtém histórico recente para análise de tendência
    historico = obter_historico_recente()
    
    # Faz previsão com histórico
    previsao = prever_risco(nivel, chuva, historico)

    # Salva no banco de dados
    cursor.execute("""
        INSERT INTO alertas (
            nivel_cm, chuva_mm, risco, 
            probabilidade_baixo, probabilidade_medio, probabilidade_alto,
            tendencia
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        nivel, chuva, previsao['risco'],
        previsao['probabilidades']['baixo'],
        previsao['probabilidades']['medio'],
        previsao['probabilidades']['alto'],
        previsao['tendencia']
    ))
    conn.commit()

    # Exibe alerta com informações preditivas
    exibir_alerta(
        nivel, 
        chuva, 
        previsao['risco'],
        previsao['probabilidades'],
        previsao['tendencia']
    )

    return jsonify(previsao)

if __name__ == "__main__":
    app.run(debug=True)