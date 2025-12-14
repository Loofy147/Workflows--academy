import sys
import argparse
import xml.etree.ElementTree as ET
import json

def check_lizard_metrics(xml_file, cc_threshold):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error: Malformed XML in {xml_file}: {e}")
        sys.exit(1)

    high_cc_functions = []

    for file_element in root.findall(".//file"):
        for function_element in file_element.findall(".//function"):
            cyclomatic_complexity = int(function_element.get("cyclomatic_complexity"))
            if cyclomatic_complexity > cc_threshold:
                high_cc_functions.append({
                    "name": function_element.get("name"),
                    "complexity": cyclomatic_complexity,
                    "file": file_element.get("name")
                })

    if high_cc_functions:
        print(f"Error: The following functions exceed the cyclomatic complexity threshold of {cc_threshold}:")
        for func in high_cc_functions:
            print(f"  - {func['name']} in {func['file']} (complexity: {func['complexity']})")
        return False
    return True

def check_radon_metrics(json_file, cog_c_threshold):
    try:
        with open(json_file) as f:
            data = json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error: Could not read or parse {json_file}: {e}")
        sys.exit(1)

    high_cog_c_functions = []

    for file_path, metrics in data.items():
        if isinstance(metrics, list):
            for metric in metrics:
                if metric.get("type") == "function" and metric.get("cognitive_complexity") > cog_c_threshold:
                    high_cog_c_functions.append({
                        "name": metric.get("name"),
                        "complexity": metric.get("cognitive_complexity"),
                        "file": file_path
                    })

    if high_cog_c_functions:
        print(f"Error: The following functions exceed the cognitive complexity threshold of {cog_c_threshold}:")
        for func in high_cog_c_functions:
            print(f"  - {func['name']} in {func['file']} (complexity: {func['complexity']})")
        return False
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check cyclomatic and cognitive complexity from lizard and radon reports.")
    parser.add_argument("--lizard-report", help="The lizard XML report file.")
    parser.add_argument("--radon-report", help="The radon JSON report file.")
    parser.add_argument("--cc", type=int, default=15, help="The cyclomatic complexity threshold.")
    parser.add_argument("--cognitive-complexity", type=int, default=10, help="The cognitive complexity threshold.")
    args = parser.parse_args()

    lizard_success = True
    if args.lizard_report:
        lizard_success = check_lizard_metrics(args.lizard_report, args.cc)

    radon_success = True
    if args.radon_report:
        radon_success = check_radon_metrics(args.radon_report, args.cognitive_complexity)

    if lizard_success and radon_success:
        print("All functions are within the complexity thresholds.")
    else:
        sys.exit(1)
