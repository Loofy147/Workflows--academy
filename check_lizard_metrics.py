import sys
import argparse
import xml.etree.ElementTree as ET

def check_lizard_metrics(xml_file, cc_threshold, cog_c_threshold):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error: Malformed XML in {xml_file}: {e}")
        sys.exit(1)

    high_cc_functions = []
    high_cog_c_functions = []

    for file_element in root.findall(".//file"):
        for function_element in file_element.findall(".//function"):
            cyclomatic_complexity = int(function_element.get("cyclomatic_complexity"))
            if cyclomatic_complexity > cc_threshold:
                high_cc_functions.append({
                    "name": function_element.get("name"),
                    "complexity": cyclomatic_complexity,
                    "file": file_element.get("name")
                })

            if "cognitive_complexity" in function_element.attrib:
                cognitive_complexity = int(function_element.get("cognitive_complexity"))
                if cognitive_complexity > cog_c_threshold:
                    high_cog_c_functions.append({
                        "name": function_element.get("name"),
                        "complexity": cognitive_complexity,
                        "file": file_element.get("name")
                    })

    if high_cc_functions:
        print(f"Error: The following functions exceed the cyclomatic complexity threshold of {cc_threshold}:")
        for func in high_cc_functions:
            print(f"  - {func['name']} in {func['file']} (complexity: {func['complexity']})")

    if high_cog_c_functions:
        print(f"Error: The following functions exceed the cognitive complexity threshold of {cog_c_threshold}:")
        for func in high_cog_c_functions:
            print(f"  - {func['name']} in {func['file']} (complexity: {func['complexity']})")

    if high_cc_functions or high_cog_c_functions:
        sys.exit(1)
    else:
        print("All functions are within the complexity thresholds.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check cyclomatic and cognitive complexity from a lizard XML report.")
    parser.add_argument("xml_file", help="The lizard XML report file.")
    parser.add_argument("--cc", type=int, default=15, help="The cyclomatic complexity threshold.")
    parser.add_argument("--cognitive-complexity", type=int, default=10, help="The cognitive complexity threshold.")
    args = parser.parse_args()
    check_lizard_metrics(args.xml_file, args.cc, args.cognitive_complexity)
