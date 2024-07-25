import re
import yaml
from gpt4all import GPT4All
from tqdm import tqdm
import xml.etree.ElementTree as ET
from xml.dom import minidom

# XML content embedded directly in the code
xml_data = """
<?xml version="1.0" encoding="UTF-8"?>
<!-- *****************************************************************************
 * Copyright (c) 2021 Ericsson
 *
 * All rights reserved. This program and the accompanying materials are
 * made available under the terms of the Eclipse Public License 2.0 which
 * accompanies this distribution, and is available at
 * https://www.eclipse.org/legal/epl-2.0/
 *
 * SPDX-License-Identifier: EPL-2.0
 ***************************************************************************** -->
<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="../../org.eclipse.tracecompass.tmf.analysis.xml.core/src/org/eclipse/tracecompass/tmf/analysis/xml/core/module/xmlDefinition.xsd">
    <stateProvider version="0"
                   id="ssh.failed.connections">
        <head>
            <traceType id="custom.txt.trace:Syslog:OpenSSHD" />
            <label value="Failed connections" />
        </head>
        <eventHandler eventName="AUTH FAILURE">
            <stateChange>
                <stateAttribute type="eventField"
                                value="UserID" />
                <stateAttribute type="eventField"
                                value="Message" />
                <stateValue type="int"
                            value="1"
                            increment="true" />
            </stateChange>
            <stateChange>
                <stateAttribute type="eventField"
                                value="UserID" />
                <stateValue type="int"
                            value="1"
                            increment="true" />
            </stateChange>
        </eventHandler>
    </stateProvider>
    <xyView id="failed.connections">
        <head>
            <analysis id="ssh.failed.connections" />
            <label value="Failed Connections" />
        </head>
        <entry path="*"
               displayType="delta">
            <display type="self" />
        </entry>
    </xyView>
</tmfxml>
"""

# Function to tokenize XML data
def tokenize_xml(xml_data):
    """Tokenize the XML data into a sequence of tokens"""
    tokens = re.findall(r'(<[^>]+>|[^<]+)', xml_data)
    return tokens

# Function to detokenize tokens back to XML
def detokenize_xml(tokens):
    """Convert a sequence of tokens back into XML data"""
    return ''.join(tokens)

# Function to create a simulated attention mask
def create_attention_mask(tokens):
    """Create a simulated attention mask for the tokens"""
    return [1] * len(tokens)

# Function to process tokens to YAML using GPT model
def process_tokens_to_yaml(model, tokens, prompt):
    """Generate YAML output for the entire token sequence"""
    token_str = yaml.dump(tokens)
    full_prompt = f"{prompt}\n\n{token_str}\n\nReturn the content above in a structured YAML format."
    response = []
    with model.chat_session():
        for _ in tqdm(range(1), desc="Processing Tokens to YAML"):
            response.append(model.generate(full_prompt))
    return ''.join(response)

# Function to convert YAML content back to token sequence
def yaml_to_tokens(yaml_content):
    """Convert YAML content back to a sequence of tokens"""
    return yaml.safe_load(yaml_content)

# Main function
def main():
    # Tokenize the XML data
    tokens = tokenize_xml(xml_data)

    # Create a simulated attention mask
    attention_mask = create_attention_mask(tokens)

    # Print the attention mask for debugging
    print("Attention Mask:", attention_mask)

    # Initialize the model
    model = GPT4All(model_name="mistral-7b-instruct-v0.1.Q4_0.gguf", device='cpu')

    # Define the prompt
    prompt = "Convert the following XML token sequence to YAML format without any modifications."

    # Process the entire token sequence to YAML
    yaml_output = process_tokens_to_yaml(model, tokens, prompt)

    # Extract YAML from response
    try:
        tokens_from_yaml = yaml_to_tokens(yaml_output)
    except yaml.YAMLError as e:
        print("Error decoding YAML:", e)
        print("YAML output received:", yaml_output)
        return

    # Detokenize the tokens back to XML
    xml_output = detokenize_xml(tokens_from_yaml)

    # Save the final generated XML to a file
    modified_output_file_path = r'modified_ssh_failed_connections.xml'
    with open(modified_output_file_path, 'w', encoding='utf-8') as modified_text_file:
        modified_text_file.write(xml_output.strip())

    print(f"Modified XML content has been saved to {modified_output_file_path}")

if __name__ == "__main__":
    main()
