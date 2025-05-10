from langchain_openai import OpenAIEmbeddings
from utils.env_loader import OPENROUTER_API_KEY

embedder = OpenAIEmbeddings(
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    model="shisa-ai/shisa-v2-llama3.3-70b:free",
    headers={
        "HTTP-Referer": "https://github.com/your-repo",
        "X-Title": "Flight Assistant"
    }
)

def get_embedding(text: str):
    return embedder.embed_query(text)
