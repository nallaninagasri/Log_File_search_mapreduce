import csv
from collections import Counter
from pathlib import Path
base = Path(__file__).resolve().parents[1]
counts, services = Counter(), Counter()
with (base/"data/synthetic_logs_1000.csv").open(newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        counts[row["level"]] += 1
        services[row["service"]] += 1
with (base/"results/level_summary.csv").open("w", newline="", encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["log_level","record_count"])
    for k in ["ERROR","WARNING","INFO"]: w.writerow([k,counts[k]])
with (base/"results/service_summary.csv").open("w", newline="", encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["service","record_count"])
    for k,v in services.most_common(): w.writerow([k,v])
print("Analysis completed. Level counts:", dict(counts))
print("Service counts:", dict(services))
