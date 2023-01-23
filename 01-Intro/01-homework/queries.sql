SELECT * from green_taxi_data limit 10;
-- INNER join
SELECT lpep_pickup_datetime,
	   lpep_pickup_datetime,
	   tip_amount,
	   passenger_count,
	   CONCAT(zpu."Borough", ' / ', zpu."Zone") As "pickup_loc",
	   CONCAT(zdo."Borough", ' / ', zdo."Zone") As "dropoff_loc"
FROM green_taxi_data gt,
	 zones zpu,
	 zones zdo
WHERE gt."PULocationID" = zpu."LocationID" 
AND gt."DOLocationID" = zdo."LocationID"
LIMIT 100;

-- another INNER join
SELECT lpep_pickup_datetime,
	   lpep_pickup_datetime,
	   tip_amount,
	   passenger_count,
	   CONCAT(zpu."Borough", ' / ', zpu."Zone") As "pickup_loc",
	   CONCAT(zdo."Borough", ' / ', zdo."Zone") As "dropoff_loc"
FROM green_taxi_data gt 
JOIN zones zpu ON gt."PULocationID" = zpu."LocationID"
JOIN zones zdo ON gt."DOLocationID" = zdo."LocationID"
LIMIT 100;

-- LEFT join (take all only from left table)
SELECT lpep_pickup_datetime,
	   lpep_pickup_datetime,
	   tip_amount,
	   passenger_count,
	   CONCAT(zpu."Borough", ' / ', zpu."Zone") As "pickup_loc",
	   CONCAT(zdo."Borough", ' / ', zdo."Zone") As "dropoff_loc"
FROM green_taxi_data gt LEFT JOIN zones zpu ON gt."PULocationID" = zpu."LocationID"
LEFT JOIN zones zdo ON gt."DOLocationID" = zdo."LocationID"
LIMIT 100;

-- OUTER join (take all from two tables)
SELECT lpep_pickup_datetime,
	   lpep_pickup_datetime,
	   tip_amount,
	   passenger_count,
	   CONCAT(zpu."Borough", ' / ', zpu."Zone") As "pickup_loc",
	   CONCAT(zdo."Borough", ' / ', zdo."Zone") As "dropoff_loc"
FROM green_taxi_data gt OUTER JOIN zones zpu ON gt."PULocationID" = zpu."LocationID"
OUTER JOIN zones zdo ON gt."DOLocationID" = zdo."LocationID"
LIMIT 100;


SELECT count(1)
from green_taxi_data
where 1=1
and lpep_pickup_datetime between '2019-01-15 00:00:00' and '2019-01-15 23:59:59'
and lpep_dropoff_datetime < '2019-01-15 23:59:59';

-- 20530

SELECT lpep_pickup_datetime::date as date, -- CAST(lpep_pickup_datetime AS DATE) as date
		max(trip_distance) as largest_distance
from green_taxi_data
GROUP BY 1
ORDER BY 2 DESC;

-- 2019-01-15

SELECT passenger_count, count(1)
from green_taxi_data
where 1=1
and lpep_pickup_datetime between '2019-01-01 00:00:00' and '2019-01-01 23:59:59'
and passenger_count in (2,3)
GROUP BY 1

-- 2: 1282 ; 3: 254

SELECT "DOLocationID", max(tip_amount)
from green_taxi_data
where 1=1
and "PULocationID" = 7
GROUP BY 1
ORDER BY 2 DESC;

-- 146