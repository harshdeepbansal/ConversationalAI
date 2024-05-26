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

    "Select Services" : 'run',
    
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
                st.subheader("Summarized Content")
                st.write(st.session_state.summarized_content)
                st.subheader("Translated Summary")
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



# **************************************---------------------***************************************************************************


# import streamlit as st
# import requests
# import json
# from app1 import getLLamaresponse
# from translator import translate_text

# BASE_URI = "https://h9455vrz-5000.inc1.devtunnels.ms/"
# BEARER_TOKEN = "xxx"  # Replace this with your actual bearer token

# def send_request_to_flask(endpoint, data):
#     url = f"{BASE_URI}/{endpoint}"
#     headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
#     response = requests.post(url, json=data, headers=headers)
#     return response.json()

# services = {
#     "Conversation Control and Customization": "run",
#     "Google Analytics Assistant": {
#         "endpoint": "/google-apis-experimental/nlp-to-ga/openai/v4",
#         "input_fields": ["query", "brand_id", "brand_manager_id"],
#     },
#     "Google Search Console Assistant": {
#         "endpoint": "/google-apis-experimental/nlp-to-gsc/openai/v2",
#         "input_fields": ["query", "brand_id", "brand_manager_id"],
#     },
#     "Google Big Query Assistant": {
#         "endpoint": "/google-apis/nlp-to-gbigquery/openai",
#         "input_fields": ["query", "brand_id", "brand_manager_id"],
#     },
#     "Google Ads Assistant": {
#         "endpoint": "/google-apis/nlp-to-gads/openai",
#         "input_fields": ["query", "brand_id", "brand_manager_id"],
#     },
#     "SQL Database Assistant": {
#         "endpoint": "/google-apis/nlp-to-gbigquery/openai",
#         "input_fields": ["query","database_schema", "brand_id", "brand_manager_id"],
#     },
#     "Postgres Database Assistant": {
#         "endpoint": "/google-apis/nlp-to-gbigquery/openai",
#         "input_fields": ["query","database_schema", "brand_id", "brand_manager_id"],
#     },
#     "Excel Sheet Assistant": {
#         "endpoint": "/xlsqa/llid/pipeline/conversational/pickle",
#         "input_fields": ["query", "brand_id", "brand_manager_id","file_id"],
#     },
#     "CSV Assistant": {
#         "endpoint": "/csvqa/llid/pipeline/conversational/pickle",
#         "input_fields": ["query", "brand_id", "brand_manager_id","file_id"],
#     },
#     "PDF Assistant": {
#         "endpoint": "/pdfqa/llid/vector",
#         "input_fields": ["query", "brand_id", "brand_manager_id","file_id"],
#     }
# }

# # Set page configuration to collapse sidebar by default
# st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="NLP Services", page_icon="🤖")

# # Custom CSS to style the sidebar buttons
# st.markdown("""
#     <style>
#     .sidebar .sidebar-content {
#         background-color: #f0f2f6;
#         padding: 10px;
#         display: flex;
#         flex-direction: column;
#         justify-content: center;
#         align-items: center;
#         height: 100vh;
#     }
#     .sidebar .stButton > button {
#         width: 90%;
#         height: 50px;
#         margin-bottom: 10px;
#         background-color: #4CAF50;
#         color: white;
#         border: none;
#         text-align: center;
#         font-size: 16px;
#         cursor: pointer;
#     }
#     .sidebar .stButton > button:hover {
#         background-color: #45a049;
#     }
#     .main-header {
#         text-align: center;
#         color: #4CAF50;
#     }
#     .css-1aumxhk {
#         justify-content: center !important;
#         align-items: center !important;
#     }
#     </style>
# """, unsafe_allow_html=True)

# st.sidebar.title("Service Selector")

# # Initialize session state for selected service
# if 'selected_service' not in st.session_state:
#     st.session_state.selected_service = None

# # Create buttons for each service in a centered manner
# for service in services.keys():
#     if st.sidebar.button(service):
#         st.session_state.selected_service = service

