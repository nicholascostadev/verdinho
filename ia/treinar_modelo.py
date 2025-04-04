import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import joblib  # Para salvar o modelo

# Carrega o dataset
df = pd.read_csv("ia/dataset_reflorestamento.csv")


# Converte nomes de plantas em números (Label Encoding)
le = LabelEncoder()
df["planta_encoded"] = le.fit_transform(df["planta"])

# Define as features (entradas) e o label (saída)
X = df[["temperatura", "umidade", "pressao", "co", "aqi", "planta_encoded"]]
y = df["label"]

# Divide em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Cria e treina o modelo
modelo = DecisionTreeClassifier(max_depth=6)
modelo.fit(X_train, y_train)

# Avaliação do modelo
y_pred = modelo.predict(X_test)
print("📊 Relatório de classificação:")
print(classification_report(y_test, y_pred))

# Salva o modelo e o codificador de plantas
joblib.dump(modelo, "modelo_recomendacao.joblib")
joblib.dump(le, "label_encoder.joblib")
print("✅ Modelo salvo como 'modelo_recomendacao.joblib'")
