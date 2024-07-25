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

xml_explanation = f"{xml_structure_description}\n\n{important_tags_description}"

from gpt4all import GPT4All
import os
import tqdm

model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf")
import re
from gpt4all import GPT4All

# Function to sanitize XML data by removing comments and special characters
def sanitize_xml(xml_data):
    # Remove comments
    xml_data = re.sub(r'<!--.*?-->', '', xml_data, flags=re.DOTALL)
    # Remove newlines and extra spaces
    xml_data = re.sub(r'\s+', ' ', xml_data)
    return xml_data

# Your XML data
xml_data = """
<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <!-- Timegraph view that show the scenario execution state in time -->
    <timeGraphView id="xml.scenarios">
        <head>
            <analysis id="lttng.analysis.irq" />
            <label value="Scenarios" />
        </head>
        <!-- FFA040 -->
        <definedValue name="PENDING"
                      value="0"
                      color="#CCCCCC" />
        <definedValue name="IN_PROGRESS"
                      value="1"
                      color="#00CCFF" />
        <definedValue name="MATCHED"
                      value="2"
                      color="#118811" />
        <definedValue name="ABANDONED"
                      value="3"
                      color="#EE0000" />
        <!-- Scenario view -->
        <entry path="scenarios/*">
            <display type="self" />
            <name type="self" />
            <entry path="*">
                <display type="constant"
                         value="state" />
                <name type="self" />
            </entry>
        </entry>
    </timeGraphView>
    <pattern version="0"
             id="lttng.analysis.irq">
        <head>
            <traceType id="org.eclipse.linuxtools.lttng2.kernel.tracetype" />
            <label value="IRQ Analysis" />
            <viewLabelPrefix value="IRQ" />
        </head>
        <storedField id="ret"
                     alias="ret" />
        <location id="CurrentCPU">
            <stateAttribute type="constant"
                            value="CPUs" />
            <stateAttribute type="eventField"
                            value="cpu" />
        </location>
        <patternHandler>
            <!-- MATCHING INPUTS -->
            <test id="test_cpu">
                <if>
                    <condition>
                        <stateValue type="query">
                            <stateAttribute type="constant"
                                            value="#CurrentScenario" />
                            <stateAttribute type="constant"
                                            value="cpu" />
                        </stateValue>
                        <stateValue type="eventField"
                                    value="cpu" />
                    </condition>
                </if>
            </test>
            <!-- IRQ FSM ACTIONS -->
            <action id="irq_handler_entry">
                <stateChange>
                    <stateAttribute type="constant"
                                    value="#CurrentScenario" />
                    <stateAttribute type="constant"
                                    value="irq" />
                    <stateValue type="eventField"
                                value="irq" />
                </stateChange>
                <stateChange>
                    <stateAttribute type="constant"
                                    value="#CurrentScenario" />
                    <stateAttribute type="constant"
                                    value="name" />
                    <stateValue type="eventField"
                                value="name" />
                </stateChange>
                <stateChange>
                    <stateAttribute type="constant"
                                    value="#CurrentScenario" />
                    <stateAttribute type="constant"
                                    value="cpu" />
                    <stateValue type="eventField"
                                value="cpu" />
                </stateChange>
            </action>
            <action id="irq_handler_exit">
                <segment>
                    <segType>
                        <segName>
                            <stateValue type="query">
                                <stateAttribute type="constant"
                                                value="#CurrentScenario" />
                                <stateAttribute type="constant"
                                                value="name" />
                            </stateValue>
                        </segName>
                    </segType>
                    <segContent>
                        <segField name="ret"
                                  type="long">
                            <stateValue type="eventField"
                                        value="ret" />
                        </segField>
                        <segField name="irq"
                                  type="long">
                            <stateValue type="query">
                                <stateAttribute type="constant"
                                                value="#CurrentScenario" />
                                <stateAttribute type="constant"
                                                value="irq" />
                            </stateValue>
                        </segField>
                        <segField name="cpu"
                                  type="long">
                            <stateValue type="eventField"
                                        value="cpu" />
                        </segField>
                    </segContent>
                </segment>
            </action>
            <!-- IRQ FSM -->
            <fsm id="irq_handler"
                 initial="wait_irq_entry">
                <precondition event="irq_handler_*" />
                <state id="wait_irq_entry">
                    <transition event="irq_handler_entry"
                                target="wait_irq_exit"
                                action="irq_handler_entry" />
                </state>
                <state id="wait_irq_exit">
                    <transition event="irq_handler_exit"
                                cond="test_cpu"
                                target="irq"
                                action="irq_handler_exit" />
                </state>
                <final id="irq" />
            </fsm>
            <!-- SCHED_SWITCH -->
            <action id="update_current_thread">
                <stateChange>
                    <stateAttribute type="location"
                                    value="CurrentCPU" />
                    <stateAttribute type="constant"
                                    value="Current_thread" />
                    <stateValue type="eventField"
                                value="next_tid" />
                </stateChange>
            </action>
            <fsm id="sched_switch"
                 multiple="false">
                <precondition event="sched_switch" />
                <state id="sched_switch">
                    <transition event="sched_switch"
                                target="sched_switch"
                                action="update_current_thread" />
                </state>
            </fsm>
        </patternHandler>
    </pattern>
</tmfxml>
"""

# Sanitize the XML data
sanitized_xml_data = sanitize_xml(xml_data)

# Define your prompt
prompt = "Show me the irqs vs time where you store the irq name it should be categorized by a tid."

# Combine the XML explanation and the prompt with the sanitized XML data
full_prompt = f"{xml_explanation}\n\nHere is the XML content:\n\n{sanitized_xml_data}\n\n{prompt}\n\nPlease ensure the output XML has a section with irqs vs time where each irq name is categorized by a tid. Maintain the original XSD format."

prompts = []
responses = []
prompts.append("Hello")
prompts.append(f"use this xsd format to generate xml files. {sanitized_xml_data}")
prompts.append(f"generate an xml output to {prompt}")


with model.chat_session():
    for prompt_item in tqdm.tqdm(prompts):
        responses.append(model.generate(prompt_item))

print(f"Generated response: {''.join(responses)}")

modified_output_file_path = r'matt_modified_irq_analysis_lttng.xml'
with open(modified_output_file_path, 'w') as modified_text_file:
    modified_text_file.write(responses[2])

print(f"Modified XML content has been saved to {modified_output_file_path}")