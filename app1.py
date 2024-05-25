import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from translator import translate_text

# Initialize session_state
if 'summarized_content' not in st.session_state:
    st.session_state.summarized_content = None

# Function to get response from LLAma 2 model
def getLLamaresponse(input_text, no_words, blog_style):
    try:
        llm = CTransformers(model='models/llama-2-7b-chat.ggmlv3.q2_K.bin',
                            model_type='llama',
                            config={'max_new_tokens': 256, 'temperature': 0.01, 'context_length' : 1024},
                            device='cuda')

        # Prompt Template
        template = """
            Write a summary in {blog_style} tone for the given {input_text}
            within {no_words} WORDS ONLY and in PARAGHRAPH only. 
        """
        
        prompt = PromptTemplate(input_variables=["blog_style", "input_text", 'no_words'],
                                template=template)
        
        # Generate the response from the LLama 2 model
        response = llm(prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words))
        return response
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Streamlit app configuration
st.set_page_config(page_title="Conversation Control & Customization",
                   page_icon='🤖',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.title("Conversation Control & Customization 🤖")
st.markdown("Enter the content and customize how it should be summarized and translated.")

# Input fields
input_text = st.text_area("Enter the Content", placeholder="Paste or type your content here", height=200)
no_words = st.text_input('Maximum Word Limit for Summary', placeholder="Enter the maximum word limit")
blog_style = st.selectbox('Summarizing according to', ('Casual', 'Formal'), index=0)

# Generate Summary button
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


# Debug: Print session state and content
# st.write("Session State:", st.session_state)
# st.write("Summarized Content:", st.session_state.summarized_content)

# Translate button
if st.session_state.summarized_content:
    selected_input_language_display = st.selectbox('Select Input Language', list(language_mapping.keys()))
    selected_output_language_display = st.selectbox('Select Output Language', list(language_mapping.keys()))
    src_lang = language_mapping[selected_input_language_display]
    tgt_lang = language_mapping[selected_output_language_display]

    if st.button("Translate Summary"):
        translated_text = translate_text(st.session_state.summarized_content, src_lang, tgt_lang)
        st.write(st.session_state.summarized_content)
        st.write(translated_text)