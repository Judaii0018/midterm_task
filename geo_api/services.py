import requests

def get_geo_insights(ip_or_domain):
    # 1. Call Location API
    loc_res = requests.get(f"http://ip-api.com/json/{ip_or_domain}")
    loc_data = loc_res.json()
    
    if loc_data.get('status') == 'fail':
        return None

    country_name = loc_data.get('country')

    # 2. Call Population API
    pop_res = requests.get(f"https://restcountries.com/v3.1/name/{country_name}?fullText=true")
    pop_data = pop_res.json()[0]

    # 3. Data Transformation & Combination
    population = pop_data.get('population', 0)
    area = pop_data.get('area', 0)
    
    # Compute at least one field: Population Density
    density = population / area if area > 0 else 0

    return {
        "city": loc_data.get('city'),
        "country": country_name,
        "coordinates": {"lat": loc_data.get('lat'), "lon": loc_data.get('lon')},
        "population_stats": {
            "total_population": population,
            "land_area_sq_km": area,
            "density_per_sq_km": round(density, 2) # Computed field
        },
        "flag": pop_data.get('flags', {}).get('png')
    }