-- Example Hive table (adapt LOCATION to your HDFS folder)
CREATE EXTERNAL TABLE IF NOT EXISTS log_records (
 record_id INT, log_timestamp STRING, level STRING,
 service STRING, message STRING, synthetic_data STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/log_records'
TBLPROPERTIES ('skip.header.line.count'='1');

SELECT level, COUNT(*) AS total_records
FROM log_records GROUP BY level ORDER BY total_records DESC;

SELECT service, COUNT(*) AS error_count
FROM log_records WHERE level='ERROR'
GROUP BY service ORDER BY error_count DESC;

SELECT * FROM log_records
WHERE LOWER(message) LIKE '%failed%';
