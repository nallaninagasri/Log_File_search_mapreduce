
import sys

# Read the search keyword
keyword = sys.argv[1].lower() if len(sys.argv) > 1 else ""

# Read log file line by line
for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    upper_line = line.upper()

    # Identify message type
    if "ERROR" in upper_line or "FAILED" in upper_line or "EXCEPTION" in upper_line:
        print("COUNT\tERROR\t1")
        print("ERROR_LINE\t" + line)

    elif "WARNING" in upper_line:
        print("COUNT\tWARNING\t1")

    elif "INFO" in upper_line:
        print("COUNT\tINFO\t1")

    # Search for the given keyword
    if keyword and keyword in line.lower():
        print("SEARCH_LINE\t" + line)
