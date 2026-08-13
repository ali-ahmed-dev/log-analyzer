import re
import json
from pathlib import Path
from datetime import datetime
from collections import Counter


# ===================== CONSTANTS =====================
SEPARATOR = "=" * 50
DASH_SEPARATOR = "-" * 50


HEADER = SEPARATOR + "\n                 LOG ANALYZER\n" + SEPARATOR
FOOTER = SEPARATOR + "\n                END OF REPORT\n" + SEPARATOR


SECTION_HEADERS = {
    "log_content": f"{DASH_SEPARATOR}\n                LOG CONTENT\n{DASH_SEPARATOR}",
    "ip": f"{DASH_SEPARATOR}\n          IP ADDRESSES OCCURRENCES\n{DASH_SEPARATOR}",
    "no_ip": f"{DASH_SEPARATOR}\n           NO IP ADDRESSES FOUND\n{DASH_SEPARATOR}",
    "errors": f"{DASH_SEPARATOR}\n            ERRORS OCCURRENCES\n{DASH_SEPARATOR}",
    "no_errors": f"{DASH_SEPARATOR}\n              NO ERRORS FOUND\n{DASH_SEPARATOR}",
    "summary": f"{DASH_SEPARATOR}\n              SUMMARY REPORT\n{DASH_SEPARATOR}",
}

IP_PATTERN = r"\b(?:(?:25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})\.){3}(?:25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})\b"
ERROR_PATTERN = r"\b(ERROR|EXCEPTION|CRITICAL|WARNING|FAILED|FATAL|SEVERE|PANIC)\b"


LOG_EXTENSIONS = {'.log', '.txt'}
MAX_PREVIEW_LINES = 100


# ===================== FILE DISCOVERY =====================
def get_log_files(path: Path) -> list[Path]:
    """
    Return a list of all log files in a directory (recursively) or a single file.

    Args:
        path (Path): File or directory path.

    Returns:
        list[Path]: List of log file paths.

    Raises:
        ValueError: If the path is not a valid file or directory.
    """
    if path.is_file():
        return [path]

    if not path.is_dir():
        raise ValueError(f"Path '{path}' is not a valid file or directory.")

    return [
        file for file in path.rglob('*')
        if file.is_file() and file.suffix.lower() in LOG_EXTENSIONS
    ]


# ===================== CORE ANALYSIS =====================
def analyze_log(filename: Path) -> tuple[int, Counter, Counter, list[str]]:
    """
    Analyze a log file and extract statistics.

    Args:
        filename (Path): Path to the log file.

    Returns:
        tuple[int, Counter, Counter, list[str]]:
            - Total line count
            - IP address counter
            - Error keyword counter
            - Preview of the last MAX_PREVIEW_LINES lines
    """
    line_count = 0
    ip_count = Counter()
    error_count = Counter()
    log_preview = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line_count += 1

            if len(log_preview) >= MAX_PREVIEW_LINES:
                log_preview.pop(0)
            log_preview.append(line.strip())

            ip_count.update(re.findall(IP_PATTERN, line))

            for error in re.findall(ERROR_PATTERN, line, re.IGNORECASE):
                error_count[error.upper()] += 1

    return line_count, ip_count, error_count, log_preview


