import os
import json
import pandas as pd

# Directory containing the case files
data_directory = 'cap_sample_data/fla/1'

# Function to load JSON files and extract text from nested opinions
def load_case_data(folder_path):
    cases = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    try:
                        case_data = json.load(f)
                        opinions = case_data.get('casebody', {}).get('opinions', [])
                        # Combine the text from all opinions
                        text = ' '.join(opinion.get('text', '') for opinion in opinions)
                        if text:  # Ensure combined text is not empty
                            case_data['combined_text'] = text
                            cases.append(case_data)
                        else:
                            print(f"Skipped file {file} due to empty 'text' field in opinions")
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from {file}: {e}")
    return cases

# Load all cases from the downloaded files
cases = load_case_data(data_directory)

# Function to extract relevant information from cases
def extract_sample_text(cases):
    case_texts = []
    for case in cases:
        case_info = {
            'case_name': case.get('name'),
            'citation': case.get('citations', [{}])[0].get('cite', ''),
            'date': case.get('decision_date', ''),
            'court': case.get('court', {}).get('name', ''),
            'text': case.get('combined_text', '')
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
