import os
from serpapi import GoogleSearch
from datetime import datetime
import json
from typing import Dict, List, Optional

class TravelAPI:
    def __init__(self):
        self.api_key = os.getenv('SERPAPI_KEY')
        if not self.api_key:
            raise ValueError("SERPAPI_KEY environment variable is not set")

    def search_flights(self, 
                      origin: str, 
                      destination: str, 
                      departure_date: str,
                      return_date: Optional[str] = None) -> List[Dict]:
        """
        Search for flights using SerpAPI
        """
        params = {
            "engine": "google_flights",
            "departure_id": origin,
            "arrival_id": destination,
            "outbound_date": departure_date,
            "return_date": return_date,
            "api_key": self.api_key
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "error" in results:
            raise Exception(f"Error searching flights: {results['error']}")
            
        return results.get("flights", [])

    def search_hotels(self, 
                     location: str, 
                     check_in: str, 
                     check_out: str,
                     guests: int = 2) -> List[Dict]:
        """
        Search for hotels using SerpAPI
        """
        params = {
            "engine": "google_hotels",
            "q": f"hotels in {location}",
            "check_in": check_in,
            "check_out": check_out,
            "guests": guests,
            "api_key": self.api_key
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "error" in results:
            raise Exception(f"Error searching hotels: {results['error']}")
            
        return results.get("hotels", [])

    def search_restaurants(self, 
                         location: str, 
                         cuisine: Optional[str] = None) -> List[Dict]:
        """
        Search for restaurants using SerpAPI
        """
        query = f"restaurants in {location}"
        if cuisine:
            query += f" {cuisine}"
            
        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key,
            "tbm": "lcl"  # Local results
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "error" in results:
            raise Exception(f"Error searching restaurants: {results['error']}")
            
        return results.get("local_results", []) 