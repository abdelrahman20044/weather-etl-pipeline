import requests 
from src.config import WEATHER_API_URL, WEATHER_PARAMS
import json

# print(data["daily"].keys())
#print(json.dumps(data, indent=4, ensure_ascii=False)) ##
#daily_data = data["daily"] 

def fetch_weather_data(url, params):
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status() # Raise HTTPError for 4xx or 5xx
    raw_json = response.text  # Get the response body as decoded JSON text for raw storage.
    data = response.json()  # Parse the JSON response into Python objects; this response becomes a dictionary.  
    return raw_json, data 
   
if __name__ == "__main__":
    raw_json, data = fetch_weather_data(WEATHER_API_URL, WEATHER_PARAMS)
    print(data.keys())   
    print(json.dumps(data, indent=4, ensure_ascii=False))#dict > str
    print(type(raw_json)) #str
    print(type(data))   #dict
    print(raw_json)
    print('\n ...........................')
    print(data)
    
    #python see json as str so we parese int dict to use it
    
    # we send the api body with the file we want to save the body in and then make a folder of the parent path of this file if not exists and if exists we have exist_ok = true and then write the data to the file and then return the file path