# # If no service is selected, display welcome message
# if not st.session_state.selected_service:
#     st.markdown("<h1 class='main-header'>Welcome to Our NLP Services 🤖</h1>", unsafe_allow_html=True)
# else:
#     service_name = st.session_state.selected_service
#     if service_name == 'Conversation Control and Customization':
#         st.header(f"Service: {service_name}")
#         if 'summarized_content' not in st.session_state:
#             st.session_state.summarized_content = None
#         input_text = st.text_area("Enter the Content", placeholder="Paste or type your content here", height=200)
#         no_words = st.text_input('Maximum Word Limit for Summary', placeholder="Enter the maximum word limit")
#         blog_style = st.selectbox('Summarizing according to', ('Casual', 'Formal'), index=0)
#         if st.button("Generate Summary"):
#             if input_text.strip() and no_words.isdigit() and int(no_words) > 0:
#                 summarized_content = getLLamaresponse(input_text, no_words, blog_style)
#                 if summarized_content:
#                     st.session_state.summarized_content = summarized_content  # Set session state
#                     st.success("Summary generated successfully!")
#                     st.write(summarized_content)
#                 else:
#                     st.warning("Unable to generate summary. Please try again.")
#             else:
#                 st.error("Invalid input. Please provide valid content and word limit.")

#         language_mapping = {
#             "English": "eng",
#             "Hindi": "hin",
#             "Urdu": "urd",
#             "Punjabi": "pan",
#             "Gujarati": "guj",
#             "Marathi": "mar",
#             "Telugu": "tel",
#             "Kannada": "kan",
#             "Malayalam": "mal",
#             "Tamil": "tam",
#             "Odia": "ory",
#             "Bengali": "ben",
#             "Assamese": "asm",
#             "Manipuri": "mni",
#         }
        
#         if st.session_state.summarized_content:
#             selected_input_language_display = st.selectbox('Select Input Language', list(language_mapping.keys()))
#             selected_output_language_display = st.selectbox('Select Output Language', list(language_mapping.keys()))
#             src_lang = language_mapping[selected_input_language_display]
#             tgt_lang = language_mapping[selected_output_language_display]
            
#             if st.button("Translate Summary"):
#                 translated_text = translate_text(st.session_state.summarized_content, src_lang, tgt_lang)
#                 st.subheader("Summarized Content")
#                 st.write(st.session_state.summarized_content)
#                 st.subheader("Translated Summary")
#                 st.write(translated_text)
#     else:
#         service_details = services[service_name]
#         input_fields = service_details["input_fields"]
#         endpoint = service_details["endpoint"]

#         st.header(f"Service: {service_name}")
#         st.subheader("Input Fields")

#         input_data = {}
#         for field in input_fields:
#             input_data[field] = st.text_input(label=field)

#         if st.button("Send Request"):
#             response = send_request_to_flask(endpoint, input_data)
#             if service_name == "Google Analytics Assistant" or service_name == "Google Search Console Assistant":
#                 st.write(response["data"]["conversation"])
#                 st.subheader("Response")
#                 st.json(response['data']['query'])
#             else:
#                 st.write(response['data'])
#                 st.subheader("Response")
#                 st.json(response)



#*****************************************************************************************************************************----*


# import streamlit as st
# import requests
# import json
# from app1 import getLLamaresponse
# from translator import translate_text

# BASE_URI = "https://h9455vrz-5000.inc1.devtunnels.ms/"
# BEARER_TOKEN = "xxx"  # Replace this with your actual bearer token

# def send_request_to_flask(endpoint, data):
#     url = f"{BASE_URI}/{endpoint}"
#     headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
#     response = requests.post(url, json=data, headers=headers)
#     return response.json()

# def upload_file_to_flask(endpoint, files, data):
#     url = f"{BASE_URI}/{endpoint}"
#     headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
#     response = requests.post(url, files=files, data=data, headers=headers)
#     st.write("Response Status Code:", response.status_code)
#     st.write("Response Content:", response.text)
#     return response.json()

