from openai import OpenAI
from utils.env_loader import OPENROUTER_API_KEY

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def get_llm_response(prompt, site_url=None, site_title=None):
    headers = {}
    if site_url:
        headers["HTTP-Referer"] = site_url
    if site_title:
        headers["X-Title"] = site_title

    response = client.chat.completions.create(
        extra_headers=headers,
        model="shisa-ai/shisa-v2-llama3.3-70b:free",
        messages=[
            {"role": "system", "content": "You are a helpful flight assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
