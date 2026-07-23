# Log Analyzer

A Python tool for analyzing log files, detecting IP addresses and errors, and exporting reports in TXT and JSON formats.

## Features

- Analyze log files.
- Count total log lines.
- Detect and count IP addresses.
- Detect and count error keywords.
- Generate a formatted report.
- Export reports to TXT.
- Export analysis data to JSON.

## Usage

1. Clone the repository:

```
git clone https://github.com/ali-ahmed-dev/log-analyzer.git
```
2. Navigate to the project directory:
```
cd log-analyzer
```

3. Run the program:
```
python log_analyzer.py
```
4. Enter the log file name when prompted.

## Technologies

- Python 3
- Regular Expressions (re)
- JSON
- datetime

  ## Requirements
- Python 3.x
- No external libraries needed (uses standard library only)

  ## Example
Enter the log file name: server.log

Total Lines: 150
Unique IPs: 12
Total Errors: 5
