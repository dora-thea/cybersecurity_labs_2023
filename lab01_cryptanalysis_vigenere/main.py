import json

from cipher import Vigenere
from cryptanalysis import Kasiski, FrequencyAnalyzer
from reportgenerator import ReportGenerator

lang = 'en'

with open('en.json') as data_file:
    en_text = json.load(data_file)

with open('key_en.json') as data_file:
    en_keys = json.load(data_file)

TABLE_COLS_ALL_CASES = ['Text length']
TABLE_COLS_ALL_CASES.extend(list(en_keys.values()))
TABLE_COLS = [
    'Text length',
    'Keyword',
    'Key length',
    'Found keyword',
    'Found key length',
    'Match'
]

report = ReportGenerator(open('report/report.md', 'w'))


def run_test(text, keyword, lgramm_len, sign=0):
    encrypted = Vigenere(keyword, lang).encrypt(text)
    probable_key_length = Kasiski(lgramm_len, lang).kasiski_examination(encrypted)
    found_keyword = FrequencyAnalyzer(probable_key_length, lang).frequency_analysis(encrypted)

    if sign == 1:
        return found_keyword

    return report.print_test(len(text), keyword, found_keyword)


def run():
    # 1
    for lgramm in range(3, 6):
        # this cycles significantly slow down report generation
        report.report.write(f"# Lgramm length {lgramm}\n")
        report.print_table_head(
            f"Matching the length of the initial key with the length of the key found using the "
            f"kasiski method.", TABLE_COLS_ALL_CASES)
        for text in en_text.values():
            found_keywords = []
            for keyword in en_keys.values():
                found_keywords.append(run_test(text, keyword, lgramm, sign=1))
            report.print_test_kasiski(len(text), list(en_keys.values()), found_keywords)

        report.print_table_head(f"The percentage of the match of the original and found key.", TABLE_COLS_ALL_CASES)
        for text in en_text.values():
            found_keywords = []
            for keyword in en_keys.values():
                found_keywords.append(run_test(text, keyword, lgramm, sign=1))
            report.print_test_matching(len(text), list(en_keys.values()), found_keywords)

    report.report.write("### *The longer the l-gramm, the higher the risk of not finding it, so finding the key length "
                        "becomes impossible.*\n")
    report.report.write("### *In general, we see that with small keys and an increase in the length of the text, "
                        "the text selection is more like a natural one, so the keyword is restored quite successfully "
                        "and vice versa*\n")

    # 2
    report.print_table_head('Fixed keyword length', TABLE_COLS)
    percents = []
    text_lengths = []
    for text in en_text.values():
        text_lengths.append(len(text))
        percents.append(run_test(text, en_keys["4"], 3))
    report.add_plot_to_report(text_lengths, percents, 'test2', 'Text')

    # 3
    report.print_table_head('Fixed text length', TABLE_COLS)
    percents = []
    for keyword in en_keys.values():
        percents.append(run_test(en_text["3"], keyword, 3))
    report.add_plot_to_report(list(map(len, list(en_keys.values()))), percents, 'test3', 'Keyword')

    '''
    # test frequency_analysis_2()
    vigenere = Vigenere('j', lang)
    encrypted = vigenere.encrypt(en_text["7"])
    analyzer = FrequencyAnalyzer(1, 'en')
    key = analyzer.frequency_analysis_2(encrypted)
    vig = Vigenere(key, 'en')
    print(vig.decrypt(encrypted))
    '''
    report.report.write("# Key points:\n 1. Longer l-gramms may offer better choices because these matches are less "
                        "likely to be by chance.\n 2. But the longer it is, the higher the risk that it will simply "
                        "not be found in the text.\n 3. Since a distance may be a multiple of the keyword length, "
                        "a factor of a distance may be the length of the keyword. If a match is by pure chance, "
                        "the factors of this distance may not be factors of the keyword length. In general, "
                        "a good choice is the largest one that appears most often. \n 4. To decrypt the text, "
                        "knowing the length of the key, substrings are selected from each n-th (n = len(key)) letter. "
                        "Such a text does not demonstrate the expected distribution of letter frequencies. The "
                        "situation may be aggravated by such a distortion of texts, such as: did not -> didn't\n "
                        "5. In addition, the longer the keyword, the sample is not only smaller, but also less "
                        "representative (the set of letters does not look like a natural text)\n "
                        "6. Thus, the program successfully implements finding the key length for the text encrypted "
                        "with the Vigenere cipher, but frequency analysis reduces the degree of success of key "
                        "recovery.\n")


if __name__ == '__main__':
    run()
