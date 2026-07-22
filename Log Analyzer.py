import re
from datetime import datetime
# import json
IP_PATTERN = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
ERROR_PATTERN = r"\b(ERROR|EXCEPTION|CRITICAL|WARNING|FAILED|FATAL)\b"
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


def analyze_log(filename):
    line_count = 0
    ip_count = {}
    error_count = {}
    log_data = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line_count += 1
            log_data.append(line.strip())
            for ip in re.findall(IP_PATTERN, line):
                ip_count[ip] = ip_count.get(ip, 0) + 1

            for error in re.findall(ERROR_PATTERN, line, re.IGNORECASE):
                error = error.upper()
                error_count[error] = error_count.get(error, 0) + 1

    return line_count, ip_count, error_count, log_data


def generate_report(filename, line_count, ip_count, error_count, log_data):
    analysis_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(HEADER)
    print(f"""File          : {filename}
Status        : Completed Successfully
Total Lines   : {line_count}
Analysis Date : {analysis_time}
""")

    print(LOG_CONTENT_HEADER)
    for line in log_data:
        print(line)

    if ip_count:
        print(IP_HEADER)
        for ip, count in ip_count.items():
            print(f"{ip} → {count}")
        print(f"Total IPs     : {sum(ip_count.values())}")
        print(f"Unique IPs    : {len(ip_count)}")
    else:
        print(NO_IP_HEADER)
        print("No IP addresses found in the log file.")

    if error_count:
        print(ERROR_HEADER)
        for error, count in error_count.items():
            print(f"{error} → {count}")
        print(f"Total Errors  : {sum(error_count.values())}")
        print(f"Unique Errors : {len(error_count)}")
    else:
        print(NO_ERROR_HEADER)
        print("No errors found in the log file.")

    print(SUMMARY_HEADER)
    print(f"Total Lines   : {line_count}")
    print(f"Total IPs     : {sum(ip_count.values())}")
    print(f"Unique IPs    : {len(ip_count)}")
    print(f"Total Errors  : {sum(error_count.values())}")
    print(f"Unique Errors : {len(error_count)}")

    print(FOOTER)


def main():
    print("Welcome to the Log Analyzer Tool")
    try:
        filename = input("Enter the log file name: ")
        line_count, ip_count, error_count, log_data = analyze_log(filename)
        generate_report(
            filename,
            line_count,
            ip_count,
            error_count,
            log_data
        )

    except FileNotFoundError:
        print("File not found.")


if __name__ == "__main__":
    main()
