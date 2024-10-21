import os
import json
from gpt4all import GPT4All
from sentence_transformers import SentenceTransformer, util
import faiss
import xml.etree.ElementTree as ET

# Ensure the environment is set for CPU-only processing
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Load the XML and prompts mapping from a JSON file
def load_prompts_xml_mapping(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Define the custom LLM class
class GPT4AllLLM:
    def __init__(self, model_path):
        self.model = GPT4All(model_path)
        self.context_window_size = 2048

    def generate(self, prompt, context=""):
        full_prompt = context + "\n\n" + prompt if context else prompt
        prompt_length = len(full_prompt.split())
        print(f"Prompt length: {prompt_length} tokens")
        if prompt_length > self.context_window_size:
            return f"Prompt exceeds the context window size of {self.context_window_size} tokens."
        try:
            response = self.model.generate(prompt=full_prompt, max_tokens=1000)
        except Exception as e:
            return f"Error during model generation: {str(e)}"
        return response.strip()

# Initialize the GPT-4All model
model_path = "mistral-7b-instruct-v0.1.Q4_0"
llm = GPT4AllLLM(model_path)

# Load data
file_path = r'trans_dataset.json'
prompts_xml_mapping = load_prompts_xml_mapping(file_path)

# Create FAISS index
embeddings_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
documents = [entry["XML"] for section in prompts_xml_mapping.values() for entry in section.values()]
embeddings = embeddings_model.encode(documents, show_progress_bar=True)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Check if user prompt exists in the dataset
def check_existing_prompt(user_prompt, prompts_xml_mapping):
    for section in prompts_xml_mapping.values():
        for prompt, data in section.items():
            if user_prompt.strip().lower() == prompt.strip().lower():
                return data["XML"]
    return None

# Retrieve and augment using FAISS
def retrieve_and_augment(user_prompt, index, embeddings_model, documents):
    refined_prompt_embedding = embeddings_model.encode([user_prompt])
    D, I = index.search(refined_prompt_embedding, 1)
    closest_document = documents[I[0][0]]
    return closest_document

# Function to refine the prompt using LLM with Chain of Thought
def refine_prompt_with_llm(user_prompt, llm, context):
    cot_prompt = (
        f"Refine the following prompt to match an XML mapping. Identify the key elements and attributes needed, and provide the refined prompt.\n\n"
        f"User prompt: {user_prompt}\n\n"
        f"Step 1: Identify the key elements such as segment name and fields.\n"
        f"Step 2: Ensure the refined prompt aligns with the given prompt.\n"
        f"Step 3: Provide the refined prompt in a well-structured format."
    )
    response = llm.generate(cot_prompt, context)
    return response

# Function to create an Intermediate Representation (IR) of the matched XML content
def create_ir_from_xml(xml_content):
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError:
        return "Error: Failed to parse XML content."

    def element_to_dict(element):
        return {
            "tag": element.tag,
            "attrib": element.attrib,
            "text": element.text.strip() if element.text else "",
            "children": [element_to_dict(child) for child in element]
        }

    def dict_to_ir(data, level=0):
        indent = "  " * level
        ir = f"{indent}Tag: {data['tag']}\n"
        if data['attrib']:
            ir += f"{indent}Attributes: {data['attrib']}\n"
        if data['text']:
            ir += f"{indent}Text: {data['text']}\n"
        for child in data['children']:
            ir += dict_to_ir(child, level + 1)
        return ir

    xml_dict = element_to_dict(root)
    ir = dict_to_ir(xml_dict)
    return ir

# Enhanced XML Fragment Generation Logic
def generate_text_from_ir(xml_ir, refined_prompt):
    prompt = (
        f"Using the following intermediate representation of the XML content, write a detailed text explanation that describes the structure and elements required by the refined prompt.\n\n"
        f"Intermediate Representation:\n{xml_ir}\n\n"
        f"Refined prompt: {refined_prompt}\n\n"
        f"Provide a detailed text explanation that can later be converted into an XML fragment."
    )
    response = llm.generate(prompt)
    return response

# Save the updated dataset
def save_updated_dataset(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    print("Updated JSON dataset saved successfully.")

# Main code execution
user_prompt = "Extract the XML simple pattern with time graph view and with id attributes xml.core.tests.simple.pattern.timegraph and xml.core.tests.simple.pattern.timegraph2."
context = "Follow the steps to ensure accurate extraction of the XML fragment."

# Check if the user prompt already exists in the dataset
existing_xml = check_existing_prompt(user_prompt, prompts_xml_mapping)

if existing_xml:
    generated_xml_fragment = existing_xml
else:
    # Step 1: Refine the User Prompt
    refined_prompt = refine_prompt_with_llm(user_prompt, llm, context)
    print(f"Refined prompt: {refined_prompt}")

    # Step 2: Retrieve the Closest XML Document
    matched_xml_content = retrieve_and_augment(refined_prompt, index, embeddings_model, documents)
    print(f"Matched XML content: {matched_xml_content}")

    # Step 3: Create Intermediate Representation from the Matched XML Content
    xml_ir = create_ir_from_xml(matched_xml_content)
    print(f"Intermediate Representation: {xml_ir}")

    # Step 4: Generate the Textual Intermediate Format Using the Intermediate Representation and Refined Prompt
    text_description = generate_text_from_ir(xml_ir, refined_prompt)
    print(f"Text description: {text_description}")

    # Save the LLM-generated XML to the dataset
    prompts_xml_mapping["LLM_Generated"][user_prompt] = {
        "User_inputted": False,
        "LLM_Snippet": True,
        "XML": text_description
    }

    # Save the updated dataset
    save_updated_dataset(file_path, prompts_xml_mapping)

    generated_xml_fragment = text_description

# Save the generated XML fragment to a file
output_file_path = "generated_output_rag.xml"
with open(output_file_path, "w") as file:
    file.write(generated_xml_fragment)

print(f"Generated XML fragment has been saved to {output_file_path}")
