import os
import json
import streamlit as st
from gpt4all import GPT4All
from sentence_transformers import SentenceTransformer, util
import faiss
import xml.etree.ElementTree as ET
import base64

# Ensure the environment is set for CPU-only processing
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Load the XML and prompts mapping from a JSON file
def load_prompts_xml_mapping(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Save the updated dataset
def save_updated_dataset(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    print("Updated JSON dataset saved successfully.")

# Define the custom LLM class
class GPT4AllLLM:
    def __init__(self, model_path):
        self.model_path = model_path
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
    
    def reinitialize(self):
        self.model = GPT4All(self.model_path)

# Initialize the GPT-4All model
llm = GPT4AllLLM("mistral-7b-instruct-v0.1.Q4_0")

# Load data
file_path = 'trans_dataset.json'
prompts_xml_mapping = load_prompts_xml_mapping(file_path)

# Create FAISS index
embeddings_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
prompts = [prompt for section in prompts_xml_mapping.values() for prompt in section.keys()]
documents = [entry["XML"] for section in prompts_xml_mapping.values() for entry in section.values()]
prompt_embeddings = embeddings_model.encode(prompts, show_progress_bar=True)
document_embeddings = embeddings_model.encode(documents, show_progress_bar=True)
index = faiss.IndexFlatIP(prompt_embeddings.shape[1])
faiss.normalize_L2(prompt_embeddings)
index.add(prompt_embeddings)

# Check if user prompt exists in the dataset using FAISS
def check_existing_prompt(user_prompt, index, embeddings_model, prompts):
    user_prompt_embedding = embeddings_model.encode([user_prompt])
    faiss.normalize_L2(user_prompt_embedding)
    D, I = index.search(user_prompt_embedding, 1)
    closest_prompt = prompts[I[0][0]]
    similarity_score = D[0][0]
    return closest_prompt, similarity_score

# Retrieve and augment using FAISS
def retrieve_and_augment(user_prompt, index, embeddings_model, documents):
    refined_prompt_embedding = embeddings_model.encode([user_prompt])
    faiss.normalize_L2(refined_prompt_embedding)
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

# Add the company logo at the top of the page and center it
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

image_path = "C:/Users/egsuaid/Downloads/1.jpg"
base64_image = get_base64_image(image_path)

st.markdown(
    """
    <style>
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 150px; /* Adjust the height as needed */
    }
    .spacer {
        height: 20px; /* Adjust the height of the space as needed */
    }
    div.stButton > button:first-child { background-color: #4CAF50; color: white; }
    div[data-baseweb="radio"] > label:first-child > div:first-child { background-color: #4CAF50; color: white; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="center">
        <img src="data:image/jpeg;base64,{base64_image}" width="500">
    </div>
    <div class="spacer"></div>
    """,
    unsafe_allow_html=True
)

# Streamlit UI
st.title("Trace Compass Extended Assistant")
st.write("Enter a prompt to generate an XML.")

# Initialize session state
if 'generated_xml_fragment' not in st.session_state:
    st.session_state.generated_xml_fragment = None
if 'llm_generated' not in st.session_state:
    st.session_state.llm_generated = False
if 'show_feedback' not in st.session_state:
    st.session_state.show_feedback = False
if 'feedback' not in st.session_state:
    st.session_state.feedback = None
if 'user_prompt' not in st.session_state:
    st.session_state.user_prompt = ""

user_prompt = st.text_area("Enter your prompt here:", st.session_state.user_prompt)

if st.button("Generate XML"):
    if user_prompt:
        # Store user prompt in session state
        st.session_state.user_prompt = user_prompt

        # Check if the user prompt already exists in the dataset
        closest_prompt, similarity_score = check_existing_prompt(user_prompt, index, embeddings_model, prompts)

        # Set a similarity threshold to determine if the prompt is a close match
        similarity_threshold = 0.8

        existing_xml = None
        if similarity_score >= similarity_threshold:
            for section in prompts_xml_mapping.values():
                if closest_prompt in section:
                    existing_xml = section[closest_prompt]["XML"]
                    user_inputted = section[closest_prompt]["User_inputted"]
                    break

        if existing_xml:
            st.session_state.generated_xml_fragment = existing_xml
            st.session_state.llm_generated = False
        else:
            # Step 1: Refine the User Prompt
            refined_prompt = refine_prompt_with_llm(user_prompt, llm, "")
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

            # Extract the XML fragment from the textual description
            try:
                st.session_state.generated_xml_fragment = text_description.split('```xml')[1].split('```')[0].strip()
            except IndexError:
                st.session_state.generated_xml_fragment = "Error: Unable to extract XML fragment."
            st.session_state.llm_generated = True

        st.session_state.show_feedback = True

if st.session_state.generated_xml_fragment:
    # Display the generated XML fragment
    st.code(st.session_state.generated_xml_fragment, language="xml")

    if st.session_state.show_feedback:
        # Provide options for feedback
        st.write("We value your feedback. Please select one of the options below:")
        feedback_options = ["XML is correct", "XML is not correct", "I don't know"]
        st.session_state.feedback = st.radio("", feedback_options, key="feedback_radio", index=None)

        if st.session_state.feedback:
            if st.button("Done"):
                if st.session_state.feedback == "XML is correct" and st.session_state.llm_generated:
                    # Add to LLM generated dictionary
                    new_entry = {
                        st.session_state.user_prompt: {
                            "User_inputted": False,
                            "LLM_Snippet": True,
                            "XML": st.session_state.generated_xml_fragment
                        }
                    }
                    if "LLM_Generated" not in prompts_xml_mapping:
                        prompts_xml_mapping["LLM_Generated"] = new_entry
                    else:
                        prompts_xml_mapping["LLM_Generated"].update(new_entry)
                    save_updated_dataset(file_path, prompts_xml_mapping)
                    st.write("The XML has been added to the dataset.")

                st.session_state.show_feedback = False

        # Provide a download link for the XML file
        st.markdown(
            """
            <style>
            div.stDownloadButton > button:first-child { background-color: #4CAF50; color: white; }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.download_button(
            label="Download XML",
            data=st.session_state.generated_xml_fragment,
            file_name="generated_output.xml",
            mime="application/xml"
        )

if st.button("New Prompt"):
    # Clear the session state variables
    st.session_state.user_prompt = ""  # Clear the user prompt explicitly
    st.session_state.generated_xml_fragment = None
    st.session_state.llm_generated = False
    st.session_state.show_feedback = False
    st.session_state.feedback = None
    llm.reinitialize()  # Reinitialize the LLM model
    st.rerun()  # Use st.rerun() instead of st.experimental_rerun()

st.markdown(
    "<p style='font-size: 12px; color: red;'>The XML content might not be completely correct, please check before using it.</p>",
    unsafe_allow_html=True
)
