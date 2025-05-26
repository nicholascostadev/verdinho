import { z, ZodError } from 'zod';
import { getRecommendedPlantExternal } from '../../../services/http/external/get-recommended-plant-external.js';
import { json } from '@sveltejs/kit';

const QuerySchema = z.object({
	lat_min: z.coerce.number(),
	lon_min: z.coerce.number(),
	lat_max: z.coerce.number(),
	lon_max: z.coerce.number()
});

export async function GET({ request, setHeaders }) {
	try {
		const { searchParams } = new URL(request.url);

		const parsedBody = QuerySchema.parse({
			lat_min: searchParams.get('lat_min'),
			lon_min: searchParams.get('lon_min'),
			lat_max: searchParams.get('lat_max'),
			lon_max: searchParams.get('lon_max')
		});

		const response = await getRecommendedPlantExternal({
			latMin: parsedBody.lat_min,
			lonMin: parsedBody.lon_min,
			latMax: parsedBody.lat_max,
			lonMax: parsedBody.lon_max
		});

		setHeaders({
			'Cache-Control': 'max-age=30'
		});

		return json(response);
	} catch (error) {
		return json(
			{ error: error instanceof ZodError ? error.format() : 'Internal server error' },
			{ status: 500 }
		);
	}
}
