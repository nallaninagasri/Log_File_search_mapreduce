# Log File Search and Error Detection Using MapReduce — BDA Additions

## Objective
Analyze application log records, classify ERROR/WARNING/INFO events, and summarize activity by severity and service.

## Dataset
`data/synthetic_logs_1000.csv` contains 1,000 generated demonstration records. They are synthetic, not real production logs.

## BDA concepts
- Ingestion: reading log records from CSV/text.
- Processing: checking consistent severity labels.
- MapReduce: mapper emits (level, 1); reducer totals each level.
- Aggregation: counts by severity and service.
- Hive: sample table and analytical queries.
- Visualization: severity and service charts.

## Run analysis
From this folder, run: `py scripts/analyze_logs.py`

## Hadoop note
The Hadoop mapper/reducer are Streaming examples. A working Hadoop installation and Streaming JAR are required. They have not been executed on a cluster in this package. Do not claim cluster execution unless you run them successfully.
