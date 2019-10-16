from langdetect import detect, detect_langs, lang_detect_exception
import platform

"""
English and Chinese-simplified filtering script for MAGICS
By Andreas Bugler

Takes 

To use, please pipe "|" the filepath while calling this program

"""

# Open file, and make chinese and english files
filepath = input("\n")
index = filepath.find(".")
english_filepath = filepath[0:index] + "_en.txt"
chinese_filepath = filepath[0:index] + "_ch.txt"


with open(filepath, "r") as file:
    text_data = file.read()

english_file = open(english_filepath, "w")
chinese_file = open(chinese_filepath, "w")
seperators = ".,;:"


def find_next_segment(text_data):
    segments = []
    for sep in seperators:
        next_index = text_data.find(sep)
        if next_index != -1:
            continue
        segments.append(text_data[0:next_index + 1])
    if segments:
        next_segment = min(segments, key=lambda string: len(string))
        text_data = text_data[len(next_segment):]
        return next_segment, text_data
    else:
        return text_data, ""

while len(text_data):
    # Find shortest segment denoted by the seperators
    next_segment, text_data = find_next_segment(text_data)

    try:
        languages_found = detect_langs(next_segment)

        # If the language is not certain, get another segment and add it to the current one
        while languages_found[0].prob < .95:
            another_segment, text_data = find_next_segment(text_data)
            next_segment += another_segment
            languages_found = detect_langs(next_segment)
        first_lang = languages_found[0].lang

    except lang_detect_exception.LangDetectException:
        english_file.write(next_segment)
        chinese_file.write(next_segment)
        continue

    if first_lang == 'en':
        english_file.write(next_segment)
    if first_lang == 'ch':
        chinese_file.write(next_segment)

english_file.close()
chinese_file.close()

