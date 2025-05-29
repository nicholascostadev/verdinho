import type { MediaResult } from './external/query-plant-by-name';

export async function getPlantGallery(plantName: string) {
	const response = await fetch(`/api/plant-gallery?plant_name=${plantName}`);

	const data = (await response.json()) as MediaResult[];

	return data;
}
