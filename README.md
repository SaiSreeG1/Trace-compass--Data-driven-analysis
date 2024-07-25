# Trace Compass Extended Assistant

## Introduction
This project aims to enhance data analysis with Trace Compass by generating accurate XML configurations from natural language prompts. Various methods were explored, such as using Hugging Transformers, Holbox AI, and Langchain framework. Finally, the current approach using LLM i.e. Mistral 7B from GPT-4All for natural language processing and FAISS, Sentence transformers for prompt matching was adopted.

## Features
- Advanced prompt engineering with techniques like Chain of Thought prompting.
- AI-driven DSL assistance using GPT-4All.
- Automated generation of XML files from natural language prompts.
- User-friendly interface with session management, feedback collection, and download options for generated XML files.
- Efficient prompt matching using FAISS and Sentence Transformers.
- Ability to import generated XML into Trace Compass for further analysis.

## To use this project, follow these steps:
1. Start the Streamlit application: streamlit run Interface.py
2. Open the application in your web browser. You will see a user interface where you can enter prompts and generate XML files.
3. Enter a natural language prompt in the text area provided.
4. Click "Generate XML" to generate an XML file based on the entered prompt.
5. If the generated XML matches an existing prompt in the dataset, it will be retrieved and displayed. If the prompt does not exist, a refined prompt will be generated, and the closest matching XML document will be retrieved and displayed.
6. You can download the generated XML file by clicking the "Download XML" button.

## Overview
This project uses Streamlit for the web interface, GPT-4All for natural language processing, and FAISS with Sentence Transformers for efficient prompt matching. The goal is to generate XML files from natural language prompts for use in Trace Compass.

## Detailed Explanation of the code (Interface.py)
1. Environment Configuration: The code sets the environment for CPU-only processing to ensure compatibility and performance.
2. Loading and Saving Data: JSON files are used to load and save the XML and prompts mapping. This allows the system to persistently store and retrieve data.
3. Custom LLM Class: A custom class for GPT-4All is defined to handle prompt generation. This includes methods for generating responses and reinitializing the model.
4. Model Initialization: The GPT-4All model is initialized with a specific model path, and data is loaded from a JSON file.
5. Creating FAISS Index: FAISS and Sentence Transformers are used to create an index for prompt embeddings. This allows efficient matching of user prompts with existing prompts in the dataset.
6. Prompt Matching: The code checks if a user prompt exists in the dataset using FAISS. If a match is found, the corresponding XML is retrieved.
7. Refining Prompts: If no exact match is found, the user prompt is refined using GPT-4All with a Chain of Thought approach to create a more accurate prompt.
8. Creating Intermediate Representation: The matched XML content is converted into an intermediate representation (IR) for easier manipulation and understanding.
9. Generating Text from IR: The IR is used to generate a detailed text explanation, which is then converted into an XML fragment.
10. Streamlit Interface: The user interface is built using Streamlit, allowing users to enter prompts, generate XML, provide feedback, and download the generated XML.
11. Session Management: Streamlit's session state is used to manage the state of the application, including storing generated XML fragments and user feedback.
12. Feedback Mechanism: Users can provide feedback on the generated XML, which is used to improve the quality of future outputs.
13. Reinitializing for New Prompts: The application can be reset for new prompts, clearing the session state and reinitializing the model.


