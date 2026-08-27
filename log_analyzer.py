import re
import json
import argparse
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

LOG_EXTENSIONS = {".log", ".txt"}
MAX_PREVIEW_LINES = 100


# ===================== FILE DISCOVERY =====================
def get_log_files(path: Path, recursive: bool = True) -> list[Path]:
    """
    Return a list of all log files in a directory or a single file.

    Args:
        path (Path): File or directory path.
        recursive (bool): Whether to search subdirectories.

    Returns:
        list[Path]: List of log file paths.

    Raises:
        ValueError: If the path is not a valid file or directory.
    """
    if path.is_file():
        return [path]

    if not path.is_dir():
        raise ValueError(f"Path '{path}' is not a valid file or directory.")

    if recursive:
        return [
            file for file in path.rglob("*")
            if file.is_file() and file.suffix.lower() in LOG_EXTENSIONS
        ]
    else:
        return [
            file for file in path.glob("*")
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
def export_to_txt(report_text: str, output_dir: Path, quiet: bool = False) -> None:
    """Export the report to a timestamped TXT file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_filename = f"report_{timestamp}.txt"
    report_path = output_dir / txt_filename

    try:
        report_path.write_text(report_text, encoding="utf-8")
        if not quiet:
            print(f"TXT report exported to {report_path}")
    except (PermissionError, OSError) as e:
        print(f"Error: Could not write TXT report to {report_path}. {e}")


def export_to_json(
    filename: Path,
    line_count: int,
    ip_count: Counter,
    error_count: Counter,
    log_preview: list[str],
    analysis_time: str,
    output_dir: Path,
    quiet: bool = False
) -> None:
    """Export analysis results to a JSON file with a timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f"report_{timestamp}.json"
    report_path = output_dir / json_filename

    report_data = {
        "file": str(filename),
        "analysis_date": analysis_time,
        "total_lines": line_count,
        "ip_addresses": dict(ip_count),
        "errors": dict(error_count),
        "log_content": log_preview,
    }

    try:
        report_path.write_text(
            json.dumps(report_data, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )
        if not quiet:
            print(f"JSON report exported to {report_path}")
    except (PermissionError, OSError) as e:
        print(f"Error: Could not write JSON report to {report_path}. {e}")


# ===================== ARGUMENT PARSER =====================
def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the CLI argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Analyze log files, detect IPs and errors, and generate reports.",
        epilog="""
Examples:
  %(prog)s /var/log/syslog
  %(prog)s /var/log/ -f json -o ./reports
  %(prog)s /var/log/ --format both --verbose
  %(prog)s /path/to/file.log --quiet
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "path",
        help="Path to a log file or a directory containing log files (.log, .txt)"
    )

    parser.add_argument(
        "-f", "--format",
        choices=["txt", "json", "both"],
        default="both",
        help="Output format: txt, json, or both (default: both)"
    )

    parser.add_argument(
        "-o", "--output",
        help="Directory to save reports (default: current directory)"
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Search subdirectories recursively (enabled by default)"
    )

    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Disable recursive directory scanning (only top-level directory)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Print detailed progress during analysis"
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress all output except errors and report generation messages"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="Log Analyzer v1.5.0"
    )

    return parser


# ===================== MAIN =====================
def main(argv: list[str] | None = None) -> int:
    """
    Main entry point for the Log Analyzer CLI.
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    # ---------- Validate input path ----------
    input_path = Path(args.path)
    if not input_path.exists():
        print(f"Error: Path '{args.path}' does not exist.")
        return 1

    # ---------- Determine recursive behavior ----------
    recursive = not args.no_recursive

    # ---------- Determine output directory ----------
    output_dir = Path(args.output) if args.output else Path.cwd()
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except (PermissionError, OSError) as e:
        print(f"Error: Could not create output directory '{output_dir}'. {e}")
        return 1

    # ---------- Get log files ----------
    try:
        log_files = get_log_files(input_path, recursive)
    except ValueError as ve:
        print(f"Error: {ve}")
        return 1

    if not log_files:
        print(f"No log files found in: '{args.path}'")
        return 1

    # ---------- Process each file ----------
    for file_path in log_files:
        if not args.quiet and args.verbose:
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

        # ---------- Export reports ----------
        if args.format in ("txt", "both"):
            export_to_txt(report_text, output_dir, quiet=args.quiet)
        if args.format in ("json", "both"):
            export_to_json(
                file_path,
                line_count,
                ip_count,
                error_count,
                log_preview,
                analysis_time,
                output_dir,
                quiet=args.quiet
            )

    if not args.quiet:
        print(f"\nAll reports saved to: {output_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())