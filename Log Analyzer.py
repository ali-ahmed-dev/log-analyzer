import re
# import json
IP_PATTERN = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
ERROR_PATTERN = r"\b(ERROR|EXCEPTION|CRITICAL|WARNING|FAILED|FATAL)\b"


def analyze_log(filename):
    line_count = 0
    ip_count = {}
    error_count = {}

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line_count += 1
            for ip in re.findall(IP_PATTERN, line):
                ip_count[ip] = ip_count.get(ip, 0) + 1
            for error in re.findall(ERROR_PATTERN, line, re.IGNORECASE):
                error = error.upper()
                error_count[error] = error_count.get(error, 0) + 1
    return line_count, ip_count, error_count


def generate_report(filename, line_count, ip_count, error_count):

    print(f"""File        : {filename}
Status      : Loaded Successfully
Total Lines : {line_count}
""")
    if ip_count:
        print(f"Total IP Addresses Occurrences: {sum(ip_count.values())}")
        print(f"Unique IP Addresses: {len(ip_count)}")
    else:
        print("No IP addresses found in the log file.")

    if error_count:
        print(f"Total Errors Occurrences: {sum(error_count.values())}")
        print(f"Unique Errors: {len(error_count)}")
    else:
        print("No Errors found in the log file.")


def main():
    print("Welcome to the Log Analyzer Tool")
    try:
        filename = input("Enter the log file name: ")
        line_count, ip_count, error_count = analyze_log(filename)
        generate_report(filename, line_count, ip_count, error_count)
    except FileNotFoundError:
        print("File not found.")


if __name__ == "__main__":
    main()
