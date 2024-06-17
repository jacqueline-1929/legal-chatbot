import json
import os

# Ensure the data directory exists
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# Load the dataset
data_path = "divorce-update.jsonl"
with open(data_path, 'r', encoding='utf-8') as f:
    dataset = [json.loads(line) for line in f]

# Initial dataset stats
print("Num examples:", len(dataset))
print("First example:")
print(json.dumps(dataset[0], indent=2))

# Validate the format of the dataset
errors = {
    'missing_prompt_or_completion': 0
}

for example in dataset:
    if 'prompt' not in example or 'completion' not in example:
        errors['missing_prompt_or_completion'] += 1

print("Validation errors:", errors)

if errors['missing_prompt_or_completion'] > 0:
    print("Some examples are missing 'prompt' or 'completion' keys.")

# Save the validated data to a new JSONL file
validated_data_path = os.path.join(output_dir, "validated_jsonl_file.jsonl")
with open(validated_data_path, 'w', encoding='utf-8') as f:
    for example in dataset:
        f.write(json.dumps(example) + "\n")

print(f"Validated data saved to '{validated_data_path}'")

# Simplified token counting for checking purposes
try:
    import tiktoken
except ImportError:
    print("Please install the tiktoken package to count tokens accurately.")

def count_tokens(text, encoding="gpt3.5"):
    enc = tiktoken.get_encoding(encoding)
    return len(enc.encode(text))

token_counts = []
for example in dataset:
    total_text = example['prompt'] + " " + example['completion']
    token_counts.append(count_tokens(total_text))

if token_counts:
    mean_tokens = sum(token_counts) / len(token_counts)
    std_tokens = (sum((x - mean_tokens) ** 2 for x in token_counts) / len(token_counts)) ** 0.5
    max_tokens = max(token_counts)
    min_tokens = min(token_counts)

    print("Token count stats:")
    print(f"  Mean: {mean_tokens}")
    print(f"  Std: {std_tokens}")
    print(f"  Max: {max_tokens}")
    print(f"  Min: {min_tokens}")
else:
    print("No token counts calculated.")
