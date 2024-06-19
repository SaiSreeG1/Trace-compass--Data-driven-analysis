import re
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from xml.dom.minidom import parseString

# Function to sanitize XML data by removing comments and special characters
def sanitize_xml(xml_data):
    xml_data = re.sub(r'<!--.*?-->', '', xml_data, flags=re.DOTALL)
    xml_data = re.sub(r'\s+', ' ', xml_data)
    return xml_data

# Function to pretty print XML
def pretty_print_xml(xml_string):
    try:
        dom = parseString(xml_string)
        return dom.toprettyxml()
    except Exception as e:
        print(f"Error in pretty printing XML: {e}")
        return xml_string

# Function to generate XML from the prompt
def generate_xml_section(prompt, model, tokenizer):
    inputs = tokenizer(prompt, return_tensors='pt', max_length=512, truncation=True)
    response = model.generate(inputs['input_ids'], max_new_tokens=512, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    generated_text = tokenizer.decode(response[0], skip_special_tokens=True)
    return generated_text

# Define the structure and important tags description
xml_structure_description = """
The XML file has these key elements:
- <tmfxml>: Root element.
- <timeGraphView>: Time graph view with <head>, <definedValue>, and <entry>.
- <pattern>: Defines analysis pattern with <head>, <storedField>, <location>, and <patternHandler> including <test>, <action>, and <fsm>.
"""

important_tags_description = """
Important tags for the task:
- <irq>: Interrupt request.
- <name>: Name associated with irq.
- <cpu>: CPU associated with irq.
These tags should be categorized by a 'tid' and shown in the irqs vs time format.
"""

example_prompt = """
With this prompt:
<irq>123</irq><name>example_irq</name><cpu>0</cpu>
giving this output:
<irq>123</irq><name>example_irq</name><cpu>0</cpu><tid>1234</tid>
make me an xml representing the user prompt.
"""

# Your XML data
xml_data = """
<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <timeGraphView id="xml.scenarios">
        <head>
            <analysis id="lttng.analysis.irq" />
            <label value="Scenarios" />
        </head>
        <definedValue name="PENDING" value="0" color="#CCCCCC" />
        <definedValue name="IN_PROGRESS" value="1" color="#00CCFF" />
        <definedValue name="MATCHED" value="2" color="#118811" />
        <definedValue name="ABANDONED" value="3" color="#EE0000" />
        <entry path="scenarios/*">
            <display type="self" />
            <name type="self" />
            <entry path="*">
                <display type="constant" value="state" />
                <name type="self" />
            </entry>
        </entry>
    </timeGraphView>
    <pattern version="0" id="lttng.analysis.irq">
        <head>
            <traceType id="org.eclipse.linuxtools.lttng2.kernel.tracetype" />
            <label value="IRQ Analysis" />
            <viewLabelPrefix value="IRQ" />
        </head>
        <storedField id="ret" alias="ret" />
        <location id="CurrentCPU">
            <stateAttribute type="constant" value="CPUs" />
            <stateAttribute type="eventField" value="cpu" />
        </location>
        <patternHandler>
            <test id="test_cpu">
                <if>
                    <condition>
                        <stateValue type="query">
                            <stateAttribute type="constant" value="#CurrentScenario" />
                            <stateAttribute type="constant" value="cpu" />
                        </stateValue>
                        <stateValue type="eventField" value="cpu" />
                    </condition>
                </if>
            </test>
            <action id="irq_handler_entry">
                <stateChange>
                    <stateAttribute type="constant" value="#CurrentScenario" />
                    <stateAttribute type="constant" value="irq" />
                    <stateValue type="eventField" value="irq" />
                </stateChange>
                <stateChange>
                    <stateAttribute type="constant" value="#CurrentScenario" />
                    <stateAttribute type="constant" value="name" />
                    <stateValue type="eventField" value="name" />
                </stateChange>
                <stateChange>
                    <stateAttribute type="constant" value="#CurrentScenario" />
                    <stateAttribute type="constant" value="cpu" />
                    <stateValue type="eventField" value="cpu" />
                </stateChange>
            </action>
            <action id="irq_handler_exit">
                <segment>
                    <segType>
                        <segName>
                            <stateValue type="query">
                                <stateAttribute type="constant" value="#CurrentScenario" />
                                <stateAttribute type="constant" value="name" />
                            </stateValue>
                        </segName>
                    </segType>
                    <segContent>
                        <segField name="ret" type="long">
                            <stateValue type="eventField" value="ret" />
                        </segField>
                        <segField name="irq" type="long">
                            <stateValue type="query">
                                <stateAttribute type="constant" value="#CurrentScenario" />
                                <stateAttribute type="constant" value="irq" />
                            </stateValue>
                        </segField>
                        <segField name="cpu" type="long">
                            <stateValue type="eventField" value="cpu" />
                        </segField>
                    </segContent>
                </segment>
            </action>
            <fsm id="irq_handler" initial="wait_irq_entry">
                <precondition event="irq_handler_*" />
                <state id="wait_irq_entry">
                    <transition event="irq_handler_entry" target="wait_irq_exit" action="irq_handler_entry" />
                </state>
                <state id="wait_irq_exit">
                    <transition event="irq_handler_exit" cond="test_cpu" target="irq" action="irq_handler_exit" />
                </state>
                <final id="irq" />
            </fsm>
            <action id="update_current_thread">
                <stateChange>
                    <stateAttribute type="location" value="CurrentCPU" />
                    <stateAttribute type="constant" value="Current_thread" />
                    <stateValue type="eventField" value="next_tid" />
                </stateChange>
            </action>
            <fsm id="sched_switch" multiple="false">
                <precondition event="sched_switch" />
                <state id="sched_switch">
                    <transition event="sched_switch" target="sched_switch" action="update_current_thread" />
                </state>
            </fsm>
        </patternHandler>
    </pattern>
</tmfxml>
"""

sanitized_xml_data = sanitize_xml(xml_data)

# Load the model and tokenizer from Hugging Face
model_name = "EleutherAI/gpt-neo-2.7B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Initialize conversation
conversation = ""

# Step 1: Introduction
conversation += "Let's work on generating a proper XML output based on your requirements.\n\n"

# Step 2: Explain XML structure
conversation += f"Step 1: The XML file has these key elements:\n{xml_structure_description}\n\n"

# Step 3: Highlight important tags
conversation += f"Step 2: Important tags for the task:\n{important_tags_description}\n\n"

# Step 4: Provide example prompt
conversation += f"Step 3: Example of input-output relationship:\n{example_prompt}\n\n"

# Step 5: Provide user prompt and XML content
user_prompt = f"""
Step 4: The XML file structure has been explained. Based on this structure, show the irqs vs time where each irq name is categorized by a tid.
Here is the XML content:

{sanitized_xml_data}

Please ensure the output XML includes a section with irqs vs time, where each irq name is categorized by a tid, and maintains the original XSD format.
"""

# Generate the XML output
generated_xml = generate_xml_section(conversation + user_prompt, model, tokenizer)

# Pretty print the XML
pretty_xml = pretty_print_xml(generated_xml)

# Print the generated response
print(f"Generated response: {pretty_xml}")

# Save the modified XML text to a new file
modified_output_file_path = os.path.join(os.getcwd(), 'modified_irq_analysis_lttng_hugg.xml')
with open(modified_output_file_path, 'w') as modified_text_file:
    modified_text_file.write(pretty_xml)

print(f"Modified XML content has been saved to {modified_output_file_path}")
