# import re
# import json


def analyze_log(filename):
    line_count = 0
    with open(filename, "r", encoding="utf-8") as file:
        for _ in file:
            line_count += 1
    return line_count


def generate_report(filename, line_count):

    print(f"""File        : {filename}
Status      : Loaded Successfully
Total Lines : {line_count}
""")


def main():
    print("Welcome to the Log Analyzer Tool")
    try:
        filename = input("Enter the log file name: ")
        line_count = analyze_log(filename)
        generate_report(filename, line_count)
    except FileNotFoundError:
        print("File not found.")


if __name__ == "__main__":
    main()
