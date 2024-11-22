#!/usr/bin/python3
import sys
import os
import html
from google.cloud import translate
def list_languages() -> dict:
    """Lists all available languages."""
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    results = translate_client.get_languages()

    for language in results:
        print("{name} ({language})".format(**language))

    return results
#--------------------------------------------------------------------------------------------------
def translate_text(target: str, text: str) -> dict:
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)
    return html.unescape(result["translatedText"])

def parsing():
    import os
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('text', action='store',help='input string to translate',type=str)
    parser.add_argument('-t','--target', action='store', default='en', help="target language : english\(default),pt,es...")
    parser.add_argument('-l','--list', action='store_true', help="list some target language")
    args = parser.parse_args()
    text = args.text
    tg   = args.target
    listt = args.list
    return text,tg,listt

#--------------------------------------------------------------------------------------------------
if __name__=="__main__":

    text,t,listt=parsing()
    if listt : 
        for target in list_languages():
            print(f"{target['language']}: {target['name']}") 
    for textline in text.split(os.linesep)[:-1] :
        print(translate_text(t,textline))
        print()
    print(translate_text(t,text.split(os.linesep)[-1]))

