import pandas as pd

# Lista de plantas com suas características ambientais ideais
plantas = [
    {"nome": "Mangueira", "temp_min": 24, "temp_max": 30, "umid_min": 60, "umid_max": 80, "co_max": 500, "press_min": 1010, "press_max": 1020, "aqi_max": 2},
    {"nome": "Jaqueira", "temp_min": 22, "temp_max": 32, "umid_min": 70, "umid_max": 90, "co_max": 400, "press_min": 1008, "press_max": 1015, "aqi_max": 2},
    {"nome": "Bananeira", "temp_min": 25, "temp_max": 35, "umid_min": 75, "umid_max": 95, "co_max": 400, "press_min": 1008, "press_max": 1015, "aqi_max": 2},
    {"nome": "Pitangueira", "temp_min": 20, "temp_max": 30, "umid_min": 60, "umid_max": 85, "co_max": 400, "press_min": 1008, "press_max": 1022, "aqi_max": 2},
    {"nome": "Cajueiro", "temp_min": 23, "temp_max": 38, "umid_min": 40, "umid_max": 70, "co_max": 350, "press_min": 1005, "press_max": 1015, "aqi_max": 1},
    {"nome": "Graviola", "temp_min": 24, "temp_max": 30, "umid_min": 70, "umid_max": 90, "co_max": 400, "press_min": 1008, "press_max": 1020, "aqi_max": 2},
    {"nome": "Aceroleira", "temp_min": 25, "temp_max": 32, "umid_min": 60, "umid_max": 80, "co_max": 350, "press_min": 1010, "press_max": 1020, "aqi_max": 1},
    {"nome": "Limoeiro", "temp_min": 18, "temp_max": 32, "umid_min": 50, "umid_max": 70, "co_max": 350, "press_min": 1008, "press_max": 1022, "aqi_max": 2},
    {"nome": "Amoreira", "temp_min": 15, "temp_max": 30, "umid_min": 60, "umid_max": 80, "co_max": 400, "press_min": 1010, "press_max": 1025, "aqi_max": 1},
    {"nome": "Alecrim", "temp_min": 15, "temp_max": 28, "umid_min": 40, "umid_max": 60, "co_max": 300, "press_min": 1010, "press_max": 1020, "aqi_max": 1}
]

# Converte para DataFrame
df = pd.DataFrame(plantas)

# Salva em CSV
caminho_saida = "plantas_caracteristicas.csv"
df.to_csv(caminho_saida, index=False)

print(f"Arquivo '{caminho_saida}' gerado com sucesso!")
