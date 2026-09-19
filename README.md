# Log Analyzer

![Python Version](https://img.shields.io/badge/python-3.x-blue?logo=python)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/badge/tests-32%20passed-brightgreen)
![CI](https://github.com/ali-ahmed-dev/log-analyzer/actions/workflows/test.yml/badge.svg)
![Version](https://img.shields.io/badge/version-1.6.0-orange)
[![GitHub stars](https://img.shields.io/github/stars/ali-ahmed-dev/log-analyzer?style=social)](https://github.com/ali-ahmed-dev/log-analyzer/stargazers)

A lightweight Python tool for analyzing log files, detecting IP addresses and error keywords, and generating structured reports in **TXT** and **JSON** formats.

Built with Python's standard library, with a focus on **performance, reliability, maintainability, and security-oriented log analysis**.

---

## Features

* Analyze single log files or scan directories recursively for `.log` and `.txt` files
* **Automatic detection of Apache/Nginx Combined Log Format**
* **Extract HTTP status codes (200, 404, 500, ...) from Apache logs**
* **Extract HTTP methods (GET, POST, PUT, DELETE, ...) from Apache logs**
* Count total log lines
* Detect and count IP addresses
* Detect and count common error keywords
* Sort IP addresses and errors by frequency
* Keep only the last 100 log lines in memory for preview
* Generate formatted TXT reports
* Export structured JSON analysis reports
* Continue processing when an individual file cannot be analyzed
* Command-line interface (CLI) powered by `argparse`
* Support TXT, JSON, or both output formats
* Configurable output directory
* Verbose and quiet execution modes
* Version flag (`--version`)
* Uses only Python's standard library

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/ali-ahmed-dev/log-analyzer.git
cd log-analyzer
```

No external Python packages are required.

---

## Testing

The project includes a test suite using `pytest`.

### Install pytest

```bash
pip install pytest
```

### Run Tests

```bash
pytest tests/ -v
```

### Test Coverage

Currently, **32 tests** cover the core functionality:

| Test Area                      | Status |
| ------------------------------ | ------ |
| IP address detection           | ✅      |
| Error keyword detection        | ✅      |
| File analysis                  | ✅      |
| Directory scanning             | ✅      |
| TXT report generation          | ✅      |
| JSON report generation         | ✅      |
| **Apache log parsing**         | ✅      |
| **HTTP status code detection** | ✅      |
| **HTTP method detection**      | ✅      |
| Edge cases                     | ✅      |

All tests pass successfully.

---

## Usage

The tool accepts either a single log file or a directory containing log files.

### Analyze a Single File

```bash
python log_analyzer.py /path/to/logfile.log
```

### Analyze a Directory

```bash
python log_analyzer.py /path/to/logs/
```

By default, reports are generated in the current working directory.

---

## Command-Line Options

| Option            | Description                                                        |
| ----------------- | ------------------------------------------------------------------ |
| `-f`, `--format`  | Output format: `txt`, `json`, or `both`. Default: `both`.          |
| `-o`, `--output`  | Directory where reports will be saved. Default: current directory. |
| `-v`, `--verbose` | Display detailed analysis progress.                                |
| `-q`, `--quiet`   | Minimize console output.                                           |
| `--version`       | Display the current version and exit.                              |
| `-h`, `--help`    | Display the help message and exit.                                 |

### Output Formats

#### TXT

```bash
python log_analyzer.py server.log --format txt
```

Generates a human-readable formatted report.

#### JSON

```bash
python log_analyzer.py server.log --format json
```

Generates structured analysis data.

#### Both

```bash
python log_analyzer.py server.log --format both
```

Generates both TXT and JSON reports.

---

## Examples

### Analyze a Single Log File

```bash
python log_analyzer.py /var/log/syslog
```

### Analyze an Apache Access Log

```bash
python log_analyzer.py /var/log/apache2/access.log
```

The analyzer automatically detects Apache format and extracts HTTP status codes and methods.

### Analyze a Directory and Export JSON Reports

```bash
python log_analyzer.py /var/log/ --format json --output ./reports
```

### Analyze a Directory with Verbose Output

```bash
python log_analyzer.py /var/log/ --verbose
```

### Analyze a File with Quiet Mode

```bash
python log_analyzer.py /path/to/file.log --quiet
```

### Display Help

```bash
python log_analyzer.py --help
```

### Display Version

```bash
python log_analyzer.py --version
```

---

## How It Works

The analyzer processes each file sequentially:

```text
Input File / Directory
        |
        v
   File Discovery
        |
        v
     Log Reading
        |
        +-- Line Count
        +-- IP Detection
        +-- Error Detection
        +-- Apache Format Detection
        |     |
        |     +-- HTTP Status Codes
        |     +-- HTTP Methods
        |
        v
   Result Aggregation
        |
        v
   Report Generation
        |
        +-- TXT
        +-- JSON
```

For directories, the tool searches recursively for supported log files.

---

## Memory Efficiency

Log Analyzer processes files **line by line** and stores only the last **100 lines** for the report preview.

This allows large log files to be analyzed without loading the entire file into memory.

```text
Large Log File
      |
      v
 Read line by line
      |
      +-- Count lines
      +-- Detect IPs
      +-- Detect errors
      +-- Detect HTTP status
      |
      v
 Keep only last 100 lines
```

---

## Detection

### IP Addresses

The analyzer detects IPv4 addresses using a regular expression and counts their occurrences.

Example:

```text
192.168.1.100 -> 45
10.0.0.5 -> 12
172.16.0.10 -> 7
```

### Error Keywords

The analyzer detects common error-related keywords:

```text
ERROR
EXCEPTION
CRITICAL
WARNING
FAILED
FATAL
SEVERE
PANIC
```

Results are sorted by frequency.

Example:

```text
ERROR -> 8
WARNING -> 3
CRITICAL -> 1
```

---

## Log Formats

### Apache/Nginx Combined Log Format

The analyzer automatically detects and parses the Apache/Nginx Combined Log Format.

**Example line:**

```text
192.168.1.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326
```

**Fields extracted:**

| Field       | Description                         | Example           |
| ----------- | ----------------------------------- | ----------------- |
| `ip`        | Client IP address                   | `192.168.1.1`     |
| `timestamp` | Request date and time               | `10/Oct/2023:...` |
| `method`    | HTTP method                         | `GET`             |
| `path`      | Requested resource                  | `/index.html`     |
| `status`    | HTTP status code                    | `200`             |
| `size`      | Response size in bytes (`-` = none) | `2326`            |

**Security-relevant status codes:**

| Code | Meaning               | Why It Matters                    |
| ---- | --------------------- | --------------------------------- |
| 200  | OK                    | Normal traffic                    |
| 401  | Unauthorized          | ⚠️ Failed authentication attempts |
| 403  | Forbidden             | ⚠️ Blocked access attempts        |
| 404  | Not Found             | ⚠️ Path scanning / enumeration    |
| 500  | Internal Server Error | 🔴 Potential exploitation         |
| 503  | Service Unavailable   | 🔴 Potential DDoS                 |

**Supported HTTP methods:**

`GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `HEAD`, `OPTIONS`

### Generic Logs

For non-Apache logs, the analyzer falls back to generic mode:

* IP address detection (via regex)
* Error keyword detection (via regex)

This ensures compatibility with any log format.

---

## Report Output

### TXT Report

Example:

```text
==================================================
                 LOG ANALYZER
==================================================
File          : /var/log/syslog
Status        : Completed Successfully
Total Lines   : 1523
Analysis Date : 2026-08-15 14:35:12

--------------------------------------------------
                LOG CONTENT
--------------------------------------------------
[last 100 lines of the log file...]

--------------------------------------------------
          IP ADDRESSES OCCURRENCES
--------------------------------------------------
192.168.1.100 -> 45
10.0.0.5 -> 12

--------------------------------------------------
            ERRORS OCCURRENCES
--------------------------------------------------
ERROR -> 8
WARNING -> 3

--------------------------------------------------
           HTTP STATUS CODES
--------------------------------------------------
200 -> 1245
401 -> 15
404 -> 8

--------------------------------------------------
            HTTP METHODS
--------------------------------------------------
GET -> 1200
POST -> 45
DELETE -> 2

--------------------------------------------------
              SUMMARY REPORT
--------------------------------------------------
Total Lines   : 1523
Total IPs     : 67
Unique IPs    : 18
Total Errors  : 11
Unique Errors : 3
Total HTTP    : 1268
Unique HTTP   : 3

==================================================
                END OF REPORT
==================================================
```

### JSON Report

Example structure:

```json
{
    "file": "/var/log/syslog",
    "analysis_date": "2026-08-15 14:35:12",
    "total_lines": 1523,
    "ip_addresses": {
        "192.168.1.100": 45,
        "10.0.0.5": 12
    },
    "errors": {
        "ERROR": 8,
        "WARNING": 3
    },
    "http_status_codes": {
        "200": 1245,
        "401": 15,
        "404": 8
    },
    "http_methods": {
        "GET": 1200,
        "POST": 45,
        "DELETE": 2
    },
    "log_content": [
        "..."
    ]
}
```

---

## Project Structure

```text
log-analyzer/
|
+-- log_analyzer.py
+-- parsers.py
+-- README.md
+-- LICENSE
+-- .gitignore
+-- tests/
|   +-- __init__.py
|   +-- conftest.py
|   +-- test_analyzer.py
|   +-- test_parsers.py
+-- pytest.ini
```

---

## Technologies

* **Python 3** — Core language
* **argparse** — Command-line interface
* **pathlib** — File and directory handling
* **collections.Counter** — Frequency counting
* **re** — Regular expression-based detection
* **json** — Structured report generation
* **datetime** — Report timestamps
* **pytest** — Testing framework

---

## Requirements

* Python 3.x
* No external dependencies
* Python Standard Library only

---

## Current Version

**v1.6.0**

---

## Development History

The project started as a simple Python log-analysis script and evolved through multiple iterations.

Major improvements include:

* IP address detection
* Error keyword detection
* Frequency-based result sorting
* Memory-efficient log processing
* Recursive directory scanning
* TXT report generation
* JSON report generation
* Improved exception handling
* Type hints and documentation
* Command-line interface
* Version flag
* Comprehensive test suite
* **Apache/Nginx Combined Log Format support**
* **HTTP status code detection**
* **HTTP method detection**

---

## Roadmap

### Short-term

* [x] Add support for Apache log format
* [ ] Add support for Nginx log format
* [ ] Add HTML report generation
* [ ] Support compressed log files (`.gz`, `.zip`)
* [ ] Configurable log parsing rules

### Long-term

* Security-oriented detection rules
* Brute-force attack detection
* Threat intelligence integration
* SQLite database storage
* Web-based dashboard
* Network-based log collection
* API integration
* Containerized deployment with Docker
* Advanced anomaly detection

---

## Security

Log Analyzer is designed as a **log analysis and security-oriented development project**.

Log files may contain sensitive information such as:

* IP addresses
* Usernames
* URLs
* Authentication events
* Server information

Always ensure that you have permission to analyze the logs you process and avoid sharing sensitive log data publicly.

---

## Contributing

Contributions, issues, and feature requests are welcome.

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

Please update tests when appropriate.

---

## License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

## Author

**Ali Ahmed**

* GitHub: [ali-ahmed-dev](https://github.com/ali-ahmed-dev)
* Project: [Log Analyzer](https://github.com/ali-ahmed-dev/log-analyzer)

---

## Support

If you find this tool useful, consider giving it a ⭐ on GitHub.

[![GitHub stars](https://img.shields.io/github/stars/ali-ahmed-dev/log-analyzer?style=social)](https://github.com/ali-ahmed-dev/log-analyzer/stargazers)
