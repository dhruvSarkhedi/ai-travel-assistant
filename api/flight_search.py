import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from utils.env_loader import SERPAPI_KEY

def create_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def format_flight_query(query: str) -> str:
    # Extract origin and destination from the query
    # This is a simple implementation - you might want to use NLP for better extraction
    parts = query.lower().split()
    if "from" in parts and "to" in parts:
        from_idx = parts.index("from")
        to_idx = parts.index("to")
        if from_idx < to_idx:
            origin = " ".join(parts[from_idx + 1:to_idx])
            destination = " ".join(parts[to_idx + 1:])
            return f"{origin} to {destination}"
    return query

def get_flight_info(query: str):
    try:
        session = create_session()
        formatted_query = format_flight_query(query)
        params = {
            "engine": "google_flights",
            "q": formatted_query,
            "api_key": SERPAPI_KEY,
            "hl": "en",
            "gl": "us"
        }
        response = session.get("https://serpapi.com/search", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching flight info: {str(e)}")
        return {"error": f"Flight API request failed: {str(e)}"}

def get_hotel_info(location: str):
    try:
        session = create_session()
        # Clean up location string
        clean_location = location.split("on")[0].strip() if "on" in location else location
        params = {
            "engine": "google_hotels",
            "q": f"hotels in {clean_location}",
            "api_key": SERPAPI_KEY,
            "hl": "en",
            "gl": "us"
        }
        response = session.get("https://serpapi.com/search", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching hotel info: {str(e)}")
        return {"error": f"Hotel API request failed: {str(e)}"}

def get_events_info(location: str):
    try:
        session = create_session()
        # Clean up location string
        clean_location = location.split("on")[0].strip() if "on" in location else location
        params = {
            "engine": "google_events",
            "q": f"events in {clean_location}",
            "api_key": SERPAPI_KEY,
            "hl": "en",
            "gl": "us"
        }
        response = session.get("https://serpapi.com/search", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching events info: {str(e)}")
        return {"error": f"Events API request failed: {str(e)}"}
