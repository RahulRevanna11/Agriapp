# from flask import Flask, request, jsonify
# import requests
# from math import exp
# from datetime import datetime, timedelta
# import asyncio
# import aiohttp
# from typing import List, Dict
# import pandas as pd
# import numpy as np
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})

# # Constants for calculations
# Cn = 900  # Penman-Monteith equation constant
# Cd = 0.34  # Penman-Monteith equation constant
# Eff = 0.85  # Irrigation system efficiency
# API_KEY = "9e2f039c7cfb45498bb123017241910"  # Replace with your WeatherAPI key

# # Crop coefficients and growth stages
# CROP_COEFFICIENTS = {
#     "maize": {
#         "initial": 0.3,
#         "mid": 1.15,
#         "late": 0.7,
#         "duration": {
#             "initial": 20,
#             "development": 35,
#             "mid": 40,
#             "late": 30
#         }
#     },
#     "wheat": {
#         "initial": 0.3,
#         "mid": 1.15,
#         "late": 0.4,
#         "duration": {
#             "initial": 15,
#             "development": 25,
#             "mid": 50,
#             "late": 30
#         }
#     },
#     "rice": {
#         "initial": 1.05,
#         "mid": 1.20,
#         "late": 0.9,
#         "duration": {
#             "initial": 30,
#             "development": 30,
#             "mid": 60,
#             "late": 30
#         }
#     },
#     "cotton": {
#         "initial": 0.35,
#         "mid": 1.20,
#         "late": 0.6,
#         "duration": {
#             "initial": 30,
#             "development": 50,
#             "mid": 55,
#             "late": 45
#         }
#     },
#     "sugarcane": {
#         "initial": 0.4,
#         "mid": 1.25,
#         "late": 0.75,
#         "duration": {
#             "initial": 50,
#             "development": 70,
#             "mid": 220,
#             "late": 140
#         }
#     }
# }

# def get_crop_coefficient(crop_name: str, days_from_planting: int) -> float:
#     """
#     Calculate the crop coefficient (Kc) based on growth stage.
    
#     Args:
#         crop_name (str): Name of the crop
#         days_from_planting (int): Number of days since planting
        
#     Returns:
#         float: Crop coefficient value
#     """
#     if crop_name not in CROP_COEFFICIENTS:
#         raise ValueError(f"Crop '{crop_name}' not supported")
    
#     crop_data = CROP_COEFFICIENTS[crop_name]
#     durations = crop_data['duration']
    
#     # Calculate stage boundaries
#     initial_stage = durations['initial']
#     dev_stage = durations['development']
#     mid_stage = durations['mid']
#     late_stage = durations['late']
    
#     # Determine growth stage and calculate coefficient
#     if days_from_planting <= initial_stage:
#         return crop_data['initial']
#     elif days_from_planting <= initial_stage + dev_stage:
#         # Linear interpolation during development stage
#         progress = (days_from_planting - initial_stage) / dev_stage
#         return crop_data['initial'] + (crop_data['mid'] - crop_data['initial']) * progress
#     elif days_from_planting <= initial_stage + dev_stage + mid_stage:
#         return crop_data['mid']
#     elif days_from_planting <= initial_stage + dev_stage + mid_stage + late_stage:
#         # Linear interpolation during late stage
#         progress = (days_from_planting - (initial_stage + dev_stage + mid_stage)) / late_stage
#         return crop_data['mid'] + (crop_data['late'] - crop_data['mid']) * progress
#     else:
#         return crop_data['late']

# async def fetch_weather_data(session: aiohttp.ClientSession, location: str, date: str) -> Dict:
#     """
#     Fetch weather data for a specific date and location.
    
#     Args:
#         session (aiohttp.ClientSession): Async HTTP session
#         location (str): Location name
#         date (str): Date in YYYY-MM-DD format
        
#     Returns:
#         Dict: Weather data
#     """
#     url = f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={location}&dt={date}"
#     async with session.get(url) as response:
#         return await response.json()

# async def fetch_weather_data_batch(session: aiohttp.ClientSession, location: str, dates: List[str]) -> List[Dict]:
#     """
#     Fetch weather data for multiple dates in parallel.
    
