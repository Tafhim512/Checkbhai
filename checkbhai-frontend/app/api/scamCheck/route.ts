import { NextResponse } from 'next/server';
import OpenAI from 'openai';

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
});

export async function POST(req: Request) {
    try {
        const { message } = await req.json();

        if (!message) {
            return NextResponse.json({ error: 'Message is required' }, { status: 400 });
        }

        if (!process.env.OPENAI_API_KEY) {
            console.error('OPENAI_API_KEY is missing from environment variables');
            return NextResponse.json({ error: 'OpenAI API Key is not configured in Vercel' }, { status: 500 });
        }

        const response = await openai.chat.completions.create({
            model: 'gpt-4o-mini',
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
                {
                    role: 'user',
                    content: message
                }
            ],
            response_format: { type: "json_object" }
        });

        const result = JSON.parse(response.choices[0].message.content || '{}');
        return NextResponse.json(result);

    } catch (error: any) {
        console.error('OpenAI API Error:', error);

        let errorMessage = 'Failed to analyze message';
        if (error.status === 401) errorMessage = 'Invalid OpenAI API Key';
        if (error.status === 429) errorMessage = 'OpenAI Quota Exceeded';

        return NextResponse.json({
            error: errorMessage,
            details: error.message
        }, { status: error.status || 500 });
    }
}
