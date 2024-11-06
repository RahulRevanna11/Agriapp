import requests
from math import exp
from datetime import datetime, timedelta
import asyncio
import aiohttp
from typing import List, Dict
import pandas as pd
import numpy as np
import nest_asyncio

# Enable nested event loops (needed for Jupyter/IPython)
nest_asyncio.apply()

# Constants remain the same
Cn = 900
Cd = 0.34
Kc = 1.15
Eff = 0.85
LOCATION = "Sangli"
API_KEY = "9e2f039c7cfb45498bb123017241910"

async def fetch_weather_data_batch(session: aiohttp.ClientSession, location: str, dates: List[str]) -> List[Dict]:
    """Fetch weather data for multiple dates in parallel"""
    async def fetch_single_date(date: str):
        url = f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={location}&dt={date}"
        async with session.get(url) as response:
            return await response.json()
    
    # Create tasks for all dates
    tasks = [fetch_single_date(date) for date in dates]
    return await asyncio.gather(*tasks)

def calculate_ET0(Tmax, Tmin, RHmean, u2, Rs):
    # Calculation remains the same but vectorized for pandas
    es = 0.6108 * (np.exp((17.27 * Tmax) / (Tmax + 237.3)) + np.exp((17.27 * Tmin) / (Tmin + 237.3))) / 2
    ea = es * RHmean / 100
    Rn = Rs * 0.408
    Tmean = (Tmax + Tmin) / 2
    delta = 4098 * es / ((Tmean + 237.3) ** 2)
    gamma = 0.665 * 101.3 / 1000
    ET0 = (0.408 * delta * Rn + gamma * Cn * u2 * (es - ea) / (Tmean + 273)) / (delta + gamma * (1 + Cd * u2))
    return ET0

def calculate_daily_irrigation_requirement(ET0, effective_precipitation):
    ETa = Kc * ET0
    return (ETa - effective_precipitation) / Eff

async def calculate_irrigation_past_year(location: str):
    # Generate all dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    dates = [(start_date + timedelta(days=x)).strftime('%Y-%m-%d') 
             for x in range((end_date - start_date).days + 1)]
    
    # Create batches of dates (to avoid overwhelming the API)
    BATCH_SIZE = 20
    date_batches = [dates[i:i + BATCH_SIZE] for i in range(0, len(dates), BATCH_SIZE)]
    
    all_weather_data = []
    async with aiohttp.ClientSession() as session:
        for batch in date_batches:
            batch_data = await fetch_weather_data_batch(session, location, batch)
            all_weather_data.extend(batch_data)
    
    # Process all data at once using pandas
    records = []
    for date, weather in zip(dates, all_weather_data):
        day_data = weather['forecast']['forecastday'][0]
        records.append({
            'date': date,
            'Tmax': day_data['day']['maxtemp_c'],
            'Tmin': day_data['day']['mintemp_c'],
            'RHmean': day_data['day']['avghumidity'],
            'u2': day_data['day']['maxwind_kph'] * 1000 / 3600,
            'Rs': day_data['day']['uv'],
            'precipitation': day_data['day']['totalprecip_mm']
        })
    
    # Convert to DataFrame for vectorized operations
    df = pd.DataFrame(records)
    
    # Calculate irrigation requirements in vectorized form
    df['ET0'] = calculate_ET0(
        df['Tmax'], df['Tmin'], df['RHmean'], df['u2'], df['Rs']
    )
    df['irrigation_mm'] = calculate_daily_irrigation_requirement(
        df['ET0'], df['precipitation']
    )
    df['irrigation_L_per_ha'] = df['irrigation_mm'] * 10000
    
    # Format results
    results = []
    for _, row in df.iterrows():
        if row['irrigation_mm'] < 0:
            results.append(f"{row['date']}: No irrigation needed (Excess moisture)")
        else:
            results.append(f"{row['date']}: {row['irrigation_L_per_ha']:.2f} L/ha")
    
    return results

def run_irrigation_calculation(location: str):
    """Wrapper function to handle async execution"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(calculate_irrigation_past_year(location))

if __name__ == "__main__":
    # Install required packages if not already installed
    try:
        import nest_asyncio
    except ImportError:
        print("Installing required packages...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'nest_asyncio', 'aiohttp', 'pandas', 'numpy'])
        import nest_asyncio
    
    # Run the calculation
    results = run_irrigation_calculation(LOCATION)
    
    print("Daily irrigation water requirements (L/ha) for each day in the past year:")
    for result in results:
        print(result)