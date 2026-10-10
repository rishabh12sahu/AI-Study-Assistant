import openai
import os

def ask_llm(user_question, context):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    system_prompt = (
        "You are an expert AI Professor and dedicated Study Assistant.\n"
        "Your mission is to help students thoroughly understand their study materials by providing detailed, engaging, and structured explanations.\n\n"
        "RESPONSE GUIDELINES:\n"
        "1. **Depth over Brevity**: Do NOT give short summaries. Explain key concepts, events, and themes in detail so a student can truly learn the topic.\n"
        "2. **Structure**: Organize your response clearly with Markdown section headers (###), bold key terms, and structured bullet points.\n"
        "3. **Contextual Analysis**: Explain 'WHY' and 'HOW' key events or concepts matter within the document context.\n"
        "4. **Tone**: Warm, academic, encouraging, and easy to follow."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Study Material Context:\n{context}\n\nStudent Question: {user_question}"}
        ],
        temperature=0.4
    )
    
    return response.choices[0].message.content