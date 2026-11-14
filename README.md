
# Log File Search and Error Detection Using MapReduce

## 1. Introduction
This project is used to search log files and detect errors using the MapReduce programming model.

Log files contain information about server activities, warnings and errors. This project analyzes those records and generates a summary.

## 2. Objectives
- To read and analyze log files.
- To identify ERROR, WARNING and INFO messages.
- To search for specific keywords.
- To count the total number of errors.
- To generate an error analysis report.

## 3. Technologies Used
- Python
- MapReduce
- Visual Studio Code
- GitHub

## 4. Project Modules

### Mapper
Reads log records and identifies different message types.

### Reducer
Combines the Mapper results and calculates the total counts.

### Sample Log
Contains sample server log information for testing.

## 5. Features
- Log file reading
- Error detection
- Warning identification
- Keyword searching
- Error counting
- Report generation

## 6. How to Run the Project

Open the terminal in the project folder.

Run:

Get-Content sample.log | py mapper.py payment | py reducer.py

Replace payment with any keyword you want to search.

## 7. Expected Results
The project displays:
- Total ERROR messages
- Total WARNING messages
- Total INFO messages
- Detected error messages
- Keyword search results

## 8. Conclusion
This project demonstrates the use of the MapReduce programming model for log file analysis and error detection. It helps identify problems in server log records in a simple and efficient way.