# services = {
#     "Conversation Control and Customization" : "run",
#     "Google Analytics Assistant": {
#         "endpoint": "/google-apis-experimental/nlp-to-ga/openai/v4",
#         "input_fields": ["query", "brand_id", "brand_manager_id"],
#     },
#     "Google Search Console Assistant": {
#         "endpoint": "/google-apis-experimental/nlp-to-gsc/openai/v1",
#         "input_fields": ["query", "brand_id", "brand_manager_id"],
#     },
#     "Google Big Query Assistant": {
#         "endpoint": "/google-apis/nlp-to-gbigquery/openai",
#         "input_fields": ["query", "brand_id", "brand_manager_id"],
#     },
#     "Google Ads Assistant": {
#         "endpoint": "/google-apis/nlp-to-gads/openai",
#         "input_fields": ["query", "brand_id", "brand_manager_id"],
#     },
#     "SQL Database Assistant": {
#         "endpoint": "/google-apis/nlp-to-gbigquery/openai",
#         "input_fields": ["query", "database_schema", "brand_id", "brand_manager_id"],
#     },
#     "Postgres Database Assistant": {
#         "endpoint": "/google-apis/nlp-to-gbigquery/openai",
#         "input_fields": ["query", "database_schema", "brand_id", "brand_manager_id"],
#     },
#     "Excel Sheet Assistant": {
#         "endpoint": "/xlsqa/llid/pipeline/conversational/pickle",
#         "input_fields": ["query", "brand_id", "brand_manager_id", "file_id"],
#     },
#     "CSV Assistant": {
#         "endpoint": "/csvqa/llid/pipeline/conversational/pickle",
#         "input_fields": ["query", "brand_id", "brand_manager_id", "file_id"],
#     },
#     "PDF Assistant": {
#         "endpoint": "/pdfqa/llid/vector",
#         "input_fields": ["query", "brand_id", "brand_manager_id", "file_id"],
#     },
#     "Media Upload": {
#         "endpoint": "/upload/local-media",
#         "input_fields": ["brand_id", "brand_manager_id", "vector_storage", "pickle_storage"]
#     }
# }

# # Set page configuration to collapse sidebar by default
# st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="NLP Services", page_icon="🤖")

# # Custom CSS to style the sidebar buttons
# st.markdown("""
#     <style>
#     .sidebar .sidebar-content {
#         background-color: #f0f2f6;
#         padding: 10px;
#         display: flex;
#         flex-direction: column;
#         justify-content: center;
#         align-items: center;
#         height: 100vh;
#     }
#     .sidebar .stButton > button {
#         width: 90%;
#         height: 50px;
#         margin-bottom: 10px;
#         background-color: #4CAF50;
#         color: white;
#         border: none;
#         text-align: center;
#         font-size: 16px;
#         cursor: pointer;
#     }
#     .sidebar .stButton > button:hover {
#         background-color: #45a049;
#     }
#     .main-header {
#         text-align: center;
#         color: #4CAF50;
#     }
#     .css-1aumxhk {
#         justify-content: center !important;
#         align-items: center !important;
#     }
#     </style>
# """, unsafe_allow_html=True)

# st.sidebar.title("Service Selector")

# # Initialize session state for selected service
# if 'selected_service' not in st.session_state:
#     st.session_state.selected_service = None

# # Create buttons for each service in a centered manner
# for service in services.keys():
#     if st.sidebar.button(service):
#         st.session_state.selected_service = service

# # If no service is selected, display welcome message
# if not st.session_state.selected_service:
#     st.markdown("<h1 class='main-header'>Welcome to Our NLP Services 🤖</h1>", unsafe_allow_html=True)
# else:
#     service_name = st.session_state.selected_service
#     if service_name == 'Conversation Control and Customization':
#         st.header(f"Service: {service_name}")
#         if 'summarized_content' not in st.session_state:
#             st.session_state.summarized_content = None
#         input_text = st.text_area("Enter the Content", placeholder="Paste or type your content here", height=200)
#         no_words = st.text_input('Maximum Word Limit for Summary', placeholder="Enter the maximum word limit")
#         blog_style = st.selectbox('Summarizing according to', ('Casual', 'Formal'), index=0)
#         if st.button("Generate Summary"):
#             if input_text.strip() and no_words.isdigit() and int(no_words) > 0:
#                 summarized_content = getLLamaresponse(input_text, no_words, blog_style)
#                 if summarized_content:
#                     st.session_state.summarized_content = summarized_content  # Set session state
#                     st.success("Summary generated successfully!")
#                     st.write(summarized_content)
#                 else:
#                     st.warning("Unable to generate summary. Please try again.")
#             else:
#                 st.error("Invalid input. Please provide valid content and word limit.")

