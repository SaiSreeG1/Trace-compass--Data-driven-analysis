import holboxai as hb
from gpt4all import GPT4All

# Initialize the GPT-4All model
model = GPT4All("mistral-7b-instruct-v0.1.Q4_0")

# Define the custom LLM class
class GPT4AllLLM:
    def __init__(self, model):
        self.model = model

    def __call__(self, prompt):
        response = self.model.generate(prompt, max_tokens=1000)  # Increase max tokens if needed
        return response.strip()

# Initialize the custom LLM
llm = GPT4AllLLM(model=model)

# Function to generate explanation from XML using HolboxAI's summarizer
def generate_explanation_from_xml(xml_str):
    summarizer = hb.Summarizer()
    explanation = summarizer.summarize(xml_str)
    return explanation

# Function to regenerate XML from explanation using GPT-4All
def regenerate_xml_from_explanation(explanation):
    prompt = f"Generate an XML based on the following explanation:\n\n{explanation}\n\nXML:"
    regenerated_xml = llm(prompt)
    return regenerated_xml

# Function to handle multiple XML files
def process_multiple_xmls(xml_list):
    results = []
    for xml_str in xml_list:
        explanation = generate_explanation_from_xml(xml_str)
        regenerated_xml = regenerate_xml_from_explanation(explanation)
        results.append({
            "original_xml": xml_str,
            "explanation": explanation,
            "regenerated_xml": regenerated_xml
        })
    return results

# Example XMLs
xml_list = [
    '''<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="../../org.eclipse.tracecompass.tmf.analysis.xml.core/src/org/eclipse/tracecompass/tmf/analysis/xml/core/module/xmlDefinition.xsd">
    <stateProvider version="0" id="ssh.failed.connections">
        <head>
            <traceType id="custom.txt.trace:Syslog:OpenSSHD" />
            <label value="Failed connections" />
        </head>
        <eventHandler eventName="AUTH FAILURE">
            <stateChange>
                <stateAttribute type="eventField" value="UserID" />
                <stateAttribute type="eventField" value="Message" />
                <stateValue type="int" value="1" increment="true" />
            </stateChange>
            <stateChange>
                <stateAttribute type="eventField" value="UserID" />
                <stateValue type="int" value="1" increment="true" />
            </stateChange>
        </eventHandler>
    </stateProvider>
    <xyView id="failed.connections">
        <head>
            <analysis id="ssh.failed.connections" />
            <label value="Failed Connections" />
        </head>
        <entry path="*" displayType="delta">
            <display type="self" />
        </entry>
    </xyView>
    </tmfxml>''',
    # Add more XML strings as needed
]

# Process multiple XML files
results = process_multiple_xmls(xml_list)

# Print results
for result in results:
    print(f"Original XML:\n{result['original_xml']}\n")
    print(f"Explanation:\n{result['explanation']}\n")
    print(f"Regenerated XML:\n{result['regenerated_xml']}\n")
