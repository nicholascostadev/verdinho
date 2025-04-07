export type PlantRecommendation = {
	recommended_plant: string;
	biome: string;
	region: string;
};

export type QuadrantData = {
	lat: number;
	lon: number;
	ndvi: number;
	aqi: number;
	refIndex: number;
	needLevel: string;
	plantRecommendation: PlantRecommendation;
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

	enableNdvi: boolean = $state(false);

	lastAnalyzedArea: {
		latMin: number;
		lonMin: number;
		latMax: number;
		lonMax: number;
		timestamp: number;
	} | null = $state(null);
}

export const mapState = new MapState();
