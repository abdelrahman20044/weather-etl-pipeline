CREATE DATABASE WeatherETL

GO
USE WeatherETL;
GO

CREATE TABLE dbo.daily_weather (
city_code VARCHAR(30) NOT NULL ,
weather_date DATE NOT NULL , 
temperature_max_c DECIMAL(5,2) NOT NULL,
temperature_min_c DECIMAL(5,2) NOT NULL,
precipitation_mm DECIMAL(8,2) NOT NULL ,      
CONSTRAINT PK_daily_weather PRIMARY KEY (city_code, weather_date),
CONSTRAINT CK_daily_weather_temperature CHECK (temperature_min_c <= temperature_max_c),
CONSTRAINT CK_daily_weather_precipitation CHECK (precipitation_mm >= 0)
)

SELECT DB_NAME() AS current_database;

SELECT *
FROM dbo.daily_weather;