#     Args:
#         session (aiohttp.ClientSession): Async HTTP session
#         location (str): Location name
#         dates (List[str]): List of dates
        
#     Returns:
#         List[Dict]: List of weather data for each date
#     """
#     tasks = [fetch_weather_data(session, location, date) for date in dates]
#     return await asyncio.gather(*tasks)

# def calculate_ET0(Tmax: float, Tmin: float, RHmean: float, u2: float, Rs: float) -> float:
#     """
#     Calculate reference evapotranspiration (ET0) using the Penman-Monteith equation.
    
#     Args:
#         Tmax (float): Maximum temperature (°C)
#         Tmin (float): Minimum temperature (°C)
#         RHmean (float): Mean relative humidity (%)
#         u2 (float): Wind speed at 2m height (m/s)
#         Rs (float): Solar radiation (MJ/m²/day)
        
#     Returns:
#         float: Reference evapotranspiration (mm/day)
#     """
#     # Calculate vapor pressure
#     es = 0.6108 * (np.exp((17.27 * Tmax) / (Tmax + 237.3)) + 
#                    np.exp((17.27 * Tmin) / (Tmin + 237.3))) / 2
#     ea = es * RHmean / 100
    
#     # Calculate net radiation
#     Rn = Rs * 0.408
    
#     # Calculate other parameters
#     Tmean = (Tmax + Tmin) / 2
#     delta = 4098 * es / ((Tmean + 237.3) ** 2)
#     gamma = 0.665 * 101.3 / 1000
    
#     # Calculate ET0
#     ET0 = (0.408 * delta * Rn + gamma * Cn * u2 * (es - ea) / (Tmean + 273)) / (delta + gamma * (1 + Cd * u2))
#     return max(0, ET0)  # Ensure non-negative value

# def calculate_daily_irrigation_requirement(ET0: float, effective_precipitation: float, Kc: float) -> float:
#     """
#     Calculate daily irrigation requirement.
    
#     Args:
#         ET0 (float): Reference evapotranspiration
#         effective_precipitation (float): Effective precipitation
#         Kc (float): Crop coefficient
        
#     Returns:
#         float: Daily irrigation requirement (mm)
#     """
#     ETc = Kc * ET0  # Crop evapotranspiration
#     irrigation_requirement = (ETc - effective_precipitation) / Eff
#     return max(0, irrigation_requirement)  # Ensure non-negative value

# async def calculate_irrigation_for_crop(location: str, crop_name: str, start_date: str) -> List[Dict]:
#     """
#     Calculate irrigation requirements for entire crop growth period.
    
#     Args:
#         location (str): Location name
#         crop_name (str): Name of the crop
#         start_date (str): Start date in YYYY-MM-DD format
        
#     Returns:
#         List[Dict]: Daily irrigation requirements
#     """
#     # Parse start date
#     start_date = datetime.strptime(start_date, '%Y-%m-%d')
    
#     # Calculate crop duration
#     crop_duration = sum(CROP_COEFFICIENTS[crop_name]['duration'].values())
    
#     # Generate dates for the entire growth period
#     dates = [(start_date - timedelta(days=x)).strftime('%Y-%m-%d') 
#              for x in range(crop_duration)]
    
#     # Fetch weather data in batches
#     BATCH_SIZE = 20
#     date_batches = [dates[i:i + BATCH_SIZE] for i in range(0, len(dates), BATCH_SIZE)]
    
#     all_weather_data = []
#     async with aiohttp.ClientSession() as session:
#         for batch in date_batches:
#             batch_data = await fetch_weather_data_batch(session, location, batch)
#             all_weather_data.extend(batch_data)
    
#     # Process data and calculate requirements
#     results = []
#     ind=0
#     for i, (date, weather) in enumerate(zip(dates, all_weather_data)):
#         try:
#             day_data = weather['forecast']['forecastday'][0]['day']
            
#             # Get crop coefficient for current growth stage
#             Kc = get_crop_coefficient(crop_name, i)
            
#             # Calculate ET0
#             ET0 = calculate_ET0(
#                 day_data['maxtemp_c'],
#                 day_data['mintemp_c'],
#                 day_data['avghumidity'],
#                 day_data['maxwind_kph'] * 1000 / 3600,  # Convert to m/s
#                 day_data['uv']
#             )
            
