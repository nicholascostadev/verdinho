import type { GetRecommendedPlantResponse } from './external/get-recommended-plant-external';

type GetRecommendedPlantParams = {
	latMin: number;
	lonMin: number;
	latMax: number;
	lonMax: number;
};

export async function getRecommendedPlant(params: GetRecommendedPlantParams) {
	const searchParams = new URLSearchParams();
	searchParams.set('lat_min', params.latMin.toString());
	searchParams.set('lat_max', params.latMax.toString());
	searchParams.set('lon_min', params.lonMin.toString());
	searchParams.set('lon_max', params.lonMax.toString());

	const response = await fetch(`/api/get-recommended-plant?${searchParams.toString()}`);

	return response.json() as Promise<GetRecommendedPlantResponse>;
}
