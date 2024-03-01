import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from translator import translate_text

# Initialize session_state
if 'summarized_content' not in st.session_state:
    st.session_state.summarized_content = None

# Function to get response from LLAma 2 model
def getLLamaresponse(input_text, no_words, blog_style):
    llm = CTransformers(model='models/llama-2-7b-chat.ggmlv3.q2_K.bin',
                        model_type='llama',
                        config={'max_new_tokens': 256, 'temperature': 0.01},
                        device='cuda')

    # Prompt Template
    template = """
        Write a summary in {blog_style} tone for {input_text}
        within {no_words} words.
    """
    
    prompt = PromptTemplate(input_variables=["blog_style", "input_text", 'no_words'],
                            template=template)
    
    # Generate the response from the LLama 2 model
    response = llm(prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words))
    print(response)
    return response

# Streamlit app configuration
st.set_page_config(page_title="Conversation Control & Customization",
                   page_icon='🤖',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("Conversation Control & Customization 🤖")

input_text = st.text_input("Enter the Content")

# creating two more columns for additional 2 fields
col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input('No of Words')

with col2:
    blog_style = st.selectbox('Summarizing according to', ('Casual', 'Formal'), index=0)

summarized_content = None

submit = st.button("Generate")

# Final response
if submit:
    st.session_state.summarized_content = getLLamaresponse(input_text, no_words, blog_style)
    st.write(st.session_state.summarized_content)

# Language selection
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

col3, col4 = st.columns([5, 5])

with col3:
    selected_input_language_display = st.selectbox('Select Language For Input Language', list(language_mapping.keys()))

with col4:
    selected_output_language_display = st.selectbox('Select Language For Output Language', list(language_mapping.keys()))

src_lang = language_mapping[selected_input_language_display]
tgt_lang = language_mapping[selected_output_language_display]

# Translate button
submit1 = st.button("Translate")
if submit1 and st.session_state.summarized_content:
    st.write(translate_text(st.session_state.summarized_content, src_lang, tgt_lang))