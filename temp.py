import gradio as gr
import requests

# Updated Server URL
SERVER_URL = "http://0.0.0.0:30000/generate"

# Function to interact with the LLM server
def query_model(prompt, max_new_tokens, temperature):
    try:
        # Define the payload
        payload = {
            "text": prompt,
            "sampling_params": {
                "max_new_tokens": max_new_tokens,
                "temperature": temperature
            }
        }
        
        # Send POST request to the LLM server
        response = requests.post(SERVER_URL, json=payload)
        
        # Check response status
        if response.status_code == 200:
            # Parse and return the generated text
            output = response.json()
            return output.get("generated_text", "No response text received.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Exception occurred: {str(e)}"

# Create Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# LLM Text Generation with SaulLM")
    with gr.Row():
        with gr.Column():
            user_input = gr.Textbox(label="Enter your prompt here", lines=5, placeholder="Type your question or input...")
            max_new_tokens = gr.Slider(label="Max New Tokens", minimum=1, maximum=512, step=1, value=16)
            temperature = gr.Slider(label="Temperature", minimum=0.0, maximum=1.0, step=0.1, value=0.7)
        with gr.Column():
            output_text = gr.Textbox(label="Generated Output", lines=10, interactive=False)
    submit_button = gr.Button("Generate")
    submit_button.click(query_model, inputs=[user_input, max_new_tokens, temperature], outputs=output_text)

# Launch the Gradio app
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860,share=True)
