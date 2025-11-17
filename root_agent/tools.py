import os
from serpapi import GoogleSearch
from dotenv import load_dotenv
from typing import Optional, Any, Dict, List


load_dotenv()

# replace the below api_key with the value from your .env file
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def search_hotels(
    query: str,
    check_in_date: str,
    check_out_date: str,
    currency: str = "USD",
    hl: str = "en",
    gl: str = "us",
) -> Dict[str, Any]:
    """Search hotels using SerpAPI Google Hotels.

    This tool queries SerpAPI's google_hotels engine and returns a dict indicating
    success or error. On success the raw SerpAPI response is returned under "results".

    Args:
        query: Search text, e.g. "Bali Resorts" or "Near the Eiffel Tower in Paris".
        check_in_date: Check-in date in YYYY-MM-DD format.
        check_out_date: Check-out date in YYYY-MM-DD format.
        currency: Currency code (default "USD").
        hl: Language (default "en").
        gl: Geo region (default "us").

    Returns:
        On success: {"status": "success", "results": <serpapi response dict>}
        On error:   {"status": "error", "error_message": "<message>"}
    """
    try:
        if not query:
            return {"status": "error", "error_message": "query is required"}
        if not check_in_date or not check_out_date:
            return {
                "status": "error",
                "error_message": "check_in_date and check_out_date are required",
            }

        params: Dict[str, Any] = {
            "api_key": SERPAPI_API_KEY,
            "engine": "google_hotels",
            "q": query,
            "hl": hl,
            "gl": gl,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "currency": currency,
        }

        client = GoogleSearch(params)
        results = client.get_dict() if hasattr(client, "get_dict") else client.get_json()
        top_hotels = _top_n_hotels_from_results(results, n=3)
        return {"status": "success", "results": top_hotels}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}


def _top_n_hotels_from_results(results: Dict[str, Any], n: int = 3) -> List[Dict[str, Any]]:
    """Extract and return top-n hotels from raw SerpAPI hotels response.

    Sorting: primary by overall_rating (descending), secondary by numeric price (ascending).
    Uses 'properties' and 'ads' lists from the response when available.
    """
    # Collect candidates from 'properties' and 'ads' (both may exist)
    candidates: List[Dict[str, Any]] = []
    props = results.get("properties") or []
    ads = results.get("ads") or []
    if isinstance(props, list):
        candidates.extend(props)
    if isinstance(ads, list):
        candidates.extend(ads)

    def rating_of(p: Dict[str, Any]) -> float:
        # try common rating keys
        for key in ("overall_rating", "overallRating", "rating"):
            if key in p and p[key] is not None:
                try:
                    return float(p[key])
                except Exception:
                    pass
        return 0.0

    def price_of(p: Dict[str, Any]) -> Optional[float]:
        # prefer extracted_price, then extracted_lowest, then rate_per_night / price fields
        if "extracted_price" in p and p["extracted_price"] is not None:
            return _safe_cast_price(p["extracted_price"])
        rp = p.get("rate_per_night") or {}
        if isinstance(rp, dict) and "extracted_lowest" in rp and rp["extracted_lowest"] is not None:
            return _safe_cast_price(rp["extracted_lowest"])
        if "extracted_lowest" in p:
            return _safe_cast_price(p.get("extracted_lowest"))
        if "price" in p:
            return _safe_cast_price(p.get("price"))
        # some items include total_rate / prices list
        tr = p.get("total_rate") or {}
        if isinstance(tr, dict) and "extracted_lowest" in tr:
            return _safe_cast_price(tr.get("extracted_lowest"))
        # fallback None
        return None

    enriched = []
    for p in candidates:
        enriched.append({
            "raw": p,
            "rating": rating_of(p),
            "price_numeric": price_of(p)
        })

    # sort: rating desc, price asc (None price goes to end)
    enriched_sorted = sorted(
        enriched,
        key=lambda x: (-x["rating"], x["price_numeric"] if x["price_numeric"] is not None else float("inf"))
    )

    top: List[Dict[str, Any]] = []
    for item in enriched_sorted[:n]:
        p = item["raw"]
        top.append({
            "id": p.get("property_token") or p.get("id") or p.get("name"),
            "name": p.get("name") or p.get("title"),
            "rating": item["rating"],
            "price": (
                p.get("extracted_price")
                or (p.get("rate_per_night", {}) or {}).get("extracted_lowest")
                or p.get("price")
                or (p.get("total_rate", {}) or {}).get("extracted_lowest")
            ),
            "address": p.get("link") or p.get("serpapi_property_details_link"),
            "amenities": p.get("amenities"),
            "raw": p
        })
    return top

