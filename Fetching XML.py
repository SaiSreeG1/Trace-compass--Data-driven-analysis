import json
from difflib import get_close_matches
from gpt4all import GPT4All

# Load the XML and prompts mapping from a JSON file
def load_prompts_xml_mapping(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Initialize the GPT-4All model
model = GPT4All("mistral-7b-instruct-v0.1.Q4_0")

# Define the custom LLM class
class GPT4AllLLM:
    def __init__(self, model):
        self.model = model

    def generate(self, prompt):
        response = self.model.generate(prompt, max_tokens=1000)
        return response.strip()

# Initialize the custom LLM
llm = GPT4AllLLM(model=model)

# Function to handle XML files and prompts
def process_prompts_with_llm(prompts_xml_mapping, user_prompt, llm):
    # Use fuzzy matching to find the closest prompt
    closest_matches = get_close_matches(user_prompt, prompts_xml_mapping.keys(), n=1, cutoff=0.1)
    if closest_matches:
        prompt = prompts_xml_mapping[closest_matches[0]]
    else:
        prompt = user_prompt
    return llm.generate(prompt)

# Function to save the generated XML to a file
def save_xml_to_file(xml_content, output_file):
    with open(output_file, "w") as file:
        file.write(xml_content)

# Example usage
file_path = r'dataset.json'  # Path to your JSON file
prompts_xml_mapping = load_prompts_xml_mapping(file_path)

user_prompt = "Analyze kernel Linux state system with events like 'exit_syscall', 'irq_handler_entry', and 'sched_switch', updating status of CPUs and threads accordingly."
# Generate XML from user prompt using LLM
generated_xml = process_prompts_with_llm(prompts_xml_mapping, user_prompt, llm)

# Save the generated XML to a file
output_file_path = "generated_output.xml"
save_xml_to_file(generated_xml, output_file_path)

# Print the generated XML
print(f"Generated XML from prompt:\n{generated_xml}\n")
