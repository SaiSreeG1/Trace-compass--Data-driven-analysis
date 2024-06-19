
import os
import xml.etree.ElementTree as ET
import json

def parse_xml(file_path):
    """Parse the given XML file and return the root element."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root
    except ET.ParseError as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def extract_data(root, filename):
    """Extract relevant data from the XML root based on specific prompts."""
    data = []

    # Prompt 1: Detailed description for plotting net_dev_queue's len over time
    net_dev_queue_entries = root.findall(".//entry[@path='net_dev_queue/len']")
    if net_dev_queue_entries:
        print(f"Found net_dev_queue entries in {filename}: {len(net_dev_queue_entries)} entries")
        for entry in net_dev_queue_entries:
            prompt = "Plot the value of net_dev_queue's len field in a cumulative way over time."
            response = "Create a line chart to display the cumulative length of net_dev_queue over time. Label the x-axis as 'Time' and the y-axis as 'Queue Length'. The chart should be titled 'Download vs Time'. Plot data points as they accumulate through the time span available in the data set."
            data.append({'prompt': prompt, 'response': response, 'source_file': filename})

    # Prompt 2: Show latencies categorized per CPU
    prompt = "Show me the latencies of sched_waking to sched_wakeup and sched_wakeup to sched_switch, categorized per CPU."
    sched_waking_found = False
    sched_wakeup_found = False
    sched_switch_found = False
    for event in root.findall(".//eventHandler"):
        event_name = event.get('eventName')
        if event_name == 'sched_waking':
            sched_waking_found = True
        if event_name == 'sched_wakeup':
            sched_wakeup_found = True
        if event_name == 'sched_switch':
            sched_switch_found = True

    if sched_waking_found and sched_wakeup_found and sched_switch_found:
        print(f"Found sched_waking, sched_wakeup, and sched_switch events in {filename}")
        response = "Generate a table with columns for CPU ID, Event Type, and Latency. Include rows for each transition between 'sched_waking' and 'sched_wakeup', and 'sched_wakeup' to 'sched_switch', showing the latency for each event."
        data.append({'prompt': prompt, 'response': response, 'source_file': filename})

    # Prompt 3: Show IRQ handler statistics
    irq_handler_entry_found = False
    irq_softirq_raise_found = False
    irq_handler_exit_found = False
    irq_softirq_entry_found = False
    irq_softirq_exit_found = False

    for action in root.findall(".//action"):
        action_id = action.get('id')
        if action_id == 'irq_handler_entry':
            irq_handler_entry_found = True
        if action_id == 'irq_softirq_raise':
            irq_softirq_raise_found = True
        if action_id == 'irq_handler_exit':
            irq_handler_exit_found = True
        if action_id == 'irq_softirq_entry':
            irq_softirq_entry_found = True
        if action_id == 'irq_softirq_exit':
            irq_softirq_exit_found = True

    if irq_handler_entry_found and irq_softirq_raise_found and irq_handler_exit_found and irq_softirq_entry_found and irq_softirq_exit_found:
        print(f"Found IRQ handler events in {filename}")
        prompt = "Show me the statistics of irq_handler_entry -> irq_softirq_raise -> irq_handler_exit -> irq_softirq_entry -> irq_softirq_exit."
        response = "Generate a sequential diagram or flowchart showing each stage of the IRQ handler process from entry to exit. Include timestamps, durations, and any relevant flags or interrupts. This should visually represent the sequence flow and include any conditional branches based on IRQ values."
        data.append({'prompt': prompt, 'response': response, 'source_file': filename})

    return data

def process_xml_files(directory):
    """Process all XML files in the specified directory to create a training dataset."""
    all_data = []
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            file_path = os.path.join(directory, filename)
            root = parse_xml(file_path)
            if root is not None:
                data = extract_data(root, filename)
                if data:
                    all_data.extend(data)
    return all_data

def main():
    directory = r'C:\Users\egsuaid\OneDrive - Ericsson\Documents\XML files'
    all_data = process_xml_files(directory)
    
    # Save the extracted data to a JSON file for further use in machine learning tasks
    with open('dataset_for_finetuning.json', 'w') as f:
        json.dump(all_data, f, indent=4)

    print("Data extraction complete. Dataset saved to 'dataset_for_finetuning.json'.")

if __name__ == "__main__":
    main()
