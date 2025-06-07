# treino_modelo.py
# Modelo simples de Machine Learning para classificar risco de enchente com base na altura da água

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib

# Simulando um conjunto de dados
# Nível da água em cm + Previsão de chuva em mm (opcional)
dados = pd.DataFrame({
    'nivel_cm': [10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90],
    'chuva_mm': [0, 0, 2, 5, 5, 10, 20, 40, 60, 80, 100, 120],
    'risco': ['baixo', 'baixo', 'baixo', 'baixo', 'medio', 'medio', 'medio', 'alto', 'alto', 'alto', 'alto', 'alto']
})

# Transformando a variável de saída em números
dados['risco'] = dados['risco'].map({'baixo': 0, 'medio': 1, 'alto': 2})

X = dados[['nivel_cm', 'chuva_mm']]
y = dados['risco']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinamento do modelo
modelo = DecisionTreeClassifier(max_depth=3, random_state=42)
modelo.fit(X_train, y_train)

# Avaliação
y_pred = modelo.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Acurácia do modelo: {acc:.2f}")

# Salvando o modelo para uso posterior
joblib.dump(modelo, 'modelo_risco_enchente.joblib')