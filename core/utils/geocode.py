import requests

def geocode_location(location_name):
    """
    Geocode a location name using OpenStreetMap Nominatim API.
    Returns (lat, lng) tuple for a location string.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': location_name,
        'format': 'json',
        'limit': 1
    }
    headers = {
        'User-Agent': 'trip-planner-app/1.0 (solomonchamamme@gmail.com)'
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data:
            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return (lon, lat)
    except Exception:
        pass
    return (0.0, 0.0)
