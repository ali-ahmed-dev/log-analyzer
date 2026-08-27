# Log Analyzer

A lightweight Python tool for analyzing log files, detecting IP addresses and error keywords, and generating structured reports in **TXT** and **JSON** formats.

Built with Python's standard library, with a focus on **performance, reliability, maintainability, and security-oriented log analysis**.

---

## Features

- Analyze single log files or scan directories recursively for `.log` and `.txt` files (with option to disable recursion).
- Count total log lines.
- Detect and count IP addresses.
- Detect and count common error keywords.
- Sort IP addresses and errors by frequency.
- Keep only the last 100 log lines in memory for preview.
- Generate formatted TXT reports.
- Export structured JSON analysis reports.
- Continue processing when an individual file cannot be analyzed.
- Command-line interface (CLI) powered by `argparse`.
- Support multiple output formats: TXT, JSON, or both.
- Configurable output directory.
- Verbose and quiet execution modes.
- **Version flag** (`--version`) to display the current tool version.
- Uses only Python's standard library.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ali-ahmed-dev/log-analyzer.git
````

### 2. Navigate to the project directory

```bash
cd log-analyzer
```

No external Python packages are required.

---

## Usage

The tool accepts either a **single log file** or a **directory containing log files**.

### Analyze a single file

```bash
python log_analyzer.py /path/to/logfile.log
```

### Analyze a directory

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

---

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

Generates structured analysis data suitable for further processing.

#### Both

```bash
python log_analyzer.py server.log --format both
```

Generates both TXT and JSON reports.

---

## Examples

### Analyze a single log file

```bash
python log_analyzer.py /var/log/syslog
```

### Analyze a directory and export JSON reports

```bash
python log_analyzer.py /var/log/ --format json --output ./reports
```

### Analyze a directory with verbose output

```bash
python log_analyzer.py /var/log/ --verbose
```

### Analyze a file with quiet mode

```bash
python log_analyzer.py /path/to/file.log --quiet
```

### Display available options

```bash
python log_analyzer.py --help
```

### Display version

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

Large log files can consume significant amounts of memory if their entire contents are loaded at once.

Log Analyzer processes files **line by line** and stores only the last **100 lines** for the report preview.

This allows the analyzer to process large files without keeping the entire file in memory.

```text
Large Log File
      |
      v
 Read line by line
      |
      +-- Count lines
      +-- Detect IPs
      +-- Detect errors
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

The analyzer detects common error-related keywords such as:

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
              SUMMARY REPORT
--------------------------------------------------
Total Lines   : 1523
Total IPs     : 67
Unique IPs    : 18
Total Errors  : 11
Unique Errors : 3

==================================================
                END OF REPORT
==================================================
```

### JSON Report

The JSON report contains structured information that can be consumed by other programs or future automation workflows.

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
+-- README.md
+-- LICENSE
+-- .gitignore
```

---

## Technologies

* **Python 3**
* **argparse** - command-line interface
* **pathlib** - file and directory handling
* **collections.Counter** - efficient frequency counting
* **re** - regular expression-based detection
* **json** - structured report generation
* **datetime** - timestamps for reports

---

## Requirements

* Python 3.x
* No external dependencies
* Uses Python Standard Library only

---

## Current Version

**v1.5.0**

---

## Development History

The project started as a simple Python log-analysis script and has gradually evolved through multiple iterations.

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
* Unified code structure and `--version` flag

The project is continuously evolving alongside the author's development in **Python, algorithms, web development, Linux, networking, and cybersecurity**.

---

## Future Development

The project will evolve gradually as new requirements, ideas, and skills emerge.

Potential future improvements include:

* Advanced CLI capabilities
* Configurable log parsing
* Support for Apache and Nginx log formats
* Compressed log file support
* Performance optimizations
* HTML report generation
* SQLite integration
* Security-oriented detection rules
* Brute-force detection
* Threat intelligence integration
* Anomaly detection
* Network-based log collection
* API integration
* Containerized deployment
* Advanced security monitoring

> These are long-term ideas rather than a fixed roadmap. Features will be added progressively as the project matures.

---

## Security

Log Analyzer is designed primarily as a **log analysis and security-oriented development project**.

Log files may contain sensitive information such as:

* IP addresses
* Usernames
* URLs
* Authentication events
* Server information

Always ensure that you have permission to analyze the logs you process and avoid sharing sensitive log data publicly.

---

## License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

## Author

**Ali Ahmed**

GitHub:
https://github.com/ali-ahmed-dev