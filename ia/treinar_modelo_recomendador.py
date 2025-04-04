import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib

# Carrega o dataset
df = pd.read_csv("dataset_recomendador.csv")

# Codifica o nome da planta como número
le = LabelEncoder()
df["planta_id"] = le.fit_transform(df["planta"])

# Divide em treino e teste
X = df[["temperatura", "umidade", "pressao", "co", "aqi"]]
y = df["planta_id"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treina o modelo
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Avaliação
y_pred = modelo.predict(X_test)
print("📊 Relatório de Classificação:")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# Salva o modelo e o encoder
joblib.dump(modelo, "modelo_recomendador.joblib")
joblib.dump(le, "label_encoder_recomendador.joblib")
print("✅ Modelo e encoder salvos com sucesso!")
