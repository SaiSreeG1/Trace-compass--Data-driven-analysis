## Introduction
This project aims to enhance data analysis with Trace Compass by generating accurate XML configurations from natural language prompts. Various methods were explored, such as using Hugging Transformers, Holbox AI, and Langchain framework. Finally, the current approach using LLM i.e. Mistral 7B from GPT-4All for natural language processing and FAISS, Sentence transformers for prompt matching was adopted.

## Overview
This repository contains various branches focused on different aspects of XML processing, prompt refinement, and interface creation using the GPT-4All language model and related technologies. Each branch serves a unique purpose, providing specific functionalities and tools to enhance XML generation and analysis.

## Branches and Their Purposes

1. Interface Branch
Description: The final implementation for creating an interactive interface that generates XML content based on user prompts.
Key Features:
Uses Streamlit for a web-based user interface.
Leverages GPT-4All for prompt processing and XML generation.
Implements FAISS for efficient prompt matching and document retrieval.
Supports user feedback and updates the dataset with new XML fragments.

2. Holbox Branch
Description: Focuses on generating explanations from XML files using HolboxAI's summarizer and regenerating XML files using GPT-4All.
Key Features:
Generates human-readable explanations from XML content.
Regenerates XML files from explanations.
Processes multiple XML files and stores the results.

3. Few Shot Prompting Branch
Description: Uses few-shot learning with GPT-4All to generate XML responses based on examples.
Key Features:
Provides several few-shot examples to guide the model.
Sanitizes XML data and generates responses based on prompts.
Saves generated responses to XML files.

4. Extract Key Tags and Keywords Branch
Description: Extracts key tags and keywords from XML content for analysis.
Key Features:
Traverses XML content to identify important elements and attributes.
Consolidates extracted information from multiple XML entries.
Saves the extracted key tags and keywords to a JSON file.

5. Initial Branch
Description: Contains initial implementations for describing XML structure, sanitizing data, and processing XML with GPT-4All.
Key Features:
Describes the structure and important tags of XML files.
Sanitizes XML data by removing comments and unnecessary spaces.
Tokenizes XML content and converts it to YAML format and back.

## How to Use
Installation:
Clone the repository.
Navigate to the repository directory.
Install the required libraries using the provided requirements.txt file or manual installation.

Running the Interface:
Switch to the Interface branch.
Run the Streamlit application as described in the branch-specific README.

Using Other Branches:
Switch to the desired branch (e.g., holbox, few shot prompting, extract key tags and keywords, initial).
Follow the specific instructions provided in the branch or code comments.
