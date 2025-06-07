import joblib
import numpy as np
from datetime import datetime, timedelta

# Carrega o modelo salvo
modelo = joblib.load('modelo_ml/modelo_risco_enchente.joblib')

# Tabela de risco
RISCOS = {0: 'baixo', 1: 'medio', 2: 'alto'}

def calcular_tendencia(historico_niveis):
    """Calcula a tendência de subida/descida do nível da água"""
    if len(historico_niveis) < 2:
        return 0
    
    diferenca = historico_niveis[-1] - historico_niveis[0]
    return diferenca / len(historico_niveis)

def prever_risco(nivel_cm, chuva_mm, historico_niveis=None):
    """
    Preve o risco de enchente considerando tendências e probabilidades
    
    Args:
        nivel_cm: Nível atual da água em cm
        chuva_mm: Quantidade de chuva em mm
        historico_niveis: Lista com histórico dos últimos níveis (opcional)
    """
    # Previsão base
    entrada = [[nivel_cm, chuva_mm]]
    resultado = modelo.predict(entrada)
    risco_base = RISCOS[int(resultado[0])]
    
    # Probabilidades de cada classe
    probabilidades = modelo.predict_proba(entrada)[0]
    
    # Ajuste baseado na tendência
    if historico_niveis:
        tendencia = calcular_tendencia(historico_niveis)
        if tendencia > 0.5:  # Subida rápida
            if risco_base == 'baixo':
                risco_base = 'medio'
            elif risco_base == 'medio':
                risco_base = 'alto'
    
    return {
        'risco': risco_base,
        'probabilidades': {
            'baixo': float(probabilidades[0]),
            'medio': float(probabilidades[1]),
            'alto': float(probabilidades[2])
        },
        'tendencia': tendencia if historico_niveis else None
    }
