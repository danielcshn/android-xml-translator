<div align="center">
  <h3> 📝 Android XML Translator 📝 </h3>
  <hr>
  <p>Translate your Android project's strings.xml to your desired language using Translate API.</p>
  <hr>
</div>

<div align="center">
  
[![GitHub issues](https://img.shields.io/bitbucket/issues/danielcshn/android-xml-translator?style=for-the-badge)](https://github.com/danielcshn/android-xml-translator/issues)
[![GitHub watchers](https://img.shields.io/github/watchers/danielcshn/android-xml-translator?style=for-the-badge)](https://github.com/danielcshn/android-xml-translator/watchers)
[![GitHub forks](https://img.shields.io/github/forks/danielcshn/android-xml-translator?style=for-the-badge)](https://github.com/danielcshn/android-xml-translator/fork)
[![GitHub stars](https://img.shields.io/github/stars/danielcshn/android-xml-translator?style=for-the-badge)](https://github.com/danielcshn/android-xml-translator/stargazers)
[![License](https://img.shields.io/github/license/danielcshn/android-xml-translator?style=for-the-badge)](https://github.com/danielcshn/android-xml-translator/blob/main/LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/danielcshn/android-xml-translator?style=for-the-badge)](https://github.com/danielcshn/android-xml-translator/commits/main)

</div>

### Prerequisites

- [Python](https://www.python.org/) - v3.8 or high

---

## 🐛 Bug reports

Please feel free to submit bug reports on the github issue tracker at https://github.com/danielcshn/android-xml-translator/issues

---

## ⬇️ Installing
```
git clone https://github.com/danielcshn/android-xml-translator.git
pip install -r requirements.txt
```

---

## 💡 Arguments: 
 **args**                   | **Description**                                            | **Must / Optional**
--------------------------- | ---------------------------------------------------------- | -------------------
`-f`, `--file`              | Path to the strings.xml file.                              | Must
`-i`, `--input_lang`        | Source language code.                                      | Must
`-o`, `--output_langs`      | Output languages. Optional Comma-separated or 'TOP10'      | Must
`-sl`, `--show-languages`   | Show supported languages.                                  | Optional
`-t`, `--timeout`           | Time to wait between translations. Default 0s.             | Optional

<b>TOP10:</b>
- zh-CN = Chinese (simplified)
- es = Spanish
- en = English
- hi = Hindi
- ar = Arabic
- pt = Portuguese
- bn = Bengali
- ru = Russian
- ja = Japanese
- de = German

## 🛠️ Executing examples
```
python xml-translator.py -f C:\dir\strings.xml -sl
python xml-translator.py -f C:\dir\strings.xml -i en -o es
python xml-translator.py -f C:\dir\strings.xml -i en -o es,fr
python xml-translator.py -f C:\dir\strings.xml -i en -o es,fr -t 5
python xml-translator.py -f C:\dir\strings.xml -i en -o TOP10
python xml-translator.py -f C:\dir\strings.xml -i en -o TOP10 -t 2
```
