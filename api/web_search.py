import requests

def duckduckgo_search(query: str):
    response = requests.get(f"https://api.duckduckgo.com/?q={query}&format=json")
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "DuckDuckGo search failed", "status": response.status_code}
