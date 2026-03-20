import requests
import logging

logger = logging.getLogger(__name__)

def get_geo_insights(ip_or_domain):
    """
    Retrieves and integrates data from ip-api and restcountries.
    Performs data transformation by calculating population density.
    """
    print(f"\n--- [DEBUG] Starting Live Retrieval for: {ip_or_domain} ---")
    
    try:
        # 1. Location API call
        loc_res = requests.get(f"http://ip-api.com/json/{ip_or_domain}", timeout=10)
        loc_data = loc_res.json()
        
        if loc_data.get('status') != 'success':
            print(f"[DEBUG] Location API failed: {loc_data.get('message')}")
            return None

        country_name = loc_data.get('country')
        print(f"[DEBUG] Country Identified: {country_name}")

        # 2. Population API call
        pop_res = requests.get(
            f"https://restcountries.com/v3.1/name/{country_name}", 
            params={"fullText": "true"}, 
            timeout=10
        )
        pop_json = pop_res.json()

        # --- THE CRITICAL FIX ---
        # The API returns a LIST [ {...} ]. We must grab the first dictionary inside it.
        if isinstance(pop_json, list) and len(pop_json) > 0:
            pop_data = pop_json # This changes the type from list to dict
        else:
            print("[DEBUG] Population API returned an empty list or error.")
            return None

        # 3. Data Transformation (Calculation)
        # Now that pop_data is a dictionary, .get() will work perfectly
        population = pop_data.get('population', 0)
        area = pop_data.get('area', 0)
        
        # Calculation: Density = Population / Area
        density = population / area if area > 0 else 0
        
        print(f"[DEBUG] Transformation Successful. Density: {round(density, 2)}")

        # 4. Return Unified JSON Structure
        return {
            "city": loc_data.get('city'),
            "country": country_name,
            "coordinates": {
                "lat": loc_data.get('lat'), 
                "lon": loc_data.get('lon')
            },
            "population_stats": {
                "total_population": population,
                "land_area_sq_km": area,
                "density_per_sq_km": round(density, 2)
            },
            # Flags are nested: pop_data['flags']['png']
            "flag": pop_data.get('flags', {}).get('png')
        }

    except requests.exceptions.Timeout:
        print("[ERROR] Connection timed out. Network restricted.")
    except Exception as e:
        # This will catch the 'list' error if pop_data isn't handled correctly
        print(f"[ERROR] Unexpected error: {e}")

    return None