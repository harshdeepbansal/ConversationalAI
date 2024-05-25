import streamlit as st
import requests
import json
from app1 import getLLamaresponse
from translator import translate_text

BASE_URI = "https://h9455vrz-5000.inc1.devtunnels.ms/"
BEARER_TOKEN = "xxx"  # Replace this with your actual bearer token

def send_request_to_flask(endpoint, data):
    url = f"{BASE_URI}/{endpoint}"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    response = requests.post(url, json=data, headers=headers)
    # st.write("Response Status Code:", response.status_code)
    # st.write("Response Content:", response.text)
    return response.json()

services = {
    
    "Conversation Control and Customization" : "run",

    "Google Analytics Assistant": {
        "endpoint": "/google-apis-experimental/nlp-to-ga/openai/v4",
        "input_fields": ["query", "brand_id", "brand_manager_id"],
    },
    "Google Search Console Assistant": {
        "endpoint": "/google-apis-experimental/nlp-to-gsc/openai/v2",
        "input_fields": ["query", "brand_id", "brand_manager_id"],
    },
    "Google Big Query Assistant": {
        "endpoint": "/google-apis/nlp-to-gbigquery/openai",
        "input_fields": ["query", "brand_id", "brand_manager_id"],
    },
    "Google Ads Assistant": {
        "endpoint": "/google-apis/nlp-to-gads/openai",
        "input_fields": ["query", "brand_id", "brand_manager_id"],
    },
    "SQL Database Assistant": {
        "endpoint": "/google-apis/nlp-to-gbigquery/openai",
        "input_fields": ["query","database_schema", "brand_id", "brand_manager_id"],
    },
    "Postgres Database Assistant": {
        "endpoint": "/google-apis/nlp-to-gbigquery/openai",
        "input_fields": ["query","database_schema", "brand_id", "brand_manager_id"],
    },
    "Excel Sheet Assistant": {
        "endpoint": "/xlsqa/llid/pipeline/conversational/pickle",
        "input_fields": ["query", "brand_id", "brand_manager_id","file_id"],
    },
    "CSV Assistant": {
        "endpoint": "/csvqa/llid/pipeline/conversational/pickle",
        "input_fields": ["query", "brand_id", "brand_manager_id","file_id"],
    },
    "PDF Assistant": {
        "endpoint": "/pdfqa/llid/vector",
        "input_fields": ["query", "brand_id", "brand_manager_id","file_id"],
    }
}

st.sidebar.title("Service Selector")
service_name = st.sidebar.selectbox("Select a service", list(services.keys()))

if service_name:
    if service_name=='Conversation Control and Customization':
        st.header(f"Service: {service_name}")
        if 'summarized_content' not in st.session_state:
            st.session_state.summarized_content = None
        input_text = st.text_area("Enter the Content", placeholder="Paste or type your content here", height=200)
        no_words = st.text_input('Maximum Word Limit for Summary', placeholder="Enter the maximum word limit")
        blog_style = st.selectbox('Summarizing according to', ('Casual', 'Formal'), index=0)
        if st.button("Generate Summary"):
            if input_text.strip() and no_words.isdigit() and int(no_words) > 0:
                summarized_content = getLLamaresponse(input_text, no_words, blog_style)
                if summarized_content:
                    st.session_state.summarized_content = summarized_content  # Set session state
                    st.success("Summary generated successfully!")
                    st.write(summarized_content)
                else:
                    st.warning("Unable to generate summary. Please try again.")
            else:
                st.error("Invalid input. Please provide valid content and word limit.")

        language_mapping = {
            "English": "eng",
            "Hindi": "hin",
            "Urdu": "urd",
            "Punjabi": "pan",
            "Gujarati": "guj",
            "Marathi": "mar",
            "Telugu": "tel",
            "Kannada": "kan",
            "Malayalam": "mal",
            "Tamil": "tam",
            "Odia": "ory",
            "Bengali": "ben",
            "Assamese": "asm",
            "Manipuri": "mni",
            }
            
        if st.session_state.summarized_content:
            selected_input_language_display = st.selectbox('Select Input Language', list(language_mapping.keys()))
            selected_output_language_display = st.selectbox('Select Output Language', list(language_mapping.keys()))
            src_lang = language_mapping[selected_input_language_display]
            tgt_lang = language_mapping[selected_output_language_display]
            
            if st.button("Translate Summary"):
                translated_text = translate_text(st.session_state.summarized_content, src_lang, tgt_lang)
                st.write(st.session_state.summarized_content)
                st.write(translated_text)
    
    else:
        service_details = services[service_name]
        input_fields = service_details["input_fields"]
        endpoint = service_details["endpoint"]

        st.header(f"Service: {service_name}")
        st.subheader("Input Fields")

        input_data = {}
        for field in input_fields:
            input_data[field] = st.text_input(label=field)

        if st.button("Send Request"):
            response = send_request_to_flask(endpoint, input_data)
            if service_name == "Google Analytics Assistant" or service_name== "Google Search Console Assistant":
                st.write(response["data"]["conversation"])
                st.subheader("Response")
                st.json(response['data']['query'])
                
            else:
                st.write(response['data'])
                st.subheader("Response")
                st.json(response)


    