#         language_mapping = {
#             "English": "eng",
#             "Hindi": "hin",
#             "Urdu": "urd",
#             "Punjabi": "pan",
#             "Gujarati": "guj",
#             "Marathi": "mar",
#             "Telugu": "tel",
#             "Kannada": "kan",
#             "Malayalam": "mal",
#             "Tamil": "tam",
#             "Odia": "ory",
#             "Bengali": "ben",
#             "Assamese": "asm",
#             "Manipuri": "mni",
#         }
        
#         if st.session_state.summarized_content:
#             selected_input_language_display = st.selectbox('Select Input Language', list(language_mapping.keys()))
#             selected_output_language_display = st.selectbox('Select Output Language', list(language_mapping.keys()))
#             src_lang = language_mapping[selected_input_language_display]
#             tgt_lang = language_mapping[selected_output_language_display]
            
#             if st.button("Translate Summary"):
#                 translated_text = translate_text(st.session_state.summarized_content, src_lang, tgt_lang)
#                 st.subheader("Summarized Content")
#                 st.write(st.session_state.summarized_content)
#                 st.subheader("Translated Summary")
#                 st.write(translated_text)

#     elif service_name=='Media Upload':
#         service_details = services[service_name]
#         input_fields = service_details["input_fields"]
#         endpoint = service_details["endpoint"]

#         st.header(f"Service: {service_name}")
#         st.subheader("Input Fields")

#         input_data = {}

#         uploaded_file = st.file_uploader("Choose a file", type=["png", "jpg", "jpeg", "mp4", "mp3", "pdf", "csv", "xls"])
#         for field in input_fields:
#             if field in ["vector_storage", "pickle_storage"]:
#                 input_data[field] = st.checkbox(field.capitalize())
#             else:
#                 input_data[field] = st.text_input(label=field)

#         if st.button("Upload"):
#             if uploaded_file is not None and input_data["brand_id"] and input_data["brand_manager_id"]:
#                 files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
#                 data = {
#                     "brand_id": input_data["brand_id"],
#                     "brand_manager_id": input_data["brand_manager_id"],
#                     "vector_storage": str(input_data["vector_storage"]).lower(),
#                     "pickle_storage": str(input_data["pickle_storage"]).lower()
#                 }
#                 response = upload_file_to_flask(endpoint, files, data)
#                 if response and "file_name" in response:
#                     st.success(f"File uploaded successfully: {response['file_name']}")
#                 else:
#                     st.error("Failed to upload file.")
#             else:
#                 st.error("Please fill in all required fields and select a file.")

#     else:
#         service_details = services[service_name]
#         input_fields = service_details["input_fields"]
#         endpoint = service_details["endpoint"]

#         st.header(f"Service: {service_name}")
#         st.subheader("Input Fields")

#         input_data = {}
#         for field in input_fields:
#             input_data[field] = st.text_input(label=field)

#         if st.button("Send Request"):
#             response = send_request_to_flask(endpoint, input_data)
#             if service_name == "Google Analytics Assistant" or service_name == "Google Search Console Assistant":
#                 st.write(response["data"]["conversation"])
#                 st.subheader("Response")
#                 st.json(response['data']['query'])
#             else:
#                 st.write(response['data'])
#                 st.subheader("Response")
#                 st.json(response)



#-------------------------------------------------------------------------------------------------------------------------------------------------

# import streamlit as st
# import requests
# import json
# from app1 import getLLamaresponse
# from translator import translate_text

# BASE_URI = "https://h9455vrz-5000.inc1.devtunnels.ms/"
# BEARER_TOKEN = "xxx"  # Replace this with your actual bearer token

# def send_request_to_flask(endpoint, data):
#     url = f"{BASE_URI}/{endpoint}"
#     headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
#     response = requests.post(url, json=data, headers=headers)
    
#     if response.status_code == 200:
#         try:
#             json_response = response.json()
#             return json_response
#         except json.JSONDecodeError:
#             st.error("Failed to decode JSON response.")
#             st.write("Raw Response Content:", response.text)
#             return None
#     else:
#         st.error(f"Request failed with status code: {response.status_code}")
#         st.write("Raw Response Content:", response.text)
#         return None

# def upload_file_to_flask(endpoint, files, data):
#     url = f"{BASE_URI}/{endpoint}"
#     headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
#     response = requests.post(url, files=files, data=data, headers=headers)
#     st.write("Response Status Code:", response.status_code)
#     st.write("Response Content:", response.text)
#     try:
#         json_response = response.json()
#         st.write("Response Content:", json_response)
#         return json_response
#     except json.JSONDecodeError:
#         st.error("Failed to decode JSON response.")
#         st.write("Raw Response Content:", response.text)
#         return None

