SELECT `readings`.`datetime` AS date_time, `stations`.`location` AS station_name, MAX(`readings`.`nox`) AS max_nox
FROM pollution_db2.readings
LEFT JOIN pollution_db2.stations ON `readings`.`station_id-fk` = `stations`.`station_id`
WHERE  year(datetime) = '2019';