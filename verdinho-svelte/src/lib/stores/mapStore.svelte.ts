export type PlantRecommendation = {
	class: string;
	family: string;
	order: string;
	gender: string;
	cientific_name: string;
};

export type AnalyzedAreaData = {
	latitude: number;
	longitude: number;
	anual_mean_temperature: number;
	anual_mean_precipitation: number;
	isothermality: number;
	temperature_seasonality: number;
};

export type QuadrantData = {
	lat: number;
	lon: number;
	plantRecommendation: PlantRecommendation;
	analyzedAreaData: AnalyzedAreaData;
};

class MapState {
	selectedArea: {
		latMin: number;
		lonMin: number;
		latMax: number;
		lonMax: number;
	} | null = $state(null);

	quadrants: QuadrantData[] = $state([]);

	isProcessing: boolean = $state(false);

	lastAnalyzedArea: {
		latMin: number;
		lonMin: number;
		latMax: number;
		lonMax: number;
		timestamp: number;
	} | null = $state(null);
}

export const mapState = new MapState();
