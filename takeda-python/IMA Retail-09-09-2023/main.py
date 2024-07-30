
import sys


if len(sys.argv) < 2:
    print("No file path provided.")
    sys.exit(1)

excel_path = sys.argv[1]
print("Excel file path:", excel_path)