export type PlantDetails = {
	usageKey: number;
	scientificName: string;
	canonicalName: string;
	rank: string;
	status: string;
	confidence: number;
	matchType: string;
	kingdom: string;
	phylum: string;
	order: string;
	family: string;
	genus: string;
	species: string;
	kingdomKey: number;
	phylumKey: number;
	classKey: number;
	orderKey: number;
	familyKey: number;
	genusKey: number;
	speciesKey: number;
	synonym: boolean;
	class: string;
};

export async function getPlantDetails(plantName: string) {
	const response = await fetch(`https://api.gbif.org/v1/species/match?name=${plantName}`);

	const data = (await response.json()) as PlantDetails;

	return data;
}
