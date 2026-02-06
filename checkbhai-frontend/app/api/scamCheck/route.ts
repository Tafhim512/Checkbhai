import { NextResponse } from 'next/server';
import OpenAI from 'openai';

export async function POST(req: Request) {
    try {
        const { message } = await req.json();

        if (!message) {
            return NextResponse.json({ error: 'Message is required' }, { status: 400 });
        }

        const openaiKey = process.env.OPENAI_API_KEY;
        const groqKey = process.env.GROQ_API_KEY;

        const providers = [];
        if (openaiKey && !openaiKey.startsWith('your-')) {
            providers.push({
                name: 'OpenAI',
                client: new OpenAI({ apiKey: openaiKey }),
                model: 'gpt-4o-mini'
            });
        }
        if (groqKey && !groqKey.startsWith('your-')) {
            providers.push({
                name: 'Groq',
                client: new OpenAI({
                    apiKey: groqKey,
                    baseURL: "https://api.groq.com/openai/v1"
                }),
                model: 'llama-3.3-70b-versatile'
            });
        }

        if (providers.length === 0) {
            return NextResponse.json({
                error: 'No AI providers configured. Please add OPENAI_API_KEY or GROQ_API_KEY to environment variables.'
            }, { status: 500 });
        }

        let lastError = null;
        for (const provider of providers) {
            try {
                const response = await provider.client.chat.completions.create({
                    model: provider.model,
                    messages: [
                        {
                            role: 'system',
                            content: `You are CheckBhai AI, a specialist in detecting scams specifically in the context of Bangladesh. 
              Analyze the user's message (which could be in English, Bangla, or Banglish) and determine if it's a scam.
              Provide a risk score from 0 to 100, a clear explanation in both English and Bangla, and a list of red flags.
              Respond ONLY in JSON format:
              {
                "risk_score": number,
                "prediction": "Scam" | "Legit",
                "explanation_en": "string",
                "explanation_bn": "string",
                "red_flags": ["string"]
              }`
                        },
                        { role: 'user', content: message }
                    ],
                    response_format: { type: "json_object" }
                });

                const result = JSON.parse(response.choices[0].message.content || '{}');
                result.provider = provider.name;
                return NextResponse.json(result);
            } catch (error: any) {
                console.warn(`${provider.name} failed:`, error.message);
                lastError = error;
            }
        }

        return NextResponse.json({
            error: 'All AI providers failed',
            details: lastError?.message
        }, { status: 500 });

    } catch (error: any) {
        console.error('ScamCheck API Error:', error);
        return NextResponse.json({
            error: 'Internal server error',
            details: error.message
        }, { status: 500 });
    }
}
