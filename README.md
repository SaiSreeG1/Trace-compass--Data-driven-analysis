## Fetching XML Branch
## Overview
This branch contains code to load prompts and corresponding XML mappings from a JSON file, process user prompts using the GPT-4All language model, and generate XML content. The main goal is to process and generate XML files based on user inputs and existing mappings.

Files: 
1. Fetching XML.py

Loads XML and prompts mapping from a JSON file.
Initializes the GPT-4All model.
Uses a custom LLM class to generate responses from prompts.
Processes prompts with LLM to generate XML content.
Saves the generated XML to a file.

2. Prompt_fetching XML.py

Ensures the environment is set for CPU-only processing.
Loads XML and prompts mapping from a JSON file.
Uses a custom LLM class to generate responses from prompts.
Creates a FAISS index for efficient search and retrieval.
Checks if user prompt exists in the dataset and retrieves corresponding XML.
Refines prompts using the LLM with Chain of Thought technique.
Generates an intermediate representation (IR) of matched XML content.
Generates textual descriptions based on IR and refined prompts.
Saves the updated dataset with generated XML fragments.
