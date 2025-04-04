# geolocalizacao.py

def obter_info_geografica(lat, lon):
    # Exemplo de limites aproximados por região
    if -33 <= lat <= -20 and -55 <= lon <= -40:
        regiao = "Sul"
    elif -23 <= lat <= -14 and -47 <= lon <= -34:
        regiao = "Sudeste"
    elif -19 <= lat <= -5 and -60 <= lon <= -45:
        regiao = "Centro-Oeste"
    elif -15 <= lat <= 5 and -75 <= lon <= -35:
        regiao = "Norte"
    elif -17 <= lat <= -2 and -45 <= lon <= -34:
        regiao = "Nordeste"
    else:
        regiao = "Desconhecida"

    # Exemplo de correspondência com biomas
    if -30 <= lat <= -12 and -55 <= lon <= -35:
        bioma = "Mata Atlântica"
    elif -10 <= lat <= 5 and -75 <= lon <= -45:
        bioma = "Amazônia"
    elif -16 <= lat <= -2 and -60 <= lon <= -40:
        bioma = "Cerrado"
    elif -12 <= lat <= -2 and -45 <= lon <= -35:
        bioma = "Caatinga"
    elif -34 <= lat <= -28 and -60 <= lon <= -50:
        bioma = "Pampa"
    elif -20 <= lat <= -15 and -60 <= lon <= -55:
        bioma = "Pantanal"
    else:
        bioma = "Desconhecido"

    return {
        "regiao": regiao,
        "bioma": bioma
    }
