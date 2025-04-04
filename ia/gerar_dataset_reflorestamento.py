import csv
import random

# Lista de plantas associadas a biomas e regiões
plantas_info = [
    {"nome": "Mangueira", "bioma": "Mata Atlântica", "regiao": "Sudeste"},
    {"nome": "Bananeira", "bioma": "Mata Atlântica", "regiao": "Sudeste"},
    {"nome": "Cajueiro", "bioma": "Caatinga", "regiao": "Nordeste"},
    {"nome": "Jaqueira", "bioma": "Mata Atlântica", "regiao": "Nordeste"},
    {"nome": "Graviola", "bioma": "Amazônia", "regiao": "Norte"},
    {"nome": "Pitangueira", "bioma": "Mata Atlântica", "regiao": "Sul"},
    {"nome": "Aceroleira", "bioma": "Caatinga", "regiao": "Nordeste"},
    {"nome": "Limoeiro", "bioma": "Mata Atlântica", "regiao": "Sudeste"},
    {"nome": "Amoreira", "bioma": "Mata Atlântica", "regiao": "Sul"},
    {"nome": "Hortelã", "bioma": "Cerrado", "regiao": "Centro-Oeste"},
    {"nome": "Alecrim", "bioma": "Cerrado", "regiao": "Centro-Oeste"},
    {"nome": "Coentro", "bioma": "Caatinga", "regiao": "Nordeste"},
    {"nome": "Manjericão", "bioma": "Cerrado", "regiao": "Centro-Oeste"},
]

# Função para gerar dados ambientais simulados com base no bioma

def gerar_dados_ambiente(bioma):
    if bioma == "Mata Atlântica":
        return random.uniform(22, 30), random.uniform(65, 90), random.uniform(1008, 1018), random.uniform(250, 400), random.randint(1, 3)
    elif bioma == "Caatinga":
        return random.uniform(26, 38), random.uniform(30, 60), random.uniform(1005, 1015), random.uniform(200, 350), random.randint(2, 5)
    elif bioma == "Amazônia":
        return random.uniform(25, 34), random.uniform(80, 95), random.uniform(1005, 1015), random.uniform(300, 500), random.randint(1, 2)
    elif bioma == "Cerrado":
        return random.uniform(20, 32), random.uniform(45, 75), random.uniform(1008, 1018), random.uniform(250, 400), random.randint(2, 4)
    elif bioma == "Pampa":
        return random.uniform(10, 25), random.uniform(60, 85), random.uniform(1010, 1022), random.uniform(200, 350), random.randint(1, 3)
    else:
        return random.uniform(20, 30), random.uniform(60, 80), random.uniform(1005, 1015), random.uniform(250, 400), random.randint(1, 3)

# Gera o CSV
with open("dataset_reflorestamento.csv", mode="w", newline="", encoding="utf-8") as arquivo:
    writer = csv.writer(arquivo)
    writer.writerow(["temperatura", "umidade", "pressao", "co", "aqi", "planta", "bioma", "regiao"])

    for _ in range(5000):
        planta = random.choice(plantas_info)
        temp, umid, press, co, aqi = gerar_dados_ambiente(planta["bioma"])
        writer.writerow([round(temp, 2), round(umid, 2), round(press, 2), round(co, 2), aqi, planta["nome"], planta["bioma"], planta["regiao"]])

print("✅ Novo dataset_reflorestamento.csv gerado com sucesso!")
