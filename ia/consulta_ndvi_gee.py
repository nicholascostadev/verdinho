import ee

# Inicializa a API
ee.Initialize(project='ndvi-reflorestamento')

def consultar_ndvi(lat, lon):
    ponto = ee.Geometry.Point([lon, lat])

    # Usando coleção Sentinel-2 com NDVI calculado
    colecao = ee.ImageCollection("COPERNICUS/S2_SR") \
        .filterBounds(ponto) \
        .filterDate('2023-01-01', '2023-12-31') \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
        .map(lambda img: img.normalizedDifference(['B8', 'B4']).rename('NDVI'))

    imagem_ndvi = colecao.mean().select('NDVI')
    ndvi_valor = imagem_ndvi.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=ponto,
        scale=10
    ).get('NDVI').getInfo()

    return ndvi_valor

# Exemplo de uso
if __name__ == "__main__":
    lat = -22.95
    lon = -43.38
    ndvi = consultar_ndvi(lat, lon)
    print(f"NDVI real para [{lat}, {lon}] = {ndvi}")