#             # Calculate irrigation requirement
#             irrigation_mm = calculate_daily_irrigation_requirement(
#                 ET0,
#                 day_data['totalprecip_mm'],
#                 Kc
#             )
            
#             # Convert to L/ha (1 mm = 10000 L/ha)
#             irrigation_L_per_ha = irrigation_mm * 10000
#             date=start_date+timedelta(days=ind)
#             results.append({
#                 'date': date
#                 ,
#                 'irrigation_needed': bool(irrigation_mm > 0),  # Convert to Python boolean
#                 'irrigation_L_per_ha': float(irrigation_L_per_ha),
#                 'Kc': float(Kc)
#             })
#             ind=ind+1
#         except Exception as e:
#             print(f"Error processing data for date {date}: {str(e)}")
#             continue
    
#     return results

# @app.route('/calculate_irrigation', methods=['POST'])
# async def calculate_irrigation():
#     """API endpoint for irrigation calculations"""
#     try:
#         data = request.get_json()
#         print(data)
#         # Validate input
#         required_fields = ['crop_name', 'start_date', 'location']
#         if not all(field in data for field in required_fields):
#             return jsonify({
#                 'error': 'Missing required fields',
#                 'required_fields': required_fields
#             }), 400
        
#         crop_name = data['crop_name'].lower()
#         start_date = data['start_date']
#         location = data['location']
        
#         # Validate crop name
#         if crop_name not in CROP_COEFFICIENTS:
#             return jsonify({
#                 'error': 'Invalid crop name',
#                 'supported_crops': list(CROP_COEFFICIENTS.keys())
#             }), 400
        
#         # Calculate irrigation requirements
#         results = await calculate_irrigation_for_crop(location, crop_name, start_date)
        
#         return jsonify({
#             'crop_name': crop_name,
#             'location': location,
#             'daily_requirements': results
#         })
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)




from flask import Flask, request, jsonify
import requests
from math import exp
from datetime import datetime, timedelta
import asyncio
import aiohttp
from typing import List, Dict
import pandas as pd
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Constants for calculations
Cn = 900  # Penman-Monteith equation constant
Cd = 0.34  # Penman-Monteith equation constant
Eff = 0.85  # Irrigation system efficiency
WEATHER_API_URL = "https://archive-api.open-meteo.com/v1/archive"

# Crop coefficients and growth stages
CROP_COEFFICIENTS = {
    "maize": {
        "initial": 0.3,
        "mid": 1.15,
        "late": 0.7,
        "duration": {
            "initial": 20,
            "development": 35,
            "mid": 40,
            "late": 30
        }
    },
    "wheat": {
        "initial": 0.3,
        "mid": 1.15,
        "late": 0.4,
        "duration": {
            "initial": 15,
            "development": 25,
            "mid": 50,
            "late": 30
        }
    },
    "rice": {
        "initial": 1.05,
        "mid": 1.20,
        "late": 0.9,
        "duration": {
            "initial": 30,
            "development": 30,
            "mid": 60,
            "late": 30
        }
    },
    "cotton": {
        "initial": 0.35,
        "mid": 1.20,
        "late": 0.6,
        "duration": {
            "initial": 30,
            "development": 50,
            "mid": 55,
            "late": 45
        }
    },
    "sugarcane": {
        "initial": 0.4,
        "mid": 1.25,
        "late": 0.75,
        "duration": {
            "initial": 50,
            "development": 70,
            "mid": 140,
            "late": 60
        }
    }
}
def get_crop_coefficient(crop_name: str, days_from_planting: int) -> float:
    """
    Calculate the crop coefficient (Kc) based on growth stage.
    
    Args:
        crop_name (str): Name of the crop
        days_from_planting (int): Number of days since planting
        
    Returns:
        float: Crop coefficient value
    """
    if crop_name not in CROP_COEFFICIENTS:
        raise ValueError(f"Crop '{crop_name}' not supported")
    
    crop_data = CROP_COEFFICIENTS[crop_name]
    durations = crop_data['duration']
    
    # Calculate stage boundaries
    initial_stage = durations['initial']
    dev_stage = durations['development']
    mid_stage = durations['mid']
    late_stage = durations['late']
    
    # Determine growth stage and calculate coefficient
    if days_from_planting <= initial_stage:
        return crop_data['initial']
    elif days_from_planting <= initial_stage + dev_stage:
        # Linear interpolation during development stage
        progress = (days_from_planting - initial_stage) / dev_stage
        return crop_data['initial'] + (crop_data['mid'] - crop_data['initial']) * progress
    elif days_from_planting <= initial_stage + dev_stage + mid_stage:
        return crop_data['mid']
    elif days_from_planting <= initial_stage + dev_stage + mid_stage + late_stage:
        # Linear interpolation during late stage
        progress = (days_from_planting - (initial_stage + dev_stage + mid_stage)) / late_stage
        return crop_data['mid'] + (crop_data['late'] - crop_data['mid']) * progress
    else:
        return crop_data['late']

