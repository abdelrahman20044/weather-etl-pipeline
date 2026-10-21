import pyodbc
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from src.transform import transform_weather_data
from src.config import WEATHER_PARAMS
from src.raw_storage import read_raw_json
import logging 
logger = logging.getLogger(__name__)
def load_weather_records(records, connection_string):
    sql = """
    INSERT INTO dbo.daily_weather ( city_code, weather_date, temperature_max_c, temperature_min_c, precipitation_mm ) VALUES (?, ?, ?, ?, ?);
        """

    connection = None
    cursor = None
    try:
        logger.info("Loading started: %s records", len(records))
        connection = pyodbc.connect(connection_string, timeout=10)
        cursor = connection.cursor()
        inserted_count = 0
        skipped_count = 0
        for record in records:
            cursor.execute("""SELECT 1 FROM dbo.daily_weather WHERE city_code = ? AND weather_date = ?; """,
            record["city_code"], record["weather_date"],)
            
            existing_row = cursor.fetchone()
            if existing_row is not None:
                skipped_count += 1
                continue
            
            values = (
            record["city_code"],
            record["weather_date"],
            record["temperature_max_c"],
            record["temperature_min_c"],
            record["precipitation_mm"],
            )
            cursor.execute(sql, values)
            inserted_count += 1
        connection.commit()
        logger.info(
            "Loading completed: inserted=%s, skipped=%s",
             inserted_count, skipped_count, ) 

        return {
            "inserted": inserted_count,
            "skipped": skipped_count,
        }
        
    except Exception:
        if connection is not None:
            connection.rollback()
        logger.exception("Loading failed")
        raise
    finally:
        try:
            if cursor is not None:
                cursor.close()
        finally:
            if connection is not None:
                connection.close()

if __name__ == "__main__":
    
    project_root = Path(__file__).resolve().parent.parent
    log_dir = project_root / "logs" / "pipeline.log"
    log_dir.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO ,
        format= "%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers= [
            logging.StreamHandler(),
            logging.FileHandler(log_dir, encoding="utf-8") ,
        ] ,
    )
    load_dotenv(project_root / ".env")
    connection_string = os.getenv("WEATHER_DB_CONNECTION")
    if not connection_string or not connection_string.strip():
        raise ValueError("WEATHER_DB_CONNECTION is required")

    fixture_path = project_root / "tests" / "fixtures" / "cairo_week.json"
    logger.info(
    "Input: city=cairo, start=%s, end=%s, file=%s",
    WEATHER_PARAMS["start_date"],
    WEATHER_PARAMS["end_date"],
    fixture_path,)
    data = json.loads(read_raw_json(fixture_path))
    records = transform_weather_data(  data, "cairo" ,  WEATHER_PARAMS["start_date"], WEATHER_PARAMS["end_date"], )  
     
    load_weather_records (records, connection_string)
