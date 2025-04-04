import random
import pandas as pd

# Lista das plantas com suas condições ideais
plantas = [
    {"nome": "Mangueira", "temp_min": 24, "temp_max": 30, "umidade_min": 60, "umidade_max": 80, "co_max": 500, "pressao_min": 1010, "pressao_max": 1020, "aqi_max": 2},
    {"nome": "Jaqueira", "temp_min": 22, "temp_max": 32, "umidade_min": 70, "umidade_max": 90, "co_max": 400, "pressao_min": 1008, "pressao_max": 1015, "aqi_max": 2},
    {"nome": "Bananeira", "temp_min": 25, "temp_max": 35, "umidade_min": 75, "umidade_max": 95, "co_max": 400, "pressao_min": 1008, "pressao_max": 1015, "aqi_max": 2},
    {"nome": "Pitangueira", "temp_min": 20, "temp_max": 30, "umidade_min": 60, "umidade_max": 85, "co_max": 400, "pressao_min": 1008, "pressao_max": 1022, "aqi_max": 2},
    {"nome": "Cajueiro", "temp_min": 23, "temp_max": 38, "umidade_min": 40, "umidade_max": 70, "co_max": 350, "pressao_min": 1005, "pressao_max": 1015, "aqi_max": 1},
    {"nome": "Graviola", "temp_min": 24, "temp_max": 30, "umidade_min": 70, "umidade_max": 90, "co_max": 400, "pressao_min": 1008, "pressao_max": 1020, "aqi_max": 2},
    {"nome": "Aceroleira", "temp_min": 25, "temp_max": 32, "umidade_min": 60, "umidade_max": 80, "co_max": 350, "pressao_min": 1010, "pressao_max": 1020, "aqi_max": 1},
    {"nome": "Limoeiro", "temp_min": 18, "temp_max": 32, "umidade_min": 50, "umidade_max": 70, "co_max": 350, "pressao_min": 1008, "pressao_max": 1022, "aqi_max": 2},
    {"nome": "Amoreira", "temp_min": 15, "temp_max": 30, "umidade_min": 60, "umidade_max": 80, "co_max": 400, "pressao_min": 1010, "pressao_max": 1025, "aqi_max": 1},
    {"nome": "Hortelã", "temp_min": 15, "temp_max": 30, "umidade_min": 60, "umidade_max": 80, "co_max": 300, "pressao_min": 1010, "pressao_max": 1025, "aqi_max": 1},
]

def gerar_ambiente():
    return {
        "temperatura": random.randint(10, 40),
        "umidade": random.randint(30, 100),
        "pressao": random.randint(1000, 1030),
        "co": random.randint(100, 600),
        "aqi": random.randint(1, 5)  # 1 = boa, 5 = muito ruim
    }

def classificar(planta, ambiente):
    fatores = 0
    if planta["temp_min"] <= ambiente["temperatura"] <= planta["temp_max"]:
        fatores += 1
    if planta["umidade_min"] <= ambiente["umidade"] <= planta["umidade_max"]:
        fatores += 1
    if ambiente["co"] <= planta["co_max"]:
        fatores += 1
    if planta["pressao_min"] <= ambiente["pressao"] <= planta["pressao_max"]:
        fatores += 1
    if ambiente["aqi"] <= planta["aqi_max"]:
        fatores += 1

    if fatores == 5:
        return 2
    elif fatores >= 2:
        return 1
    else:
        return 0

# Geração do dataset
dados = []
for _ in range(5000):  # número de exemplos
    ambiente = gerar_ambiente()
    for planta in plantas:
        label = classificar(planta, ambiente)
        dados.append({
            **ambiente,
            "planta": planta["nome"],
            "label": label
        })

# Salvar em CSV
df = pd.DataFrame(dados)
df.to_csv("dataset_reflorestamento.csv", index=False)
print("✅ Dataset salvo como 'dataset_reflorestamento.csv'")
