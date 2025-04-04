from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import joblib
import ee
import csv
import numpy as np
import traceback
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import KNeighborsClassifier
from geolocalizacao import obter_info_geografica
from typing import Dict, List, Union, Any, Tuple, Optional

ee.Initialize(project='ndvi-reflorestamento')

modelo_classificador = joblib.load("modelo_recomendacao.joblib")
encoder_classificador = joblib.load("label_encoder.joblib")
modelo_recomendador = joblib.load("modelo_recomendador.joblib")
encoder_recomendador = joblib.load("label_encoder_recomendador.joblib")

app = Flask(__name__)
CORS(app)

def interpretar_label(label: int) -> str:
    if label == 2:
        return "Recomendado: planta ideal para esse ambiente."
    elif label == 1:
        return "Pode ser plantada: atende parcialmente as condições."
    else:
        return "Não recomendado: não atende às condições ambientais."

@app.route('/recomendar', methods=['POST'])
def recomendar() -> Tuple[Response, int]:
    data = request.get_json()
    try:
        planta_nome: str = data["planta"]
        planta_id: int = encoder_classificador.transform([planta_nome])[0]
        entrada: List[Union[float, int]] = [
            float(data["temperatura"]),
            float(data["umidade"]),
            float(data["pressao"]),
            float(data["co"]),
            float(data["aqi"]),
            planta_id
        ]
        pred: int = modelo_classificador.predict([entrada])[0]
        return jsonify({
            "planta": planta_nome,
            "classificacao": int(pred),
            "descricao": interpretar_label(pred)
        }), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"erro": str(e)}), 400

@app.route('/melhor-planta', methods=['POST'])
def melhor_planta() -> Tuple[Response, int]:
    data = request.get_json()
    print("📥 Dados recebidos na rota /melhor-planta:", data)  # <-- DEBUG LOG
    try:
        lat: float = float(data["lat"])
        lon: float = float(data["lon"])

        geo_info: Dict[str, str] = obter_info_geografica(lat, lon)
        bioma: str = geo_info.get("bioma", "Desconhecido")
        regiao: str = geo_info.get("regiao", "Desconhecida")

        entrada: List[float] = [
            float(data["temperatura"]),
            float(data["umidade"]),
            float(data["pressao"]),
            float(data["co"]),
            float(data["aqi"])
        ]

        X: List[List[float]] = []
        y: List[str] = []
        with open("dataset_reflorestamento.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["bioma"] == bioma and row["regiao"] == regiao:
                    X.append([
                        float(row["temperatura"]), 
                        float(row["umidade"]), 
                        float(row["pressao"]), 
                        float(row["co"]), 
                        float(row["aqi"])
                    ])
                    y.append(row["planta"])

        if not X:
            msg: str = f"Sem dados para bioma '{bioma}' e região '{regiao}'"
            print("⚠️", msg)
            return jsonify({"erro": msg}), 404

        knn: KNeighborsClassifier = KNeighborsClassifier(n_neighbors=3)
        knn.fit(X, y)
        pred: str = knn.predict([entrada])[0]

        return jsonify({
            "planta_recomendada": pred,
            "bioma": bioma,
            "regiao": regiao
        }), 200

    except Exception as e:
        print("❌ Erro interno na rota /melhor-planta:")
        traceback.print_exc()
        return jsonify({"erro": str(e)}), 400

@app.route('/ndvi-real', methods=['POST'])
def ndvi_real() -> Tuple[Response, int]:
    data = request.get_json()
    try:
        lat: float = float(data["lat"])
        lon: float = float(data["lon"])
        ponto: ee.Geometry.Point = ee.Geometry.Point([lon, lat])
        colecao: ee.ImageCollection = ee.ImageCollection("COPERNICUS/S2_SR") \
            .filterBounds(ponto) \
            .filterDate('2023-01-01', '2023-12-31') \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
            .map(lambda img: img.normalizedDifference(['B8', 'B4']).rename('NDVI'))

        imagem_ndvi: ee.Image = colecao.mean().select('NDVI')
        ndvi_valor: Optional[float] = imagem_ndvi.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=ponto,
            scale=10
        ).get('NDVI').getInfo()

        return jsonify({ "ndvi": ndvi_valor }), 200
    except Exception as e:
        print("Erro NDVI real:", e)
        return jsonify({"erro": str(e)}), 400

@app.route('/adicionar-planta', methods=['POST'])
def adicionar_planta() -> Tuple[Response, int]:
    try:
        data = request.get_json()
        nome: str = data['nome']
        descricao: str = data['descricao']

        model: SentenceTransformer = SentenceTransformer('all-MiniLM-L6-v2')
        vetor: np.ndarray = model.encode(descricao)

        with open("plantas_embeddings.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([nome] + vetor.tolist())

        return jsonify({"nome": nome}), 200
    except Exception as e:
        print("Erro ao adicionar planta:", e)
        return jsonify({"erro": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
