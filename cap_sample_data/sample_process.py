import os
import json

# Directory containing the case files
data_directory = 'cap_sample_data/fla/1'

# List of the first two files to process
files_to_process = ["0001-01.json", "0010-01.json"]

# Function to load JSON files and extract text from nested opinions
def load_case_data(folder_path, files):
    cases = []
    for file in files:
        file_path = os.path.join(folder_path, file)
        if file.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
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

# Load the specified cases from the downloaded files
cases = load_case_data(data_directory, files_to_process)

# Function to create prompt-completion pairs
def create_prompt_completion_pairs(cases):
    prompt_completion_pairs = []
    for case in cases:
        prompt = f"Summarize the following legal case:\n\n{case.get('combined_text', '')}"
        completion = f"Case Name: {case.get('case_name', '')}\nCitation: {case.get('citations', [{}])[0].get('cite', '')}\nDate: {case.get('decision_date', '')}\nCourt: {case.get('court', {}).get('name', '')}\nSummary: {case.get('combined_text', '')}"
        prompt_completion_pairs.append({
            "prompt": prompt,
            "completion": completion
        })
    return prompt_completion_pairs

# Create prompt-completion pairs from the cases
prompt_completion_pairs = create_prompt_completion_pairs(cases)

# Save the prompt-completion pairs to a JSONL file
with open('sample_case_law_data.jsonl', 'w') as f:
    for pair in prompt_completion_pairs:
        json.dump(pair, f)
        f.write('\n')

print("Sample data extraction and saving completed.")