def _safe_cast_price(value: Optional[Any]) -> Optional[float]:
    """Return numeric price if possible, else None."""
    if value is None:
        return None
    try:
        return float(value)
    except Exception:
        try:
            import re
            num = re.sub(r"[^\d.]", "", str(value))
            return float(num) if num else None
        except Exception:
            return None


def search_flight(
    originLocationCode: str,
    destinationLocationCode: str,
    departureDate: str,
    returnDate: Optional[str] = None,
    adults: int = 1,
    travelClass: Optional[str] = None,
    hl: str = "en",
    gl: str = "us",
    currency: str = "USD",
) -> Dict[str, Any]:
    """Search flights using SerpAPI Google Flights.

    This tool queries SerpAPI's google_flights engine and returns a dict indicating
    success or error. On success the raw SerpAPI response is returned under "results".

    Args:
        originLocationCode: Origin IATA Airport code (e.g. "JFK").
        destinationLocationCode: Destination IATA Airport code (e.g. "CDG").
        departureDate: Outbound date in YYYY-MM-DD.
        returnDate: Optional return date in YYYY-MM-DD.
        adults: Number of adult passengers (default 1).
        travelClass: Optional travel class string, e.g. "business" or "economy" (default economy).
        hl: Language (default "en").
        gl: Geo region (default "us").
        currency: Currency code (default "USD").

    Returns:
        On success: {"status": "success", "results": <serpapi response dict>}
        On error:   {"status": "error", "error_message": "<message>"}
    """
    try:
        if not originLocationCode or not destinationLocationCode or not departureDate:
            return {
                "status": "error",
                "error_message": "originLocationCode, destinationLocationCode and departureDate are required",
            }

        params: Dict[str, Any] = {
            "api_key": SERPAPI_API_KEY,
            "engine": "google_flights",
            "hl": hl,
            "gl": gl,
            "departure_id": originLocationCode,
            "arrival_id": destinationLocationCode,
            "outbound_date": departureDate,
            "currency": currency,
            "adults": adults,
        }
        if returnDate:
            params["return_date"] = returnDate
        if travelClass:
            params["travel_class"] = travelClass

        client = GoogleSearch(params)
        results = _safe_get_dict(client)
        top_flights = _top_n_flights_from_results(results, n=3)
        return {"status": "success", "results": top_flights}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

def _top_n_flights_from_results(results: Dict[str, Any], n: int = 3) -> List[Dict[str, Any]]:
    """Extract and return top-n flights from raw SerpAPI flights response."""
    flights_list = results.get("best_flights") or results.get("other_flights") or []
    if not isinstance(flights_list, list):
        return []

    def price_key(f: Dict[str, Any]) -> float:
        try:
            return float(f.get("price") or 0.0)
        except Exception:
            return 0.0

    sorted_flights = sorted(flights_list, key=lambda f: price_key(f))
    top = []
    for f in sorted_flights[:n]:
        top.append({
            "price": f.get("price"),
            "total_duration": f.get("total_duration"),
            "type": f.get("type"),
            "airline_logo": f.get("airline_logo"),
            "flights": f.get("flights"),
            "layovers": f.get("layovers"),
            "raw": f
        })
    return top

def _safe_get_dict(client: Any) -> Dict[str, Any]:
    """Call the client in a compatible way and return dict result."""
    if hasattr(client, "get_dict"):
        return client.get_dict()
    if hasattr(client, "get_json"):
        # some versions return JSON string; try to parse if needed
        res = client.get_json()
        if isinstance(res, str):
            import json
            return json.loads(res)
        return res
    # fallback to client.search if available
    if hasattr(client, "search"):
        return client.search()
    raise RuntimeError("Cannot extract JSON/dict from serpapi client")


if __name__ == "__main__":
    print(search_hotels(query="Near the Eiffel Tower in Paris", check_in_date="2025-11-19", check_out_date="2025-11-25"))
    print(search_flight(originLocationCode="JFK", destinationLocationCode="CDG", departureDate="2025-11-19", returnDate="2025-11-25"))
