from PyBinglate import BingTranslator, LANGUAGES
from google.cloud import translate
import json
import html
import os

class GoogleAPI:
    
    def __init__(self):
        self.list_of_used_lang = list()
        self.google_tr = translate.Client.from_service_account_json(os.path.join(os.path.curdir, "utils", "creds.json"))

    def google_translate(self, text:str, target='ru'):
        try:
            for each in self.list_of_used_lang:
                text.replace(each, '')
            GOOGLE_LANGUAGES = self.google_tr.get_languages(target_language=target)
            trans = self.google_tr.translate(text, target_language=target)
            tr_text = trans['translatedText']
            tr_text = html.unescape(tr_text)
            x = trans['detectedSourceLanguage']
            for lang in GOOGLE_LANGUAGES:
                if lang['language'] == x:
                    language = lang['name']
                    break
            try:
                language = f"{language[0].upper()}{language[1:]}:\n"
                if language not in self.list_of_used_lang:
                    self.list_of_used_lang.append(language)
            except:
                raise MyGoogleAPIError("There is no such language.. // What?")

            result = f"{language}{tr_text}"
            return result

        except Exception as e:
            raise MyGoogleAPIError(f"Google Translation API Error ({e})")


class MyBingTranslator:
    def __init__(self):
        self.list_of_used_lang = list()
        self.tr = BingTranslator()

    def translate(self, text, target='ru', tell_input_lang=False):
        try:
            try:
                translation = self.tr.translate(text, target, raw=tell_input_lang)
            except:
                translation = self.tr.translate(text, 'en', raw=tell_input_lang)
            if tell_input_lang:
                from_lang = translation[0]['detectedLanguage']['language']
                from_lang = LANGUAGES[from_lang]
                from_lang = self.tr.translate(from_lang, target)
                from_lang = f'{from_lang[0].upper()}{from_lang[1:]}:\n'

                for each in self.list_of_used_lang:
                    text.replace(each, '')
                if from_lang not in self.list_of_used_lang:
                    self.list_of_used_lang.append(from_lang)

                tr_text = translation[0]['translations'][0]['text']
                tr_text = html.unescape(tr_text)
                translation_and_lang = f"{from_lang}{tr_text}"
                return translation_and_lang
            else:
                tr_text = html.unescape(tr_text)
                return translation
        except Exception as e:
            print(e)
            raise MyBingError(f"BingTranslator failed with error >>> {e}")

# Custom errors
class MyBingError(Exception):
    pass

class MyGoogleAPIError(Exception):
    pass
