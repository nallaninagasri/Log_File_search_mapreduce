
import sys

# Store the counts
counts = {
    "ERROR": 0,
    "WARNING": 0,
    "INFO": 0
}

error_lines = []
search_lines = []

# Read Mapper output
for line in sys.stdin:
    parts = line.rstrip("\n").split("\t", 2)

    if parts[0] == "COUNT":
        counts[parts[1]] += int(parts[2])

    elif parts[0] == "ERROR_LINE":
        error_lines.append(parts[1])

    elif parts[0] == "SEARCH_LINE":
        search_lines.append(parts[1])

# Display final results
print("\n========== LOG ANALYSIS REPORT ==========")

print("\nMessage Counts:")
for level, count in counts.items():
    print(level, ":", count)

print("\nTotal Errors:", counts["ERROR"])

print("\nDetected Error Messages:")
for error in error_lines:
    print("-", error)

print("\nKeyword Search Results:")
if search_lines:
    for result in search_lines:
        print("-", result)
else:
    print("No matching records found.")

print("\n========== ANALYSIS COMPLETED ==========")
