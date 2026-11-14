
import os
import sys
import re
import subprocess
from flask import Flask, request, render_template_string

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

# Website design
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Log Analysis Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #101827;
            color: white;
        }

        header {
            background: #17243a;
            padding: 25px 7%;
            border-bottom: 1px solid #34435a;
        }

        header h1 {
            margin: 0;
            color: #60a5fa;
        }

        header p {
            color: #b7c5d9;
        }

        main {
            max-width: 1100px;
            margin: 35px auto;
            padding: 0 20px;
        }

        .search-box, .panel {
            background: #1b2940;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
        }

        input {
            padding: 12px;
            border-radius: 7px;
            border: 1px solid #50617a;
            background: #101827;
            color: white;
            margin: 8px 5px 8px 0;
            max-width: 100%;
        }

        button {
            padding: 12px 22px;
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 7px;
            cursor: pointer;
            font-weight: bold;
        }

        button:hover {
            background: #1d4ed8;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 18px;
            margin-bottom: 25px;
        }

        .card {
            background: #1b2940;
            padding: 25px;
            border-radius: 12px;
            border-left: 5px solid #60a5fa;
        }

        .card h3 {
            color: #b7c5d9;
            margin: 0;
        }

        .card h2 {
            font-size: 35px;
            margin: 15px 0 0;
        }

        .error { border-color: #ef4444; }
        .warning { border-color: #f59e0b; }
        .info { border-color: #22c55e; }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        th, td {
            text-align: left;
            padding: 13px;
            border-bottom: 1px solid #34435a;
            overflow-wrap: anywhere;
        }

        th {
            color: #60a5fa;
        }

        .message {
            background: #263750;
            padding: 12px;
            border-radius: 7px;
            margin: 10px 0;
            overflow-wrap: anywhere;
        }

        .empty {
            color: #aebdd1;
        }

        footer {
            text-align: center;
            padding: 25px;
            color: #aebdd1;
        }

        @media(max-width: 600px) {
            main { margin-top: 20px; }
            .search-box, .panel { padding: 16px; }
        }
    </style>
</head>

<body>

<header>
    <h1>Log Analysis Dashboard</h1>
    <p>Log File Search and Error Detection Using MapReduce</p>
</header>

<main>

    <section class="search-box">
        <h2>Analyze Log Files</h2>

        <form method="POST" enctype="multipart/form-data">

            <label>Search Keyword:</label><br>
            <input type="text" name="keyword"
                   placeholder="Example: payment"
                   value="{{ keyword }}">

            <br><br>

            <label>Upload a log file (.log or .txt):</label><br>
            <input type="file" name="logfile"
                   accept=".log,.txt">

            <br><br>

            <button type="submit">Analyze Logs</button>
        </form>

        <p class="empty">
            If you don't upload a file, the default sample.log is analyzed.
        </p>
    </section>

    {% if error_message %}
        <div class="panel">
            <h3>Unable to analyze the file</h3>
            <p>{{ error_message }}</p>
        </div>
    {% endif %}

    {% if result %}

    <div class="cards">

        <div class="card error">
            <h3>Total Errors</h3>
            <h2>{{ result.ERROR }}</h2>
        </div>

        <div class="card warning">
            <h3>Total Warnings</h3>
            <h2>{{ result.WARNING }}</h2>
        </div>

        <div class="card info">
            <h3>Total Info</h3>
            <h2>{{ result.INFO }}</h2>
        </div>

    </div>

    <section class="panel">
        <h2>Detected Error Messages</h2>

        {% if errors %}
            {% for item in errors %}
                <div class="message">🔴 {{ item }}</div>
            {% endfor %}
        {% else %}
            <p class="empty">No errors detected.</p>
        {% endif %}
    </section>

    <section class="panel">
        <h2>Keyword Search Results</h2>

        {% if matches %}
            {% for item in matches %}
                <div class="message">🔍 {{ item }}</div>
            {% endfor %}
        {% else %}
            <p class="empty">No matching records found.</p>
        {% endif %}
    </section>

    {% endif %}

</main>

<footer>
    Log Analysis Project | Python + Flask + MapReduce
</footer>

</body>
</html>
"""


def analyze_logs(log_text, keyword):

    mapper_path = os.path.join(BASE_DIR, "mapper.py")
    reducer_path = os.path.join(BASE_DIR, "reducer.py")

    if not os.path.exists(mapper_path):
        raise FileNotFoundError("mapper.py is missing.")

    if not os.path.exists(reducer_path):
        raise FileNotFoundError("reducer.py is missing.")

    # Run Mapper
    mapper = subprocess.run(
        [sys.executable, mapper_path, keyword],
        input=log_text,
        text=True,
        capture_output=True,
        cwd=BASE_DIR,
        check=True
    )

    # Run Reducer using Mapper output
    reducer = subprocess.run(
        [sys.executable, reducer_path],
        input=mapper.stdout,
        text=True,
        capture_output=True,
        cwd=BASE_DIR,
        check=True
    )

    # Extract counts from Reducer output
    counts = {
        "ERROR": 0,
        "WARNING": 0,
        "INFO": 0
    }

    for line in reducer.stdout.splitlines():
        match = re.match(
            r"^\s*(ERROR|WARNING|INFO)\s*:\s*(\d+)",
            line
        )

        if match:
            counts[match.group(1)] = int(match.group(2))

    # Extract error messages and keyword matches
    errors = []
    matches = []

    for line in mapper.stdout.splitlines():

        if line.startswith("ERROR_LINE\t"):
            errors.append(line.split("\t", 1)[1])

        elif line.startswith("SEARCH_LINE\t"):
            matches.append(line.split("\t", 1)[1])

    return counts, errors, matches


@app.route("/", methods=["GET", "POST"])
def home():

    keyword = "payment"
    result = None
    errors = []
    matches = []
    error_message = None

    try:

        if request.method == "POST":
            keyword = request.form.get("keyword", "").strip()

        uploaded_file = (
            request.files.get("logfile")
            if request.method == "POST"
            else None
        )

        if uploaded_file and uploaded_file.filename:

            filename = uploaded_file.filename.lower()

            if not filename.endswith((".log", ".txt")):
                raise ValueError("Please upload a .log or .txt file.")

            log_text = uploaded_file.read().decode(
                "utf-8-sig", errors="replace"
            )

        else:

            sample_path = os.path.join(BASE_DIR, "sample.log")

            with open(sample_path, "r", encoding="utf-8") as file:
                log_text = file.read()

        result, errors, matches = analyze_logs(
            log_text, keyword
        )

    except Exception as e:
        error_message = str(e)

    return render_template_string(
        HTML,
        keyword=keyword,
        result=result,
        errors=errors,
        matches=matches,
        error_message=error_message
    )


if __name__ == "__main__":
    app.run(debug=True)
