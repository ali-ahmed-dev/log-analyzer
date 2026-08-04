# Log Analyzer

A Python tool for analyzing log files, detecting IP addresses and error keywords, and generating professional reports in TXT and JSON formats.

---

## Features

- Analyze log files.
- Count total log lines.
- Detect and count IP addresses.
- Detect and count error keywords.
- Generate a formatted report.
- Export reports to TXT.
- Export analysis data to JSON.
- Memory-efficient processing: Handles large log files (>1GB) by storing only the last 100 lines in memory.
- Sorted Reports: IP addresses and error keywords are displayed in descending order of frequency (most frequent first).

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

Then enter the log file name when prompted.

---

## Project Structure

```text
log-analyzer/
│
├── log_analyzer.py
└── README.md
```

---

## Technologies

- Python 3
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

Status        : Completed Successfully
Total Lines   : 150
Unique IPs    : 12
Total Errors  : 5
```

---

## Current Version

**v1.1.0**

---

## Author

**Ali Ahmed**