# ===================== REPORT GENERATION =====================
def generate_report(
    filename: Path,
    line_count: int,
    ip_count: Counter,
    error_count: Counter,
    log_preview: list[str],
    analysis_time: str
) -> str:
    """
    Generate a formatted report from log analysis results.

    Args:
        filename (Path): Name of the analyzed log file.
        line_count (int): Total number of lines in the file.
        ip_count (Counter): Counter of IP addresses.
        error_count (Counter): Counter of error keywords.
        log_preview (list[str]): Preview of the last MAX_PREVIEW_LINES lines.
        analysis_time (str): Timestamp of the analysis.

    Returns:
        str: Formatted report as a single string.
    """
    report = [
        HEADER,
        f"File          : {filename}",
        f"Status        : Completed Successfully",
        f"Total Lines   : {line_count}",
        f"Analysis Date : {analysis_time}",
        "",
        SECTION_HEADERS["log_content"],
        *log_preview,
    ]

    # IP Addresses Section
    report.append(SECTION_HEADERS["ip"] if ip_count else SECTION_HEADERS["no_ip"])
    if ip_count:
        report.extend(f"{ip} → {count}" for ip, count in ip_count.most_common())
    else:
        report.append("No IP addresses found in the log file.")

    # Errors Section
    report.append(SECTION_HEADERS["errors"] if error_count else SECTION_HEADERS["no_errors"])
    if error_count:
        report.extend(f"{error} → {count}" for error, count in error_count.most_common())
    else:
        report.append("No errors found in the log file.")

    # Summary Section
    report.extend([
        SECTION_HEADERS["summary"],
        f"Total Lines   : {line_count}",
        f"Total IPs     : {sum(ip_count.values())}",
        f"Unique IPs    : {len(ip_count)}",
        f"Total Errors  : {sum(error_count.values())}",
        f"Unique Errors : {len(error_count)}",
        FOOTER,
    ])

    return "\n".join(report)


# ===================== EXPORT FUNCTIONS =====================
def export_to_json(
    filename: Path,
    line_count: int,
    ip_count: Counter,
    error_count: Counter,
    log_preview: list[str],
    analysis_time: str
) -> None:
    """
    Export analysis results to a JSON file with a timestamp.

    Args:
        filename (Path): Name of the analyzed log file.
        line_count (int): Total number of lines.
        ip_count (Counter): Counter of IP addresses.
        error_count (Counter): Counter of error keywords.
        log_preview (list[str]): Preview of log lines.
        analysis_time (str): Timestamp of the analysis.

    Returns:
        None
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f"report_{timestamp}.json"

    report_data = {
        "file": str(filename),
        "analysis_date": analysis_time,
        "total_lines": line_count,
        "ip_addresses": dict(ip_count),
        "errors": dict(error_count),
        "log_content": log_preview,
    }

    Path(json_filename).write_text(
        json.dumps(report_data, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"Report exported to {json_filename}")

# ===================== EXPORT FUNCTIONS =====================
def export_to_txt(report_text: str) -> None:
    """
    Export the report text to a timestamped TXT file.

    Args:
        report_text (str): The formatted report text to export.

    Returns:
        None
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_filename = f"report_{timestamp}.txt"

    Path(txt_filename).write_text(report_text, encoding="utf-8")
    print(f"Report exported to {txt_filename}")


# ===================== MAIN =====================
def main() -> None:
    """
    Main entry point for the Log Analyzer tool.

    Orchestrates the entire workflow:
    1. Get user input (file or directory path).
    2. Discover log files.
    3. Analyze each file.
    4. Generate and export reports.
    """
    print("Welcome to the Log Analyzer Tool")

    user_input = input("Enter the log file or directory path: ").strip()
    if not user_input:
        print("Error: No path provided.")
        return

    try:
        log_files = get_log_files(Path(user_input))
    except ValueError as ve:
        print(f"Error: {ve}")
        return

    if not log_files:
        print(f"No log files found in the specified path: '{user_input}'")
        return

    for file_path in log_files:
        print(f"\n--- Analyzing: {file_path} ---")
        analysis_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            line_count, ip_count, error_count, log_preview = analyze_log(file_path)
        except (PermissionError, UnicodeDecodeError, OSError) as e:
            print(f"Error analyzing {file_path}: {e}")
            continue
        except Exception as e:
            print(f"Unexpected error analyzing {file_path}: {e}")
            continue

        report_text = generate_report(
            file_path,
            line_count,
            ip_count,
            error_count,
            log_preview,
            analysis_time
        )

        print(report_text)
        export_to_txt(report_text)
        export_to_json(
            file_path,
            line_count,
            ip_count,
            error_count,
            log_preview,
            analysis_time
        )


if __name__ == "__main__":
    main()
