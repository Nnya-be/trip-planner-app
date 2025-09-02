import requests

def reverse_geocode(lat, lon):
    """
    Get location name from coordinates using OpenStreetMap Nominatim reverse geocoding.
    Returns a string name (city, town, or address).
    """
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        'lat': lat,
        'lon': lon,
        'format': 'json',
        'zoom': 10,
        'addressdetails': 1
    }
    headers = {
        'User-Agent': 'trip-planner-app/1.0 (your_email@example.com)'
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        address = data.get('address', {})
        # Prefer city, then town, then village, then state, then road
        name = address.get('city') or address.get('town') or address.get('village') or address.get('state') or address.get('road')
        if name:
            return name
        return data.get('display_name', 'Unknown location')
    except Exception:
        return 'Unknown location'
