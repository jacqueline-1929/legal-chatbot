import requests
import os
import json
import pandas as pd

# Base URL for the case files
base_url = "https://static.case.law/fla/1/cases/"

# List of files to download
files_to_download = [
    "0001-01.json", "0010-01.json", "0025-01.json", "0037-01.json",
    "0056-01.json", "0063-01.json", "0092-01.json", "0094-01.json",
    "0110-01.json", "0133-01.json", "0136-01.json", "0155-01.json",
    "0160-01.json", "0189-01.json", "0197-01.json", "0197-02.json",
    "0198-01.json", "0210-01.json", "0211-01.json", "0219-01.json",
    "0226-01.json", "0232-01.json", "0233-01.json", "0242-01.json",
    "0245-01.json", "0262-01.json", "0271-01.json", "0281-01.json",
    "0292-01.json"
]

# Create a directory to store the files
os.makedirs('cap_sample_data/fla/1', exist_ok=True)

# Function to download a file from a URL
def download_file(file_name, base_url, folder):
    url = base_url + file_name
    local_filename = os.path.join(folder, file_name)
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded {local_filename}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    return local_filename

# Download all the case files
for file_name in files_to_download:
    download_file(file_name, base_url, 'cap_sample_data/fla/1')

# Function to load JSON files
def load_case_data(folder_path):
    cases = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(root, file), 'r') as f:
                    try:
                        case_data = json.load(f)
                        cases.append(case_data)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from {file}: {e}")
    return cases

# Load all cases from the downloaded files
cases = load_case_data('cap_sample_data/fla/1')

# Function to extract relevant information from cases
def extract_sample_text(cases):
    case_texts = []
    for case in cases:
        case_info = {
            'case_name': case.get('name'),
            'citation': case.get('citations', [{}])[0].get('cite', ''),
            'date': case.get('decision_date', ''),
            'court': case.get('court', {}).get('name', ''),
            'text': ' '.join([opinion.get('text', '') for opinion in case.get('casebody', {}).get('data', {}).get('opinions', [])])
        }
        case_texts.append(case_info)
    return case_texts

# Extract relevant information from the cases
sample_case_texts = extract_sample_text(cases)

# Save the sample data to CSV for easy inspection
df_sample = pd.DataFrame(sample_case_texts)
df_sample.to_csv('sample_case_law_data.csv', index=False)

# Convert to JSONL format for the ChatGPT API
df_sample.to_json('sample_case_law_data.jsonl', orient='records', lines=True)

print("Data extraction and saving completed.")
