import re
from datetime import datetime
import json
from pathlib import Path

IP_PATTERN = r"\b(?:(?:25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})\.){3}(?:25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})\b"
ERROR_PATTERN = r"\b(ERROR|EXCEPTION|CRITICAL|WARNING|FAILED|FATAL|SEVERE|PANIC)\b"

HEADER = "=" * 50 + "\n                 LOG ANALYZER\n" + "=" * 50
FOOTER = "=" * 50 + "\n                END OF REPORT\n" + "=" * 50


LOG_CONTENT_HEADER = (
    "-" * 50 +
    "\n                LOG CONTENT\n" +
    "-" * 50
)

IP_HEADER = (
    "-" * 50 +
    "\n          IP ADDRESSES OCCURRENCES\n" +
    "-" * 50
)

NO_IP_HEADER = (
    "-" * 50 +
    "\n           NO IP ADDRESSES FOUND\n" +
    "-" * 50
)

ERROR_HEADER = (
    "-" * 50 +
    "\n            ERRORS OCCURRENCES\n" +
    "-" * 50
)

NO_ERROR_HEADER = (
    "-" * 50 +
    "\n              NO ERRORS FOUND\n" +
    "-" * 50
)

SUMMARY_HEADER = (
    "-" * 50 +
    "\n              SUMMARY REPORT\n" +
    "-" * 50
)



def get_log_files(path):
    """Return a list of all log files (by extension) in a directory and its subdirectories."""
    log_extensions = {'.log', '.txt'}
    path_obj = Path(path)
    files = []

    if path_obj.is_file():
        return [path_obj]
    elif path_obj.is_dir():
        for file in path_obj.rglob('*'):
            if file.is_file() and file.suffix.lower() in log_extensions:
                files.append(file)
        return files
    else:
        raise ValueError(f"Path '{path}' is not a valid file or directory.")


def analyze_log(filename):
    line_count = 0
    ip_count = {}
    error_count = {}
    log_preview = []
    max_preview_lines = 100

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line_count += 1
            if len(log_preview) >= max_preview_lines:
                log_preview.pop(0)
            log_preview.append(line.strip())
            for ip in re.findall(IP_PATTERN, line):
                ip_count[ip] = ip_count.get(ip, 0) + 1

            for error in re.findall(ERROR_PATTERN, line, re.IGNORECASE):
                error = error.upper()
                error_count[error] = error_count.get(error, 0) + 1

    return line_count, ip_count, error_count, log_preview


def generate_report(filename, line_count, ip_count, error_count, log_preview, analysis_time):

    report = []

    report.append(HEADER)
    report.append(f"""File          : {filename}
Status        : Completed Successfully
Total Lines   : {line_count}
Analysis Date : {analysis_time}
""")

    report.append(LOG_CONTENT_HEADER)
    for line in log_preview:
        report.append(line)

    if ip_count:
        report.append(IP_HEADER)
        for ip, count in sorted(ip_count.items(), key=lambda x: x[1], reverse=True):
            report.append(f"{ip} → {count}")
    else:
        report.append(NO_IP_HEADER)
        report.append("No IP addresses found in the log file.")

    if error_count:
        report.append(ERROR_HEADER)
        for error, count in sorted(error_count.items(), key=lambda x: x[1], reverse=True):
            report.append(f"{error} → {count}")
    else:
        report.append(NO_ERROR_HEADER)
        report.append("No errors found in the log file.")

    report.append(SUMMARY_HEADER)
    report.append(f"Total Lines   : {line_count}")
    report.append(f"Total IPs     : {sum(ip_count.values())}")
    report.append(f"Unique IPs    : {len(ip_count)}")
    report.append(f"Total Errors  : {sum(error_count.values())}")
    report.append(f"Unique Errors : {len(error_count)}")

    report.append(FOOTER)

    return "\n".join(report)


def export_to_json(filename, line_count, ip_count, error_count, log_preview, analysis_time):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f"report_{timestamp}.json"
    report_data = {
        "file": filename,
        "analysis_date": analysis_time,
        "total_lines": line_count,
        "ip_addresses": ip_count,
        "errors": error_count,
        "log_content": log_preview
    }

    with open(json_filename, "w", encoding="utf-8") as file:
        json.dump(report_data, file, indent=4, ensure_ascii=False)
    print(f"Report exported to {json_filename}")


def export_to_txt(report_text):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_filename = f"report_{timestamp}.txt"
    with open(txt_filename, "w", encoding="utf-8") as file:
        file.write(report_text)
    print(f"Report exported to {txt_filename}")


def main():
    print("Welcome to the Log Analyzer Tool")
    try:
        user_input = input("Enter the log file or directory path: ").strip()
        if not user_input:
            print("Error: No path provided.")
            return

        try:
            log_files = get_log_files(user_input)
        except ValueError as ve:
            print(f"Error: {ve}")
            return

        if not log_files:
            print(f"No log files found in the specified path: '{user_input}'")
            return

        for file_path in log_files:
            print(f"\n--- Analyzing: {file_path} ---")
            filename = str(file_path)
            analysis_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            line_count, ip_count, error_count, log_preview = analyze_log(filename)

            report_text = generate_report(
                filename,
                line_count,
                ip_count,
                error_count,
                log_preview,
                analysis_time
            )

            print(report_text)
            export_to_txt(report_text)
            export_to_json(
                filename,
                line_count,
                ip_count,
                error_count,
                log_preview,
                analysis_time
            )

    except PermissionError:
        print(f"Error: Permission denied. You do not have read access to '{user_input}'.")
        return

    except UnicodeDecodeError:
        print(f"Error: The file '{user_input}' is not a valid UTF-8 text file. Please check its encoding.")
        return

    except OSError as e:
        print(f"Error: An operating system error occurred. Details: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
