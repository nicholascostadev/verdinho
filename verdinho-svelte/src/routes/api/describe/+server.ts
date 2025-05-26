import { GEMINI_API_KEY } from '$env/static/private';
import { createGoogleGenerativeAI } from '@ai-sdk/google';
import { json } from '@sveltejs/kit';
import { streamText } from 'ai';

const google = createGoogleGenerativeAI({
	apiKey: GEMINI_API_KEY
});

export async function GET({ request, setHeaders }) {
	const { searchParams } = new URL(request.url);
	const plantName = searchParams.get('plant_name');

	if (!plantName) {
		return json({ error: 'Plant name is required' }, { status: 400 });
	}

	const result = streamText({
		model: google('gemini-2.0-flash'),
		system: `
### Who you are

You are a biologist, with clear and long knowledge about the subject.

### What you're gonna do

You are going to be given a plant name and you will need to describe it in a way that is easy to understand for a non-biologist, showing the characteristics of the plant. It should have at most 150 words.

You can use bullet-lists to list characteristics for the plant.

### Rules

1. You should not format text with code blocks, or inline code.
2. You should return the text in Markdown, with plain text, so not wrapping it with “\`\`\`md\`\`\`” or anything like that.
3. If the text received is not a name of a plant you know, please just return: “Não foi possível gerar uma descrição da planta.”
4. The answer should be in Portuguese - Brazil.`,
		prompt: `Plant name: ${plantName}`
	});

	setHeaders({
		'Cache-Control': 'max-age=8'
	});

	return result.toTextStreamResponse();
}
