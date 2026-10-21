from src.raw_storage import read_raw_json
from pathlib import Path
import json
from datetime import date
from math import isfinite
from src.config import WEATHER_PARAMS

project_root = Path(__file__).resolve().parent.parent
fixture_path = project_root / "tests" / "fixtures" / "cairo_week.json"

#print(data)
def transform_weather_data(data, city_code, start_date, end_date):    
    if not isinstance(city_code, str) or not city_code.strip():
        raise ValueError("City code must be a non-empty string")
    
    if not isinstance(data, dict):
        raise ValueError("Weather data must be a dictionary")
    elif "daily" not in data :
        raise ValueError(" data must contain daily dictionary")
    
    if not isinstance(start_date,str) :
        raise ValueError("start_date must be a string")
    
    if not isinstance(end_date,str) :
        raise ValueError("end_date must be a string")
    
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    if start > end:
        raise ValueError("Start date must not be after end date")

    expected_units = {
    "time": "iso8601",
    "temperature_2m_max": "°C",
    "temperature_2m_min": "°C",
    "precipitation_sum": "mm",
    }
    if "daily_units" not in data:
        raise ValueError("Weather data must contain daily_units")
    units = data["daily_units"]
    if not isinstance(units, dict):
        raise ValueError("Daily units must be a dictionary")
    
    for field in expected_units : 
        if units.get(field) != expected_units[field]:
            raise ValueError(f"Missing or incorrect unit for {field}")
    
    daily = data["daily"]
    dailyList = []
    
    if not isinstance(daily, dict):
        raise ValueError("Daily data must be a dictionary")
    
    required_fields = (
    "time",
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
)
    
    for field in required_fields: 
        if(field not in daily ) :
            raise ValueError(f"Missing daily field: {field}")
        
        elif( not isinstance(daily[field] , list)) :
            raise ValueError(f"{field} must be a list")
           
        if (len(daily["time"]) != len(daily[field])) :
            raise ValueError(f"Daily field length does not match time: {field}")
        

    if (len(daily["time"]) < 1) :
        raise ValueError(f"day count must be 1 ore more")

    seen_dates = set()
    for i in range(len(daily['time'])) : 
        date_text = daily["time"][i]
        if not isinstance(date_text, str):
            raise ValueError(f"Weather date must be a string at index {i}")
        weather_date = date.fromisoformat(date_text)
        if not start <= weather_date <= end:
            raise ValueError(f"Weather date outside requested period: {date_text}")
        if weather_date in seen_dates:
            raise ValueError(f"Duplicate weather date: {date_text}")
        seen_dates.add(weather_date)
        
        for field in required_fields[1:]: 
            value = daily[field][i]
            if type(value) not in (int, float):
                raise ValueError(f"Invalid measurement in {field} at index {i}")
                  
            if not isfinite(value):
                raise ValueError(f"Non-finite measurement in {field} at index {i}")
                
            
            if (field == "precipitation_sum" and value < 0 ) :
                raise ValueError("precipitation_sum cant be negative")
            
            if (field != "precipitation_sum" and not (-100 <= value <= 70)):
                raise ValueError(f"Temperature out of range in {field} at index {i}")   
            
        if daily["temperature_2m_min"][i] > daily["temperature_2m_max"][i]:
            raise ValueError(f"Minimum temperature exceeds maximum at index {i}")
            
             
        dailyList.append({
        "city_code": city_code,
        "weather_date": weather_date,
        "temperature_max_c": daily["temperature_2m_max"][i],
        "temperature_min_c": daily["temperature_2m_min"][i],
        "precipitation_mm": daily["precipitation_sum"][i]    
        })
     
       
    expected_count = (end - start).days + 1
    if len(seen_dates) != expected_count:
        raise ValueError("Daily data does not cover every date in the requested period")

    return dailyList 
        
if __name__ == "__main__":
    data = json.loads(read_raw_json(fixture_path))
    transformed = transform_weather_data(  data, "cairo" ,  WEATHER_PARAMS["start_date"], WEATHER_PARAMS["end_date"], )  
    print(transformed)
    print(type(transformed[0]["weather_date"]))
    
    
  #  print(json.dumps(transformed, indent=4, ensure_ascii=False)) 



# Validate the input types, requested period, units, and required daily lists.
# For each day:
#   1. Parse the date and reject out-of-range or duplicate dates.
#   2. Validate the three measurements at the same index.
#   3. Ensure minimum temperature does not exceed maximum temperature.
#   4. Append one record containing that day's date and measurements.
# Verify that every date in the requested period is present, then return the records.


        
    

