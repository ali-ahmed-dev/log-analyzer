# import re
# import json


def analyze_log(filename):
    pass


def generate_report():
    pass


def main():
    print("Welcome to the Log Analyzer Tool")
    filename = input("Enter the log file name: ")
    try:
        analyze_log(filename)
    except FileNotFoundError:
        print("File not found.")


if __name__ == "__main__":
    main()