# services = {
#     "Conversation Control and Customization" : "run",
#     "Google Analytics Assistant": {
#         "endpoint": "/google-apis-experimental/nlp-to-ga/openai/v4",
#         "input_fields": ["query", "brand_id", "brand_manager_id"],
#     },
#     "Google Search Console Assistant": {
#         "endpoint": "/google-apis-experimental/nlp-to-gsc/openai/v1",
#         "input_fields": ["query", "brand_id", "brand_manager_id"],
#     },
#     "Google Big Query Assistant": {
#         "endpoint": "/google-apis/nlp-to-gbigquery/openai",
#         "input_fields": ["query", "brand_id", "brand_manager_id"],
#     },
#     "Google Ads Assistant": {
#         "endpoint": "/google-apis/nlp-to-gads/openai",
#         "input_fields": ["query", "brand_id", "brand_manager_id"],
#     },
#     "SQL Database Assistant": {
#         "endpoint": "/google-apis/nlp-to-gbigquery/openai",
#         "input_fields": ["query", "database_schema", "brand_id", "brand_manager_id"],
#     },
#     "Postgres Database Assistant": {
#         "endpoint": "/google-apis/nlp-to-gbigquery/openai",
#         "input_fields": ["query", "database_schema", "brand_id", "brand_manager_id"],
#     },
#     "Excel Sheet Assistant": {
#         "endpoint": "/xlsqa/llid/pipeline/conversational/pickle",
#         "input_fields": ["query", "brand_id", "brand_manager_id", "file_id"],
#     },
#     "CSV Assistant": {
#         "endpoint": "/csvqa/llid/pipeline/conversational",
#         "input_fields": ["query", "brand_id", "brand_manager_id", "file_id"],
#     },
#     "PDF Assistant": {
#         "endpoint": "/pdfqa/llid/vector",
#         "input_fields": ["query", "brand_id", "brand_manager_id", "file_id"],
#     },
#     "Media Upload": {
#         "endpoint": "/upload/local-media",
#         "input_fields": ["brand_id", "brand_manager_id", "vector_storage", "pickle_storage"]
#     }
# }

# # Set page configuration to collapse sidebar by default
# st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="NLP Services", page_icon="🤖")

# # Custom CSS to style the sidebar buttons
# st.markdown(
#     """
#     <style>
#     .sidebar .sidebar-content {
#         background-color: #f0f2f6;
#         padding: 10px;
#         display: flex;
#         flex-direction: column;
#         align-items: center;
#     }
#     .stButton > button {
#         width: 100%;
#         height: 50px;
#         margin-bottom: 10px;
#         background-color: #ADD8E6; /* Light blue color */
#         color: white;
#         border: none;
#         text-align: center;
#         font-size: 16px;
#         cursor: pointer;
#     }
#     .stButton > button:hover {
#         color: #00008B; /* Darker blue text color on hover */
#     }
#     .main-header {
#         text-align: center;
#         color: #4CAF50;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# st.sidebar.title("Service Selector")

# # Initialize session state for selected service
# if 'selected_service' not in st.session_state:
#     st.session_state.selected_service = None

# # Create buttons for each service in a centered manner
# for service in services.keys():
#     if st.sidebar.button(service):
#         st.session_state.selected_service = service

# # If no service is selected, display welcome message
# if not st.session_state.selected_service:
#     st.markdown("<h1 class='main-header'>Welcome to Our NLP Services 🤖</h1>", unsafe_allow_html=True)
# else:
#     service_name = st.session_state.selected_service
#     if service_name == 'Conversation Control and Customization':
#         st.header(f"Service: {service_name}")
#         if 'summarized_content' not in st.session_state:
#             st.session_state.summarized_content = None
#         input_text = st.text_area("Enter the Content", placeholder="Paste or type your content here", height=200)
#         no_words = st.text_input('Maximum Word Limit for Summary', placeholder="Enter the maximum word limit")
#         blog_style = st.selectbox('Summarizing according to', ('Casual', 'Formal'), index=0)
#         if st.button("Generate Summary"):
#             if input_text.strip() and no_words.isdigit() and int(no_words) > 0:
#                 summarized_content = getLLamaresponse(input_text, no_words, blog_style)
#                 if summarized_content:
#                     st.session_state.summarized_content = summarized_content  # Set session state
#                     st.success("Summary generated successfully!")
#                     st.write(summarized_content)
#                 else:
#                     st.warning("Unable to generate summary. Please try again.")
#             else:
#                 st.error("Invalid input. Please provide valid content and word limit.")

