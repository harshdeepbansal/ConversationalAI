import torch
import torchaudio
# from seamless_communication.models.unity import load_unity_text_tokenizer
from seamless_communication.inference import Translator



def load_seamless_communication(MODEL_NAME="seamlessM4T_medium", VOCODER_NAME="vocoder_36langs"):

    if torch.cuda.is_available():
        DEVICE = torch.device("cuda:0")
        DATA_TYPE = torch.float16
    else:
        DEVICE = torch.device("cpu")
        DATA_TYPE = torch.float32

    # Load TextTokenizer separately
    # text_tokenizer = load_unity_text_tokenizer(MODEL_NAME)

    translator = Translator(
        MODEL_NAME, VOCODER_NAME, DEVICE, dtype=DATA_TYPE
    )
    return translator



def translate_text(input_text, src_lang, tgt_lang):
    # Translate input_text from source language to target language
    translator = load_seamless_communication()
    translated_text, _ = translator.predict(input_text, "t2tt", tgt_lang, src_lang)
    print(translated_text[0])
    return str(translated_text[0])


if __name__ == "__main__":
    x=translate_text("Hello","eng","hin")
    print(x)
    
