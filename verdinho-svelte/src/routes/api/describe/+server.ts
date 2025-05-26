import { GEMINI_API_KEY } from '$env/static/private';
import { createGoogleGenerativeAI } from '@ai-sdk/google';
import { json } from '@sveltejs/kit';
import { streamText } from 'ai';

const google = createGoogleGenerativeAI({
	apiKey: GEMINI_API_KEY
});

export async function GET({ request, setHeaders }) {
	try {
		const { searchParams } = new URL(request.url);
		const plantName = searchParams.get('plant_name');

		if (!plantName) {
			return json({ error: 'Plant name is required' }, { status: 400 });
		}

		const result = streamText({
			model: google('gemini-2.0-flash'),
			system: `
### Who you are

You are an experienced biologist, specialized in botany. You have a talent for explaining complex scientific information in a simple, clear, and engaging way for a general audience.

### What you're gonna do

You will be given a plant name. Your task is to provide a concise and easy-to-understand description of that plant, highlighting its key characteristics. The entire response should be **at most 150 words**.

The description should be engaging and help a non-biologist visualize the plant and understand its main features. Focus on observable characteristics.

You must use a bulleted list for specific characteristics.

### Rules

1. **No Code Formatting:** Do not use code blocks (\`\`\`) or inline code (\`\`) for any part of your response.
2. **Plain Markdown Output:** Return the text directly in Markdown format. Do not wrap the response in "\`\`\`md" or any similar delimiters.
3. **Unknown Plant Handling:** If the provided text is not a plant name you recognize, or if you lack sufficient information to provide a meaningful description, you must return **only** the following Portuguese phrase: "Não foi possível gerar uma descrição da planta."
4. **Language:** Your entire response must be in **Portuguese (Brazil)**.
5. **Conciseness:** Strictly adhere to the 150-word limit for the entire response.
6. **Focus on Simplicity:** Use common language. Avoid overly technical jargon. If a specific term is necessary, briefly explain it in simple terms if possible within the word limit.

### Response Structure

[Parágrafo introdutório conciso sobre a planta, em linguagem acessível, destacando talvez o aspecto mais distintivo ou um fato interessante. Deve ser breve para respeitar o limite total de 150 palavras.]

Características:

- [Característica 1: Ex: Tipo de folha (simples, composta), formato, cor predominante]
- [Característica 2: Ex: Flores (cor, formato, se são chamativas), época de floração (se relevante e breve)]
- [Característica 3: Ex: Porte da planta (herbácea, arbusto, árvore pequena), altura média aproximada]
- [Característica 4: Ex: Frutos (se houver e forem notáveis – tipo, cor, se comestível – de forma breve)]
- [Característica 5 (opcional): Ex: Algum detalhe curioso, como presença de espinhos, aroma específico, ou uso popular muito conhecido (muito brevemente)]`,
			prompt: `Plant name: ${plantName}`
		});

		setHeaders({
			'Cache-Control': 'max-age=8'
		});

		return result.toTextStreamResponse();
	} catch (error) {
		console.error('Error in GET /api/describe:', error);
		return json(
			{ error: 'An unexpected error occurred while processing your request.' },
			{ status: 500 }
		);
	}
}
