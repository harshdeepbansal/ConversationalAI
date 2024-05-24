import gradio as gr
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
from translator import translate_text

# Define language mapping in global scope
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
            within {no_words} WORDS ONLY and in PARAGRAPH only.
        """
        
        prompt = PromptTemplate(input_variables=["blog_style", "input_text", 'no_words'],
                                template=template)
        
        # Generate the response from the LLama 2 model
        response = llm(prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words))
        return response
    except Exception as e:
        return f"Error: {e}"

# Define Gradio interface functions
def generate_summary(input_text, no_words, blog_style):
    if input_text.strip() and no_words.isdigit() and int(no_words) > 0:
        summarized_content = getLLamaresponse(input_text, no_words, blog_style)
        if summarized_content:
            return summarized_content
        else:
            return "Unable to generate summary. Please try again."
    else:
        return "Invalid input. Please provide valid content and word limit."

def translate_summary(summarized_content, input_language, output_language):
    src_lang = language_mapping[input_language]
    tgt_lang = language_mapping[output_language]
    
    translated_text = translate_text(summarized_content, src_lang, tgt_lang)
    return translated_text

# Create Gradio interface
input_text = gr.Textbox(lines=10, placeholder="Paste or type your content here", label="Input Text")
no_words = gr.Textbox(placeholder="Enter the maximum word limit", label="Maximum Word Limit for Summary")
blog_style = gr.Radio(choices=["Casual", "Formal"], label="Summarizing according to")
input_language = gr.Dropdown(choices=list(language_mapping.keys()), label="Select Input Language")
output_language = gr.Dropdown(choices=list(language_mapping.keys()), label="Select Output Language")
summarized_content = gr.Textbox(label="Summarized Content")
translated_text = gr.Textbox(label="Translated Summary")

# Define the layout of the Gradio interface
with gr.Blocks() as iface:
    with gr.Row():
        with gr.Column():
            input_text.render()
            no_words.render()
            blog_style.render()
            gr.Button("Generate Summary").click(generate_summary, [input_text, no_words, blog_style], summarized_content)
    with gr.Row():
        summarized_content.render()
    with gr.Row():
        with gr.Column():
            input_language.render()
            output_language.render()
            gr.Button("Translate Summary").click(translate_summary, [summarized_content, input_language, output_language], translated_text)
    with gr.Row():
        translated_text.render()

iface.launch()
