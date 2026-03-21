import requests
import logging

logger = logging.getLogger(__name__)

def get_country_insights(country_name):
    """
    Retrieves country data directly from restcountries API
    and calculates population density.
    """

    logger.info(f"Fetching data for country: {country_name}")

    try:
        res = requests.get(
            f"https://restcountries.com/v3.1/name/{country_name}",
            timeout=10
        )
        res.raise_for_status()
        data = res.json()

        if not isinstance(data, list) or len(data) == 0:
            logger.error("No country data found.")
            return None

        country = data[0]

        # Extract values
        population = country.get('population', 0)
        area = country.get('area', 0)
        density = population / area if area else 0

        # Coordinates (latlng = [lat, lon])
        latlng = country.get('latlng', [None, None])

        return {
            "country": country.get('name', {}).get('common'),
            "capital": country.get('capital', [None])[0],
            "region": country.get('region'),
            "coordinates": {
                "lat": latlng[0],
                "lon": latlng[1]
            },
            "population_stats": {
                "total_population": population,
                "land_area_sq_km": area,
                "density_per_sq_km": round(density, 2)
            },
            "flag": country.get('flags', {}).get('png')
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

    return None