#         language_mapping = {
#             "English": "eng",
#             "Hindi": "hin",
#             "Urdu": "urd",
#             "Punjabi": "pan",
#             "Gujarati": "guj",
#             "Marathi": "mar",
#             "Telugu": "tel",
#             "Kannada": "kan",
#             "Malayalam": "mal",
#             "Tamil": "tam",
#             "Odia": "ory",
#             "Bengali": "ben",
#             "Assamese": "asm",
#             "Manipuri": "mni",
#         }
        
#         if st.session_state.summarized_content:
#             selected_input_language_display = st.selectbox('Select Input Language', list(language_mapping.keys()))
#             selected_output_language_display = st.selectbox('Select Output Language', list(language_mapping.keys()))
#             src_lang = language_mapping[selected_input_language_display]
#             tgt_lang = language_mapping[selected_output_language_display]
            
#             if st.button("Translate Summary"):
#                 translated_text = translate_text(st.session_state.summarized_content, src_lang, tgt_lang)
#                 st.subheader("Summarized Content")
#                 st.write(st.session_state.summarized_content)
#                 st.subheader("Translated Summary")
#                 st.write(translated_text)

#     elif service_name=='Media Upload':
#         service_details = services[service_name]
#         input_fields = service_details["input_fields"]
#         endpoint = service_details["endpoint"]

#         st.header(f"Service: {service_name}")
#         st.subheader("Input Fields")

#         input_data = {}

#         uploaded_file = st.file_uploader("Choose a file", type=["png", "jpg", "jpeg", "mp4", "mp3", "pdf", "csv", "xls"])
#         for field in input_fields:
#             if field in ["vector_storage", "pickle_storage"]:
#                 input_data[field] = st.checkbox(field.capitalize())
#             else:
#                 input_data[field] = st.text_input(label=field)

#         if st.button("Upload"):
#             if uploaded_file is not None and input_data["brand_id"] and input_data["brand_manager_id"]:
#                 files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
#                 data = {
#                     "brand_id": input_data["brand_id"],
#                     "brand_manager_id": input_data["brand_manager_id"],
#                     "vector_storage": str(input_data["vector_storage"]).lower(),
#                     "pickle_storage": str(input_data["pickle_storage"]).lower()
#                 }
#                 response = upload_file_to_flask(endpoint, files, data)
#                 if response and "file_name" in response:
#                     st.success(f"File uploaded successfully: {response['file_name']}")
#                 else:
#                     st.error("Failed to upload file.")
#             else:
#                 st.error("Please fill in all required fields and select a file.")

#     else:
#         service_details = services[service_name]
#         input_fields = service_details["input_fields"]
#         endpoint = service_details["endpoint"]

#         st.header(f"Service: {service_name}")
#         st.subheader("Input Fields")

#         input_data = {}
#         for field in input_fields:
#             input_data[field] = st.text_input(label=field)

#         if st.button("Send Request"):
#             response = send_request_to_flask(endpoint, input_data)
#             if service_name == "Google Analytics Assistant" or service_name == "Google Search Console Assistant":
#                 st.write(response["data"])
#                 st.subheader("Response")
#                 st.json(response)
#             else:
#                 st.subheader("Response")
#                 st.write(response)



#******************************************************************------------------------------------*******************


# import streamlit as st
# import requests
# import json
# from app1 import getLLamaresponse
# from translator import translate_text

# BASE_URI = "https://h9455vrz-5000.inc1.devtunnels.ms/"
# BEARER_TOKEN = "xxx"  # Replace this with your actual bearer token

# def send_request_to_flask(endpoint, data):
#     url = f"{BASE_URI}/{endpoint}"
#     headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
#     response = requests.post(url, json=data, headers=headers)
    
