import type { FeatureGroup } from "leaflet";

export type PlantRecommendation = {
	class: string;
	family: string;
	order: string;
	gender: string;
	cientific_name: string;
};

export type QuadrantBounds = {
	latMin: number;
	lonMin: number;
	latMax: number;
	lonMax: number;
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
	quadrantBounds: {
		latMin: number;
		lonMin: number;
		latMax: number;
		lonMax: number;
	};
	plantRecommendation: PlantRecommendation;
	analyzedAreaData: AnalyzedAreaData;
};

class MapState {
	drawnItems: FeatureGroup | null = $state(null);

	selectedArea: {
		latMin: number;
		lonMin: number;
		latMax: number;
		lonMax: number;
	} | null = $state(null);

	quadrants: QuadrantData[] = $state([]);
	processingQuadrants: QuadrantBounds[] = $state([])

	isProcessing = $derived(this.processingQuadrants.length > 0);

	lastAnalyzedArea: {
		latMin: number;
		lonMin: number;
		latMax: number;
		lonMax: number;
		timestamp: number;
	} | null = $state(null);

	addQuadrant(quadrant: QuadrantData) {
		if (this.quadrants.find(item => item.quadrantBounds.latMin === quadrant.quadrantBounds.latMin && item.quadrantBounds.lonMin === quadrant.quadrantBounds.lonMin && item.quadrantBounds.latMax === quadrant.quadrantBounds.latMax && item.quadrantBounds.lonMax === quadrant.quadrantBounds.lonMax)) {
			return;
		}

		this.quadrants.push(quadrant);
	}

	hasQuadrantWithSameArea(quadrantBounds: QuadrantBounds) {
		// Combine existing quadrants and processing quadrants to not allow the user to select
		// an area that is also being processed
		const allQuadrantBounds = [...this.quadrants.map(item => item.quadrantBounds), ...this.processingQuadrants]

		return allQuadrantBounds.some(item => {
			return quadrantBounds.latMin === item.latMin && quadrantBounds.latMax == item.latMax && quadrantBounds.lonMin == item.lonMin && quadrantBounds.lonMax == item.lonMax;
		});
	}

	removeProcessingQuadrant(quadrantBounds: QuadrantBounds) {
		this.processingQuadrants = this.processingQuadrants.filter(item => item.latMin !== quadrantBounds.latMin || item.lonMin !== quadrantBounds.lonMin || item.latMax !== quadrantBounds.latMax || item.lonMax !== quadrantBounds.lonMax);
	}

	addProcessingQuadrant(quadrantBounds: QuadrantBounds) {
		this.processingQuadrants.push(quadrantBounds);
	}

	clearDrawings() {
		this.drawnItems?.clearLayers();
	}
}

export const mapState = new MapState();
