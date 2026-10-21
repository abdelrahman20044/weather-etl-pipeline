select count(weather_date) as days_count from daily_weather 
WHERE city_code = 'cairo'
  AND weather_date >= '2026-01-01'
  AND weather_date < '2026-02-01'

select  top(1) with ties temperature_max_c , weather_date from daily_weather 
WHERE city_code = 'cairo'
  AND weather_date >= '2026-01-01'
  AND weather_date < '2026-02-01'
order by temperature_max_c desc

select avg(temperature_max_c) as avg_max_temp, SUM(precipitation_mm) as total_precip from daily_weather 
WHERE city_code = 'cairo'
  AND weather_date >= '2026-01-01'
  AND weather_date < '2026-02-01'

select weather_date,temperature_max_c ,temperature_max_c
    -lag(temperature_max_c)over( order by weather_date) as change_from_previous_day from daily_weather
WHERE city_code = 'cairo'
  AND weather_date >= '2026-01-01'
  AND weather_date < '2026-02-01'
  ORDER BY weather_date DESC;
  

-- another way for second query 
select weather_date , temperature_max_c from (select * , DENSE_RANK() over(order by temperature_max_c desc) as dn from daily_weather 
WHERE city_code = 'cairo'
  AND weather_date >= '2026-01-01'
  AND weather_date < '2026-02-01' ) as newtable where dn = 1