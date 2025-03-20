from openai import OpenAI
from config import OPENROUTER_API_KEY, SITE_URL, SITE_NAME
import logging

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def ask_openrouter(messages):
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": SITE_URL,
                "X-Title": SITE_NAME,
            },
            model="deepseek/deepseek-r1:free",
            messages=messages,
            temperature=0.6,
            max_tokens=2000
        )
        response_text = completion.choices[0].message.content
        return response_text
    except Exception as e:
        logging.error(f"Ошибка при запросе к OpenRouter: {e}")
        return "Извините, произошла ошибка при обработке вашего запроса."
