import { json } from '@sveltejs/kit';
import { getPlantDetails } from '../../../services/http/external/get-plant-details';
import { queryPlantByName } from '../../../services/http/external/query-plant-by-name';

export async function GET({ request, setHeaders }) {
	const { searchParams } = new URL(request.url);
	const plantName = searchParams.get('plant_name');

	if (!plantName) {
		return json({ error: 'Plant name is required' }, { status: 400 });
	}

	const plantDetails = await getPlantDetails(plantName);

	if (!plantDetails.speciesKey) {
		return json({ error: 'Plant information not found.' }, { status: 404 });
	}

	const plantGallery = await queryPlantByName(plantDetails.speciesKey.toString());

	setHeaders({
		'Cache-Control': 'public, max-age=600'
	});

	return json(plantGallery);
}
