#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import xml.etree.ElementTree as ET
from deep_translator import GoogleTranslator

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    strings = {elem.attrib['name']: elem.text for elem in root.findall('string')}
    return tree, root, strings

def translate_strings(strings, src_lang, target_langs):
    translations = {lang: {} for lang in target_langs}

    for key, text in strings.items():
        for lang in target_langs:
            translated_text = GoogleTranslator(source=src_lang, target=lang).translate(text)
            translations[lang][key] = translated_text

    return translations

def create_translated_xml(base_tree, base_root, translations, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for lang, translated_strings in translations.items():
        lang_dir = os.path.join(output_dir, f'values-{lang}')
        os.makedirs(lang_dir, exist_ok=True)
        output_path = os.path.join(lang_dir, 'strings.xml')
        
        for elem in base_root.findall('string'):
            key = elem.attrib['name']
            if key in translated_strings:
                elem.text = translated_strings[key]
        
        # base_tree.write(output_path, encoding='utf-8', xml_declaration=True)
        with open(output_path, "wb") as f:
            f.write(b"<?xml version='1.0' encoding='utf-8'?>\n")
            base_tree.write(f, encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Translate Android strings.xml file.")
    parser.add_argument("-f", "--file", required=True, help="Path to the strings.xml file")
    parser.add_argument("-i", "--input_lang", required=True, help="Source language code")
    parser.add_argument("-o", "--output_langs", required=True, help="Comma-separated target languages")
    
    args = parser.parse_args()
    file_path = args.file
    input_lang = args.input_lang
    output_langs = args.output_langs.split(',')
    output_dir = os.path.join(os.path.dirname(file_path), 'translates')
    
    base_tree, base_root, strings = parse_xml(file_path)
    translations = translate_strings(strings, input_lang, output_langs)
    create_translated_xml(base_tree, base_root, translations, output_dir)
    
    print(f"Translations saved in {output_dir}")

if __name__ == "__main__":
    main()
