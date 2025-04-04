import requests

url = "http://localhost:5000/recomendar"

dados = {
    "temperatura": 28,
    "umidade": 75,
    "pressao": 1012,
    "co": 350,
    "aqi": 1,
    "planta": "Mangueira"
}

resposta = requests.post(url, json=dados)
print(resposta.json())