async def fetch_weather_data(latitude: float, longitude: float, start_date: str, end_date: str) -> Dict:
    """
    Fetch weather data for a specific date range and location.
    
    Args:
        latitude (float): Latitude of the location
        longitude (float): Longitude of the location
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
        
    Returns:
        Dict: Weather data
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,et0_fao_evapotranspiration"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(WEATHER_API_URL, params=params) as response:
            print(response)
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Error fetching weather data: {await response.text()}")

def calculate_daily_irrigation_requirement(ET0: float, effective_precipitation: float, Kc: float) -> float:
    """
    Calculate daily irrigation requirement.
    
    Args:
        ET0 (float): Reference evapotranspiration
        effective_precipitation (float): Effective precipitation
        Kc (float): Crop coefficient
        
    Returns:
        float: Daily irrigation requirement (mm)
    """
    ETc = Kc * ET0  # Crop evapotranspiration
    irrigation_requirement = (ETc - effective_precipitation) / Eff
    return max(0, irrigation_requirement)  # Ensure non-negative value

async def calculate_irrigation_for_crop(latitude: float, longitude: float, crop_name: str, start_date: str) -> List[Dict]:
    """
    Calculate irrigation requirements for entire crop growth period.
    
    Args:
        latitude (float): Latitude of the location
        longitude (float): Longitude of the location
        crop_name (str): Name of the crop
        start_date (str): Start date in YYYY-MM-DD format
        
    Returns:
        List[Dict]: Daily irrigation requirements
    """
    # Parse start date
    start_date = datetime.strptime(start_date, '%Y-%m-%d')-timedelta(days=365)
    
    # Calculate crop duration
    crop_duration = sum(CROP_COEFFICIENTS[crop_name]['duration'].values())
    
    # Generate dates for the entire growth period moving forward
    dates = [(start_date + timedelta(days=x)).strftime('%Y-%m-%d') 
             for x in range(crop_duration)]
    
    # Fetch weather data
    print(dates[-1])
    try:
        weather_data = await fetch_weather_data(latitude, longitude, dates[0], dates[-1])
    except Exception as e:
        print(dates[-1])
        raise Exception(f"Error fetching weather data: {str(e)}")
    
    # Process data and calculate requirements
    results = []
    for i, date in enumerate(dates):
        try:
            day_data = weather_data['daily']
        except KeyError:
            raise Exception(f"Invalid weather data format. Missing 'daily' key.")
        
        # Get crop coefficient for current growth stage
        Kc = get_crop_coefficient(crop_name, i)
        
        # Calculate irrigation requirement
        irrigation_req = calculate_daily_irrigation_requirement(
            day_data['et0_fao_evapotranspiration'][i],
            day_data['precipitation_sum'][i],
            Kc
        )
        type(date)
        results.append({
            "date": (datetime.strptime(date, '%Y-%m-%d')+timedelta(days=365)).strftime('%Y-%m-%d')  ,
            "irrigation_L_per_ha": irrigation_req
        })
    
    return results



@app.route('/irrigation', methods=['POST'])
async def irrigation_endpoint():
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']

    crop_name = data['crop_name']
    start_date = data['start_date']
    results = await calculate_irrigation_for_crop(latitude, longitude, crop_name, start_date)
    return jsonify({'crop_name':crop_name,'daily_requirements':results,})

if __name__ == '__main__':
    app.run(debug=True,port=5001)