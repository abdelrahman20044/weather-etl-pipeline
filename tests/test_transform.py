import json
import unittest
from pathlib import Path
from src.transform import transform_weather_data


class TestTransform(unittest.TestCase):
    def setUp(self):
        fixture = Path(__file__).resolve().parent / "fixtures" / "cairo_week.json"
        self.data = json.loads(fixture.read_text(encoding="utf-8"))

    def test_valid_week(self):
        
        records = transform_weather_data( self.data, "cairo", "2026-01-01", "2026-01-07")
        
        self.assertEqual(len(records), 7)
        self.assertEqual( records[0]["temperature_max_c"], self.data["daily"]["temperature_2m_max"][0], )

    def test_missing_measurement(self):
        self.data["daily"]["temperature_2m_max"][0] = None
        
        with self.assertRaises(ValueError):
            transform_weather_data(
            self.data, "cairo", "2026-01-01", "2026-01-07")  

    def test_unequal_lengths(self):
        self.data["daily"]["temperature_2m_max"].pop()

        with self.assertRaises(ValueError):
            transform_weather_data( self.data, "cairo", "2026-01-01", "2026-01-07" )  

    def test_duplicate_date(self):
        self.data["daily"]["time"][0]=self.data["daily"]["time"][1] 
        with self.assertRaises(ValueError):
            transform_weather_data( self.data, "cairo", "2026-01-01", "2026-01-07" )  

    

    