import re
# import json
IP_PATTERN = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"


def analyze_log(filename):
    line_count = 0
    ip_count = {}

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line_count += 1
            for ip in re.findall(IP_PATTERN, line):
                ip_count[ip] = ip_count.get(ip, 0) + 1
    return line_count, ip_count


def generate_report(filename, line_count, ip_count):

    print(f"""File        : {filename}
Status      : Loaded Successfully
Total Lines : {line_count}
""")
    if ip_count:
        print(f"Total IP Addresses Occurrences: {sum(ip_count.values())}")
        print(f"Unique IP Addresses: {len(ip_count)}")
    else:
        print("No IP addresses found in the log file.")


def main():
    print("Welcome to the Log Analyzer Tool")
    try:
        filename = input("Enter the log file name: ")
        line_count, ip_count = analyze_log(filename)
        generate_report(filename, line_count, ip_count)
    except FileNotFoundError:
        print("File not found.")


if __name__ == "__main__":
    main()
