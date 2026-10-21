import os
import argparse
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

from src.config import WEATHER_API_URL, WEATHER_PARAMS
from src.extract import fetch_weather_data
from src.raw_storage import save_raw_json, read_raw_json
from src.transform import transform_weather_data
from src.load import load_weather_records

logger = logging.getLogger(__name__)

def run_pipeline(raw_file=None):
    logger.info(
        "Pipeline started: city=cairo, start=%s, end=%s, source=%s",
        WEATHER_PARAMS["start_date"],
        WEATHER_PARAMS["end_date"],
        "saved file" if raw_file is not None else "API",
    )
    project_root = Path(__file__).resolve().parent.parent
    load_dotenv(project_root / ".env")
    connection_string = os.getenv("WEATHER_DB_CONNECTION")
    if not connection_string or not connection_string.strip():
        raise ValueError("WEATHER_DB_CONNECTION is required")
    if raw_file is not None:
        saved_path = Path(raw_file)
        logger.info("Reading raw input: %s", saved_path.resolve())
        data = json.loads(read_raw_json(saved_path))
    else:
        logger.info("Requesting historical weather data")
        raw_json, data = fetch_weather_data(WEATHER_API_URL, WEATHER_PARAMS)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")

        filename = ( f"cairo_{WEATHER_PARAMS['start_date']}_"
                    f"{WEATHER_PARAMS['end_date']}_{timestamp}.json")

        saved_path = save_raw_json(raw_json , project_root / "data" / "raw" / filename)
        logger.info("Raw response saved: %s", saved_path)
    logger.info("Validating and transforming weather data")
    records = transform_weather_data(data , 'cairo' , WEATHER_PARAMS["start_date"] , WEATHER_PARAMS["end_date"])
    logger.info("Transformation completed: records=%s", len(records))
    result = load_weather_records(records , connection_string)
    logger.info(
        "Pipeline completed: inserted=%s, skipped=%s, raw_file=%s",
        result["inserted"], result["skipped"], saved_path,
    )
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the weather ETL pipeline.")
    parser.add_argument(
        "--raw-file",
        type=Path,
        help="Read a saved JSON response instead of requesting the API. Dates must match WEATHER_PARAMS.",
    )
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parent.parent
    log_file = project_root / "logs" / "pipeline.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
    )
    try:
        result = run_pipeline(raw_file=args.raw_file)
    except Exception:
        logger.exception("Pipeline failed")
        raise SystemExit(1)
