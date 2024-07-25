from gpt4all import GPT4All
import re
import tqdm

# Initialize the GPT4All model
model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf", device='cpu')

# Function to sanitize XML data by removing comments and special characters
def sanitize_xml(xml_data):
    xml_data = re.sub(r'<!--.*?-->', '', xml_data, flags=re.DOTALL)
    xml_data = re.sub(r'\s+', ' ', xml_data)
    return xml_data

# Few-shot examples
example_1_prompt = "Plot the number of times a user id failed to connect vs time."
example_1_response = sanitize_xml("""
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
""")

example_2_prompt = "Show me the irqs vs time where you store the irq name it should be categorized by a tid."
example_2_response = sanitize_xml("""
<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <!-- Timegraph view that show the scenario execution state in time -->
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
""")

example_3_prompt = "Given the state system 'org.eclipse.tracecompass...', plot the user bandwidth, it is every attribute under the user/* branch."
example_3_response = sanitize_xml("""
<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="../../org.eclipse.tracecompass.tmf.analysis.xml.core/src/org/eclipse/tracecompass/tmf/analysis/xml/core/module/xmlDefinition.xsd">
    <xyView id="endpoint.bandwidth">
        <head>
            <analysis id="org.eclipse.tracecompass.incubator.internal.system.core.analsysis.httpd.HttpdConnectionAnalysis" />
            <label value="Endpoint Bandwidth" />
        </head>
        <entry path="endpoint/*"
               displayType="delta">
            <display type="self" />
        </entry>
    </xyView>
    <xyView id="ip.bandwidth">
        <head>
            <analysis id="org.eclipse.tracecompass.incubator.internal.system.core.analsysis.httpd.HttpdConnectionAnalysis" />
            <label value="IP Bandwidth" />
        </head>
        <entry path="ip/*"
               displayType="delta">
            <display type="self" />
        </entry>
    </xyView>
    <xyView id="user.bandwidth">
        <head>
            <analysis id="org.eclipse.tracecompass.incubator.internal.system.core.analsysis.httpd.HttpdConnectionAnalysis" />
            <label value="User Bandwidth" />
        </head>
        <entry path="user/*"
               displayType="delta">
            <display type="self" />
        </entry>
    </xyView>
</tmfxml>
""")
example_4_prompt = "Give me statistics on GC durations using the field 'Pause' and classify by type."
example_4_response = sanitize_xml("""
<tmfxml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="xmlDefinition.xsd">
    <!-- *************************************************************************** 
		* Copyright (c) 2024 Ericsson * * All rights reserved. This program and the 
		accompanying materials are * made available under the terms of the Eclipse 
		Public License 2.0 which * accompanies this distribution, and is available 
		at * https://www.eclipse.org/legal/epl-2.0/ * * SPDX-License-Identifier: 
		EPL-2.0 *************************************************************************** -->
    <pattern version="1"
             id="system.gc.duration">
        <head>
            <label value="GC Segments" />
        </head>
        <patternHandler>
            <action id="segment_create">
                <segment>
                    <segType>
                        <segName>
                            <stateValue type="eventField"
                                        value="Cause" />
                        </segName>
                    </segType>
                    <segTime>
                        <begin type="eventField"
                               value="timestamp" />
                        <duration type="eventField"
                                  value="Pause" />
                    </segTime>
                </segment>
            </action>
            <fsm id="gcs"
                 multiple="true">
                <state id="start">
                    <transition event="*"
                                target="duration"
                                action="segment_create" />
                </state>
                <final id="duration" />
            </fsm>
        </patternHandler>
    </pattern>
</tmfxml>
""")

# Define your few-shot prompt with the examples and the task prompt
few_shot_prompt = f"""
{example_1_prompt}
{example_1_response}

{example_2_prompt}
{example_2_response}

{example_3_prompt}
{example_3_response}

{example_4_prompt}
{example_4_response}

Now, using the above examples, respond to the following prompt:

Give me statistics on GC durations using the field 'Pause' and classify by type.
"""

# Generate the response
responses = []
prompts = [few_shot_prompt]

with model.chat_session():
    for prompt_item in tqdm.tqdm(prompts):
        responses.append(model.generate(prompt_item))

# Print the generated response
print(f"Generated response: {''.join(responses)}")

# Save the modified XML content to a new file
modified_output_file_path = r'fewshot.xml'
with open(modified_output_file_path, 'w') as modified_text_file:
    modified_text_file.write(responses[0])

print(f"Modified XML content has been saved to {modified_output_file_path}")

