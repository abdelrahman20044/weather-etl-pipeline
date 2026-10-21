from pathlib import Path
from datetime import datetime, timezone
from src.config import WEATHER_API_URL, WEATHER_PARAMS
from src.extract import fetch_weather_data
import json

project_root = Path(__file__).resolve().parent.parent
raw_dir = project_root / "data" / "raw"
def save_raw_json(raw_json, file_path):
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("x", encoding="utf-8") as file:
        file.write(raw_json)
    return file_path
 
def read_raw_json(file_path) : 
    file_path = Path(file_path)
    return file_path.read_text(encoding="utf-8")
    
         
if __name__ == "__main__":
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    filename = f"cairo_2026-01-01_2026-01-07_{timestamp}.json"
    raw_json, data = fetch_weather_data(WEATHER_API_URL, WEATHER_PARAMS)

    saved_path = save_raw_json(raw_json, raw_dir / filename )
    saved_text = read_raw_json(saved_path)
    print(saved_path)
    print(saved_text == raw_json)  # Check that the saved and reloaded text exactly matches the source text.
    print(json.loads(saved_text) == data)  # Check that the reloaded JSON contains the same parsed data.
    
    
    
    
    
    
    
    
    
    
     
    
#     raw_dir.mkdir(parents=True, exist_ok= True)
#     file_path = raw_dir / "practice.txt"
#     file_path.write_text("Hello from raw storage",     encoding="utf-8")
#     print(raw_dir)
#     print(raw_dir.exists())
#     saved_text = file_path.read_text(encoding="utf-8")
#     print(saved_text)
    
    

    