import requests
import json
import sys
from deep_translator import GoogleTranslator
from langdetect import detect

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

# You can use DeepL or Google Translate to translate the text
# DeepL can translate more casual text in Japanese
# DeepLx is a free and open-source DeepL API, i use this because DeepL Pro is not available in my country
# but sometimes i'm facing request limit, so i use Google Translate as a backup
def translate_deeplx(text, source, target):
    url = "http://localhost:1188/translate"
    headers = {"Content-Type": "application/json"}

    # define the parameters for the translation request
    params = {
        "text": text,
        "source_lang": source,
        "target_lang": target
    }

    # convert the parameters to a JSON string
    payload = json.dumps(params)

    try:
        # send the POST request with the JSON payload
        response = requests.post(url, headers=headers, data=payload)

        # get the response data as a JSON object
        data = response.json()

        # extract the translated text from the response
        translated_text = data['data']

        return translated_text
    except Exception as e:
        print(f"DeepLX error: {e}, falling back to Google Translate")
        return translate_google(text, source, target)

def translate_google(text, source, target):
    try:
        # Mapeamento de códigos de idioma
        lang_map = {
            "JA": "ja",
            "EN": "en",
            "PT": "pt",
            "ID": "id",
            "ES": "es",
            "FR": "fr",
            "DE": "de",
            "ZH": "zh-CN",
            "KO": "ko",
            "RU": "ru",
            "AR": "ar",
            "HI": "hi",
        }
        
        # Converte os códigos de idioma
        source_lang = lang_map.get(source.upper(), source.lower())
        target_lang = lang_map.get(target.upper(), target.lower())
        
        # Se source e target forem iguais, retorna o texto original
        if source_lang == target_lang:
            return text
        
        # Traduz usando deep-translator
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        return translated
    except Exception as e:
        print(f"Error translate: {e}")
        return text  # Retorna o texto original se falhar
    
def detect_google(text):
    try:
        # Detecta o idioma usando langdetect
        detected = detect(text)
        return detected.upper()
    except Exception as e:
        print(f"Error detect: {e}")
        return "EN"  # Retorna inglês como padrão

if __name__ == "__main__":
    text = "aku tidak menyukaimu"
    source = translate_google(text, "ID", "JA")
    print(source)