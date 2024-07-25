# from gpt4all import GPT4All
# model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf")

# with model.chat_session():
#     response1 = model.generate(prompt='hello', temp=0)
#     response2 = model.generate(prompt='write a python example of how to parse an event with the field X and Y and generate a plot of x vs y. ignore the timestamps on the events.', temp=0)
#     response3 = model.generate(prompt='thank you', temp=0)
#     print(model.current_chat_session)

from gpt4all import GPT4All

# Load the Mistral 7B model from the local file using GPT4All
model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf")

# Define a simple prompt to test the model
simple_prompt = "What is the capital of India"

# Generate output
response = model.generate(simple_prompt)

# Print the generated response
print(f"Generated response: {response}")
