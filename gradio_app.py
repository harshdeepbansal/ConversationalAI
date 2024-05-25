import gradio as gr
import requests

BASE_URI = "http://127.0.0.1:5000"
BEARER_TOKEN = "xxx"  # Replace this with your actual bearer token

def send_request_to_flask(endpoint, data):
    url = f"{BASE_URI}/{endpoint}"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    response = requests.post(url, json=data, headers=headers)
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.text)
    return response.json()

def create_service_ui(service_name, endpoint, input_fields, output_keys):
    input_components = [gr.Textbox(label=label) for label in input_fields]
    output_components = [gr.Textbox(label=key) for key in output_keys]

    def process_input(*args):
        data = {label: arg for label, arg in zip(input_fields, args)}
        response = send_request_to_flask(endpoint, data)
        output_values = {}
        for key in output_keys:
            output_values[key] = response.get(key, "")
        return [output_values[key] for key in output_keys]

    return input_components, output_components, process_input

services = {
    "nlp_to_ga": {
        "endpoint": "/google-apis-experimental/nlp-to-ga/openai/v3",
        "input_fields": ["query", "brand_id", "brand_manager_id"],
        "output_keys": ["data", "type", "validation", "version"]
    },
    "nlp_to_bq 2": {
        "endpoint": "service2",
        "input_fields": ["Input Field 1", "Input Field 2"],
        "output_keys": ["output1", "output2"]
    }
}

interfaces = []
for service_name, service_details in services.items():
    inputs, outputs, fn = create_service_ui(
        service_name, service_details["endpoint"], service_details["input_fields"], service_details["output_keys"]
    )
    interface = gr.Interface(
        fn=fn,
        inputs=inputs,
        outputs=outputs,
        title=service_name
    )
    interfaces.append((service_name, interface))

with gr.Blocks() as demo:
    with gr.Tabs():
        for title, interface in interfaces:
            with gr.TabItem(title):
                interface.render()

demo.launch()