import json

# Path to your converted data file
data_path = "converted_sample_case_law_data.jsonl"

# Verify the format of the JSONL file
with open(data_path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        try:
            data = json.loads(line)
            if not all(key in data for key in ("prompt", "completion")):
                print(f"Missing keys in line {i + 1}")
            if not isinstance(data["prompt"], str) or not isinstance(data["completion"], str):
                print(f"Invalid types in line {i + 1}")
        except json.JSONDecodeError as e:
            print(f"JSON decode error in line {i + 1}: {e}")

print("Verification completed.")
