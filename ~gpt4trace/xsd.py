def explain_tags():
    explanation = """
    <TraceAnalysis>: The root element for the trace analysis configuration.
    <Configuration>: Contains the event configuration.
    <Event name="irq_handler_entry">: Defines an event named "irq_handler_entry".
    <Field name="timestamp">: Specifies a field for the event's timestamp.
    <Field name="irq">: Specifies a field for the event's IRQ.
    <Field name="tid">: Specifies a field for the event's TID.
    <Plot>: Configuration for the plot.
    <Type>irqs_vs_time</Type>: Type of the plot, in this case, IRQs vs Time.
    <XAxis>timestamp</XAxis>: X-axis of the plot, representing timestamps.
    <YAxis>irq</YAxis>: Y-axis of the plot, representing IRQs.
    <Category>tid</Category>: Category to differentiate IRQs by TID.
    """
    print("Tag Explanations:\n", explanation)

explain_tags()
example_xml = '''
<TraceAnalysis>
    <Configuration>
        <Event name="irq_handler_entry">
            <Field name="timestamp" />
            <Field name="irq" />
            <Field name="tid" />
        </Event>
    </Configuration>
    <Plot>
        <Type>irqs_vs_time</Type>
        <XAxis>timestamp</XAxis>
        <YAxis>irq</YAxis>
        <Category>tid</Category>
    </Plot>
</TraceAnalysis>
'''
print("Example XML:\n", example_xml)
from gpt4all import GPT4All
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

# Initialize the GPT4All model
model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf")

# Define the prompt for the AI model with a structured request for XML
prompt = """
Generate an XML configuration to plot IRQs over time, categorized by TID. 
The XML should define events named "irq_handler_entry" with fields for timestamp, irq, and tid.
It should look like this:

<TraceAnalysis>
    <Configuration>
        <Event name="irq_handler_entry">
            <Field name="timestamp" />
            <Field name="irq" />
            <Field name="tid" />
        </Event>
    </Configuration>
    <Plot>
        <Type>irqs_vs_time</Type>
        <XAxis>timestamp</XAxis>
        <YAxis>irq</YAxis>
        <Category>tid</Category>
    </Plot>
</TraceAnalysis>
"""

# Generate XML response using the AI model
with model.chat_session():
    response = model.generate(prompt=prompt, temp=0)
    xml_response = response  # Directly use response as a string

# Validate if the response is valid XML
try:
    root = ET.fromstring(xml_response)
    print("Generated XML:\n", xml_response)
except ET.ParseError as e:
    print("The generated response is not valid XML.")
    print("Error:", e)
    exit()

# Initialize lists to store data
timestamps = []
irqs = []
tids = []

# Extract data from the XML
for event in root.findall('.//Event'):
    if event.attrib.get('name') == 'irq_handler_entry':
        timestamp = event.find('.//Field[@name="timestamp"]').text
        irq = event.find('.//Field[@name="irq"]').text
        tid = event.find('.//Field[@name="tid"]').text
        timestamps.append(timestamp)
        irqs.append(irq)
        tids.append(tid)

# Convert timestamps to floats (assuming they are strings)
timestamps = [float(ts) for ts in timestamps]

# Create a plot
fig, ax = plt.subplots()
scatter = ax.scatter(timestamps, irqs, c=tids, cmap='viridis')

# Add labels and title
ax.set_xlabel('Time')
ax.set_ylabel('IRQ')
ax.set_title('IRQs over Time Categorized by TID')
legend = ax.legend(*scatter.legend_elements(), title="TID")
ax.add_artist(legend)

# Show the plot
plt.show()
skeleton_template = '''<TraceAnalysis xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="trace_analysis.xsd">
    <Configuration>
        <Event name="event_name">
            <Field name="timestamp" />
            <Field name="irq" />
            <Field name="tid" />
            <!-- Add more fields as necessary -->
        </Event>
    </Configuration>
    <Plot>
        <Type>plot_type</Type>
        <XAxis>x_axis_field</XAxis>
        <YAxis>y_axis_field</YAxis>
        <Category>category_field</Category>
    </Plot>
</TraceAnalysis>'''

print("Skeleton Template:\n", skeleton_template)
def create_prompt(human_text):
    prompt = f"""
    Generate an XML configuration to {human_text}. 
    The XML should define events named "irq_handler_entry" with fields for timestamp, irq, and tid.
    It should look like this:

    <TraceAnalysis>
        <Configuration>
            <Event name="irq_handler_entry">
                <Field name="timestamp" />
                <Field name="irq" />
                <Field name="tid" />
            </Event>
        </Configuration>
        <Plot>
            <Type>irqs_vs_time</Type>
            <XAxis>timestamp</XAxis>
            <YAxis>irq</YAxis>
            <Category>tid</Category>
        </Plot>
    </TraceAnalysis>
    """
    return prompt

human_text = "plot IRQs over time, categorized by TID"
prompt = create_prompt(human_text)
print("Generated Prompt:\n", prompt)
