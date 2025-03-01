#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import argparse
import xml.etree.ElementTree as ET
from deep_translator import GoogleTranslator

SUPPORTED_LANGUAGES = {
    'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'assamese': 'as', 'aymara': 'ay',
    'azerbaijani': 'az', 'bambara': 'bm', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bhojpuri': 'bho', 'bosnian': 'bs',
    'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-CN', 'chinese (traditional)': 'zh-TW',
    'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dhivehi': 'dv', 'dogri': 'doi', 'dutch': 'nl', 'english': 'en',
    'esperanto': 'eo', 'estonian': 'et', 'ewe': 'ee', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy', 'galician': 'gl',
    'georgian': 'ka', 'german': 'de', 'greek': 'el', 'guarani': 'gn', 'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw',
    'hebrew': 'iw', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'ilocano': 'ilo', 'indonesian': 'id',
    'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'kinyarwanda': 'rw',
    'konkani': 'gom', 'korean': 'ko', 'krio': 'kri', 'kurdish (kurmanji)': 'ku', 'kurdish (sorani)': 'ckb', 'kyrgyz': 'ky', 'lao': 'lo',
    'latin': 'la', 'latvian': 'lv', 'lingala': 'ln', 'lithuanian': 'lt', 'luganda': 'lg', 'luxembourgish': 'lb', 'macedonian': 'mk',
    'maithili': 'mai', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'meiteilon (manipuri)': 'mni-Mtei',
    'mizo': 'lus', 'mongolian': 'mn', 'myanmar': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia (oriya)': 'or', 'oromo': 'om', 'pashto': 'ps',
    'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'quechua': 'qu', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm',
    'sanskrit': 'sa', 'scots gaelic': 'gd', 'sepedi': 'nso', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si',
    'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg',
    'tamil': 'ta', 'tatar': 'tt', 'telugu': 'te', 'thai': 'th', 'tigrinya': 'ti', 'tsonga': 'ts', 'turkish': 'tr', 'turkmen': 'tk', 'twi': 'ak',
    'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'
}

TOP_LANGUAGES = ['zh-CN', 'es', 'en', 'hi', 'ar', 'pt', 'bn', 'ru', 'ja', 'de']

def show_languages():
    print("Supported languages:")
    for lang, code in SUPPORTED_LANGUAGES.items():
        print(f"{code}: {lang}")

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    strings = {elem.attrib['name']: elem.text for elem in root.findall('string')}
    return tree, root, strings

def translate_strings(strings, src_lang, target_langs, delay):
    translations = {lang: {} for lang in target_langs}

    for key, text in strings.items():
        for lang in target_langs:
            translated_text = GoogleTranslator(source=src_lang, target=lang).translate(text)
            translations[lang][key] = translated_text
            time.sleep(delay)
    
    return translations

def create_translated_xml(base_tree, base_root, translations, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for lang, translated_strings in translations.items():
        lang_dir_name = lang.replace('-', '-r')
        lang_dir = os.path.join(output_dir, f'values-{lang_dir_name}')
        os.makedirs(lang_dir, exist_ok=True)
        output_path = os.path.join(lang_dir, 'strings.xml')
        
        for elem in base_root.findall('string'):
            key = elem.attrib['name']
            if key in translated_strings:
                elem.text = translated_strings[key]
        
        with open(output_path, "wb") as f:
            f.write(b"<?xml version='1.0' encoding='utf-8'?>\n")
            base_tree.write(f, encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Translate Android strings.xml file.")
    parser.add_argument("-f", "--file", help="Path to the strings.xml file")
    parser.add_argument("-i", "--input_lang", help="Source language code")
    parser.add_argument("-o", "--output_langs", help="Comma-separated target languages or 'TOP10'")
    parser.add_argument("-sl", "--show-languages", action="store_true", help="Show supported languages")
    parser.add_argument("-t", "--timeout", type=float, default=0, help="Time in seconds to wait between translations")
    
    args = parser.parse_args()

    if args.show_languages:
        show_languages()
        return
    
    if not args.file or not args.input_lang or not args.output_langs:
        parser.error("-f, -i, and -o arguments are required unless using -sl")
    
    if args.input_lang not in SUPPORTED_LANGUAGES.values():
        parser.error(f"Invalid input language: {args.input_lang}")

    if args.output_langs.upper() == "TOP10":
        output_langs = TOP_LANGUAGES
    else:
        output_langs = args.output_langs.split(',')
        for lang in output_langs:
            if lang not in SUPPORTED_LANGUAGES.values():
                parser.error(f"Invalid output language: {lang}")
    
    base_tree, base_root, strings = parse_xml(args.file)
    translations = translate_strings(strings, args.input_lang, output_langs, args.timeout)
    create_translated_xml(base_tree, base_root, translations, os.path.join(os.path.dirname(args.file), 'translates'))
    print("Translations saved.")

if __name__ == "__main__":
    main()