#     if response.status_code == 200:
#         try:
#             json_response = response.json()
#             return json_response
#         except json.JSONDecodeError:
#             st.error("Failed to decode JSON response.")
#             st.write("Raw Response Content:", response.text)
#             return None
#     else:
#         st.error(f"Request failed with status code: {response.status_code}")
#         st.write("Raw Response Content:", response.text)
#         return None

# def upload_file_to_flask(endpoint, files, data):
#     url = f"{BASE_URI}/{endpoint}"
#     headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
#     response = requests.post(url, files=files, data=data, headers=headers)
#     st.write("Response Status Code:", response.status_code)
#     st.write("Response Content:", response.text)
#     try:
#         json_response = response.json()
#         st.write("Response Content:", json_response)
#         return json_response
#     except json.JSONDecodeError:
#         st.error("Failed to decode JSON response.")
#         st.write("Raw Response Content:", response.text)
#         return None

# services = {
#     "Conversation Control and Customization" : "run",
#     "Google Analytics Assistant": {
#         "endpoint": "/google-apis-experimental/nlp-to-ga/openai/v4",
#         "input_fields": ["query", "brand_id", "brand_manager_id"],
#     },
#     "Google Search Console Assistant": {
#         "endpoint": "/google-apis-experimental/nlp-to-gsc/openai/v1",
#         "input_fields": ["query", "brand_id", "brand_manager_id"],
#     },
#     "Google Big Query Assistant": {
#         "endpoint": "/google-apis/nlp-to-gbigquery/openai",
#         "input_fields": ["query", "brand_id", "brand_manager_id"],
#     },
#     "Google Ads Assistant": {
#         "endpoint": "/google-apis/nlp-to-gads/openai",
#         "input_fields": ["query", "brand_id", "brand_manager_id"],
#     },
#     "SQL Database Assistant": {
#         "endpoint": "/google-apis/nlp-to-gbigquery/openai",
#         "input_fields": ["query", "database_schema", "brand_id", "brand_manager_id"],
#     },
#     "Postgres Database Assistant": {
#         "endpoint": "/google-apis/nlp-to-gbigquery/openai",
#         "input_fields": ["query", "database_schema", "brand_id", "brand_manager_id"],
#     },
#     "Excel Sheet Assistant": {
#         "endpoint": "/xlsqa/llid/pipeline/conversational/pickle",
#         "input_fields": ["query", "brand_id", "brand_manager_id", "file_id"],
#     },
#     "CSV Assistant": {
#         "endpoint": "/csvqa/llid/pipeline/conversational",
#         "input_fields": ["query", "brand_id", "brand_manager_id", "file_id"],
#     },
#     "PDF Assistant": {
#         "endpoint": "/pdfqa/llid/vector",
#         "input_fields": ["query", "brand_id", "brand_manager_id", "file_id"],
#     },
#     "Media Upload": {
#         "endpoint": "/upload/local-media",
#         "input_fields": ["brand_id", "brand_manager_id", "vector_storage", "pickle_storage"]
#     }
# }

# # Set page configuration to collapse sidebar by default
# st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="NLP Services", page_icon="🤖")

# # Custom CSS to style the sidebar buttons
# st.markdown(
#     """
#     <style>
#     .sidebar .sidebar-content {
#         background-color: #f0f2f6;
#         padding: 10px;
#         display: flex;
#         flex-direction: column;
#         align-items: center;
#     }
#     .stButton > button {
#         width: 100%;
#         height: 50px;
#         margin-bottom: 10px;
#         background-color: #ADD8E6; /* Light blue color */
#         color: white;
#         border: none;
#         text-align: center;
#         font-size: 16px;
#         cursor: pointer;
#     }
#     .stButton > button:hover {
#         color: #00008B; /* Darker blue text color on hover */
#     }
#     .main-header {
#         text-align: center;
#         color: #4CAF50;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# st.sidebar.title("Service Selector")

# # Initialize session state for selected service
# if 'selected_service' not in st.session_state:
#     st.session_state.selected_service = None

# # Create buttons for each service in a centered manner
# for service in services.keys():
#     if st.sidebar.button(service):
#         st.session_state.selected_service = service

