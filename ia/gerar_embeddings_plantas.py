import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import csv

# Carrega o modelo de embeddings semânticos
modelo = SentenceTransformer('all-MiniLM-L6-v2')

# Lê o CSV com as características das plantas
df = pd.read_csv("plantas_caracteristicas.csv")

# Gera descrições textuais de cada planta
def gerar_descricao(planta):
    return (
        f"Planta {planta['nome']}: prefere clima entre {planta['temp_min']} e {planta['temp_max']} graus Celsius, "
        f"umidade entre {planta['umid_min']}% e {planta['umid_max']}%, pressão entre {planta['press_min']} e {planta['press_max']} hPa, "
        f"concentração de CO até {planta['co_max']} ppm e AQI até {planta['aqi_max']}."
    )

# Gera vetores para cada planta
embeddings = []

for _, planta in df.iterrows():
    descricao = gerar_descricao(planta)
    vetor = modelo.encode(descricao)
    embeddings.append([planta['nome']] + vetor.tolist())

# Salva os embeddings em um novo CSV
with open("plantas_embeddings.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["nome"] + [f"dim_{i}" for i in range(len(embeddings[0]) - 1)])
    writer.writerows(embeddings)

print("✅ Embeddings gerados e salvos em plantas_embeddings.csv")
