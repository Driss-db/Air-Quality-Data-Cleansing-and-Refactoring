SELECT `stations`.`location` AS 'station_name', avg(`readings`.`pm2.5`) AS 'avg_pm2.5', avg(`readings`.`vpm2.5`) AS 'avg_vpm2.5'
FROM pollution_db2.readings
LEFT JOIN pollution_db2.stations ON `readings`.`station_id-fk` = `stations`.`station_id`
WHERE year(datetime) = '2019'  AND time(datetime) BETWEEN '07:30:00' AND '08:30:00'
GROUP BY `readings`.`station_id-fk`;