type GetRecommendedPlantResponse = {
  prediction: {
    class: string
    family: string
    order: string
    gender: string
    cientific_name: string
  }
  features_used: {
    latitude: number
    longitude: number
    anual_mean_temperature: number
    anual_mean_precipitation: number
    isothermality: number;
    temperature_seasonality: number;
  }
}


type GetRecommendedPlantParams = {
  latMin: number;
  lonMin: number;
  latMax: number;
  lonMax: number;
}

export async function getRecommendedPlant(params: GetRecommendedPlantParams) {
  const response = await fetch(`${import.meta.env.VITE_API_URL}/recommend-plant-bbox`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      lat_min: params.latMin,
      lat_max: params.latMax,
      lon_min: params.lonMin,
      lon_max: params.lonMax
    })
  });

  return response.json() as Promise<GetRecommendedPlantResponse>;
}