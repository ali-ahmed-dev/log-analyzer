# Log Analyzer

A Python tool for analyzing log files, detecting IP addresses and error keywords, and generating professional reports in TXT and JSON formats.

---

## Features

- Analyze log files.
- Count total log lines.
- Detect and count IP addresses.
- Detect and count error keywords.
- Generate a formatted report.
- Export reports in TXT format.
- Export analysis data in JSON format.
- Memory-efficient processing: Handles large log files (>1GB) by storing only the last 100 lines in memory.
- Sorted Reports: IP addresses and error keywords are displayed in descending order of frequency (most frequent first).
- **Recursive directory scanning**: Analyze all log files within a folder and its subfolders.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/ali-ahmed-dev/log-analyzer.git
```

Navigate to the project directory:

```bash
cd log-analyzer
```

---

## Usage

Run the program:

```bash
python log_analyzer.py
```

Then enter the path to a log file or a directory containing log files (`.log` or `.txt`).

---

## Project Structure

```text
log-analyzer/
│
├── log_analyzer.py
├── README.md
├── LICENSE
└── .gitignore
```

---

## Technologies

- Python 3
- pathlib
- collections (Counter)
- Regular Expressions (`re`)
- JSON
- datetime

---

## Requirements

- Python 3.x
- No external libraries required (uses Python Standard Library only).

---

## Example

```text
Welcome to the Log Analyzer Tool

Enter the log file name:
server.log

==================================================
                 LOG ANALYZER
==================================================
Status        : Completed Successfully
Total Lines   : 150
Unique IPs    : 12
Total Errors  : 5
```

### Example with a Directory

```text
Welcome to the Log Analyzer Tool

Enter the log file or directory path: /var/log

--- Analyzing: /var/log/syslog ---
==================================================
                 LOG ANALYZER
==================================================
Status        : Completed Successfully
Total Lines   : 1523
Unique IPs    : 45
Total Errors  : 12

--- Analyzing: /var/log/auth.log ---
==================================================
                 LOG ANALYZER
==================================================
Status        : Completed Successfully
Total Lines   : 342
Unique IPs    : 18
Total Errors  : 5
```

---

## License

This project is licensed under the MIT License.

---

## Version

**v1.3.0**

---

## Author

**Ali Ahmed**