# # If no service is selected, display welcome message
# if not st.session_state.selected_service:
#     st.markdown("<h1 class='main-header'>Welcome to Our NLP Services 🤖</h1>", unsafe_allow_html=True)
# else:
#     service_name = st.session_state.selected_service
#     if service_name == 'Conversation Control and Customization':
#         st.header(f"Service: {service_name}")
#         if 'summarized_content' not in st.session_state:
#             st.session_state.summarized_content = None
#         input_text = st.text_area("Enter the Content", placeholder="Paste or type your content here", height=200)
#         no_words = st.text_input('Maximum Word Limit for Summary', placeholder="Enter the maximum word limit")
#         blog_style = st.selectbox('Summarizing according to', ('Casual', 'Formal'), index=0)
#         if st.button("Generate Summary"):
#             if input_text.strip() and no_words.isdigit() and int(no_words) > 0:
#                 summarized_content = getLLamaresponse(input_text, no_words, blog_style)
#                 if summarized_content:
#                     st.session_state.summarized_content = summarized_content  # Set session state
#                     st.success("Summary generated successfully!")
#                     st.write(summarized_content)
#                 else:
#                     st.warning("Unable to generate summary. Please try again.")
#             else:
#                 st.error("Invalid input. Please provide valid content and word limit.")

#         language_mapping = {
#             "English": "eng",
#             "Hindi": "hin",
#             "Urdu": "urd",
#             "Punjabi": "pan",
#             "Gujarati": "guj",
#             "Marathi": "mar",
#             "Telugu": "tel",
#             "Kannada": "kan",
#             "Malayalam": "mal",
#             "Tamil": "tam",
#             "Odia": "ory",
#             "Bengali": "ben",
#             "Assamese": "asm",
#             "Manipuri": "mni",
#         }
        
#         if st.session_state.summarized_content:
#             selected_input_language_display = st.selectbox('Select Input Language', list(language_mapping.keys()))
#             selected_output_language_display = st.selectbox('Select Output Language', list(language_mapping.keys()))
#             src_lang = language_mapping[selected_input_language_display]
#             tgt_lang = language_mapping[selected_output_language_display]
            
#             if st.button("Translate Summary"):
#                 translated_text = translate_text(st.session_state.summarized_content, src_lang, tgt_lang)
#                 st.subheader("Summarized Content")
#                 st.write(st.session_state.summarized_content)
#                 st.subheader("Translated Summary")
#                 st.write(translated_text)

#     elif service_name=='Media Upload':
#         service_details = services[service_name]
#         input_fields = service_details["input_fields"]
#         endpoint = service_details["endpoint"]

#         st.header(f"Service: {service_name}")
#         st.subheader("Input Fields")

#         input_data = {}

#         uploaded_file = st.file_uploader("Choose a file", type=["png", "jpg", "jpeg", "mp4", "mp3", "pdf", "csv", "xls"])
#         for field in input_fields:
#             if field in ["vector_storage", "pickle_storage"]:
#                 input_data[field] = st.checkbox(field.capitalize())
#             else:
#                 input_data[field] = st.text_input(label=field)

#         if st.button("Upload"):
#             if uploaded_file is not None and input_data["brand_id"] and input_data["brand_manager_id"]:
#                 files = {'file': (uploaded_file.name, uploaded_file, uploaded_file.type)}
#                 data = {
#                     "brand_id": input_data["brand_id"],
#                     "brand_manager_id": input_data["brand_manager_id"],
#                     "vector_storage": str(input_data["vector_storage"]).lower(),
#                     "pickle_storage": str(input_data["pickle_storage"]).lower()
#                 }
#                 response = upload_file_to_flask(endpoint, files, data)
#                 if response and "file_name" in response:
#                     st.success(f"File uploaded successfully: {response['file_name']}")
#                 else:
#                     st.error("Failed to upload file.")
#             else:
#                 st.error("Please fill in all required fields and select a file.")

#     else:
#         service_details = services[service_name]
#         input_fields = service_details["input_fields"]
#         endpoint = service_details["endpoint"]

#         st.header(f"Service: {service_name}")
#         st.subheader("Input Fields")

#         input_data = {}
#         for field in input_fields:
#             input_data[field] = st.text_input(label=field)

#         if st.button("Send Request"):
#             response = send_request_to_flask(endpoint, input_data)
#             if service_name == "Google Analytics Assistant" or service_name == "Google Search Console Assistant":
#                 st.write(response["data"])
#                 st.subheader("Response")
#                 st.json(response)
#             else:
#                 st.subheader("Response")
#                 st.write(response)