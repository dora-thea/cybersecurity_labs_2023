import math
from collections import Counter
from cipher import ALPHA

# assumption
MAX_KEY_LENGTH = 15
# the number of repetitions of the most frequent divisor * PERCENT = threshold
# for selecting the most frequent divisors
PERCENT = 0.8
MOST_COMMON_LETTERS = {
    'en': 'e',
    'ru': 'о'
}
FREQUENCIES = {'en': {'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702, 'f': 0.0228,
                      'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025,
                      'm': 0.02406, 'n': 0.06749, 'o': 0.07507, 'p': 0.01929, 'q': 0.00095, 'r': 0.05987,
                      's': 0.06327, 't': 0.09056, 'u': 0.02758, 'v': 0.00978, 'w': 0.0236, 'x': 0.0015,
                      'y': 0.01974, 'z': 0.00074},
               'ru': {'а': 0.07821, 'б': 0.01732, 'в': 0.04491, 'г': 0.01698, 'д': 0.03103, 'е': 0.08567,
                      'ё': 0.0007, 'ж': 0.01082, 'з': 0.01647, 'и': 0.06777, 'й': 0.01041, 'к': 0.03215,
                      'л': 0.04813, 'м': 0.03139, 'н': 0.0685, 'о': 0.11394, 'п': 0.02754, 'р': 0.04234,
                      'с': 0.05382, 'т': 0.06443, 'у': 0.02882, 'ф': 0.00132, 'х': 0.00833, 'ц': 0.00333,
                      'ч': 0.01645, 'ш': 0.00775, 'щ': 0.00331, 'ъ': 0.00023, 'ы': 0.01854, 'ь': 0.02106,
                      'э': 0.0031, 'ю': 0.00544, 'я': 0.01979
                      }}


def prepare_text(text, alphabet):
    return "".join(c for c in text.lower() if c in alphabet)


class Kasiski:
    def __init__(self, length, lang):
        self.length = length
        self.alpha = ALPHA[lang.lower()]

    def find_lgramms(self, text):
        lgramms_tmp = {}

        for i in range(len(text) - self.length + 1):
            lgramms_tmp[text[i: i + self.length]] = lgramms_tmp.get(text[i: i + self.length], []) + [i]

        lgramms = {}
        for key, item in lgramms_tmp.items():
            if len(item) >= 2:
                lgramms[key] = item

        return lgramms

    @staticmethod
    def get_distances(positions):
        return [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]

    def kasiski_examination(self, text):

        ciphertext = prepare_text(text, self.alpha)

        # The ciphertext is analyzed for the presence of repeating l-grams in it
        seq_positions = self.find_lgramms(ciphertext)
        if len(seq_positions) == 0:
            return 0

        # Calculate spacings between positions of l-gramms
        seq_spacings = {}
        for seq, positions in seq_positions.items():
            seq_spacings[seq] = self.get_distances(positions)

        # Count factors (<= MAX_KEY_LENGTH) of all spacings
        factor_count = Counter()
        for spacings in seq_spacings.values():
            for space in spacings:
                for f in range(2, MAX_KEY_LENGTH + 1):
                    if space % f == 0:
                        factor_count[f] += 1

        # Select a subset of the most frequently repeated divisors and return the largest divisor from it
        common = factor_count.most_common()
        passing_score = PERCENT * common[0][1]
        key_len = max([c[0] for c in common if c[1] > passing_score])
        return key_len


class FrequencyAnalyzer:
    def __init__(self, length, lang):
        self.alpha = ALPHA[lang.lower()]
        self.key_length = length
        self.most_common_letter = MOST_COMMON_LETTERS[lang.lower()]
        self.known_freq = list(FREQUENCIES[lang.lower()].values())

    def get_substrings(self, text):
        return [text[i::self.key_length] for i in range(self.key_length)]

    @staticmethod
    def get_frequencies(text):
        return Counter(text)

    # ex. most frequently occurring letter in substring: 'm', consider it as equivalent
    # to the most common letter in natural language('e' in English)
    def frequency_analysis(self, text):
        if self.key_length == 0:
            return ""

        ciphertext = prepare_text(text, self.alpha)
        blocks = self.get_substrings(ciphertext)
        block_frequencies = [self.get_frequencies(block) for block in blocks]

        key = ''
        for i, block in enumerate(blocks):
            ci = block_frequencies[i].most_common()[0][0]
            key += self.alpha[(self.alpha.index(ci) - self.alpha.index(self.most_common_letter))
                              % len(self.alpha)]
        return key

    # [1, 2, 3] --> [3, 1, 2]
    @staticmethod
    def make_shift(freq):
        return [freq[-1]] + freq[:-1]

    # frequency analysis based on selecting shift, that the pattern of relative frequencies matches
    # the pattern of letter frequencies in a natural language
    def frequency_analysis_2(self, text):
        if self.key_length == 0:
            return ""

        ciphertext = prepare_text(text, self.alpha)
        blocks = self.get_substrings(ciphertext)

        key = ''
        for block in blocks:
            block_frequencies = dict.fromkeys(self.alpha, 0)
            for c in block:
                block_frequencies[c] += 1
            temp_freq = list(block_frequencies.values())
            sum_module_lst = []

            for i in range(len(self.alpha)):
                sum_module = 0
                for j in range(len(self.alpha)):
                    sum_module += math.fabs(self.known_freq[i] - temp_freq[i] / len(block))
                sum_module_lst.append(sum_module)
                temp_freq = self.make_shift(temp_freq)

            shift = sum_module_lst.index(min(sum_module_lst))
            key += self.alpha[(len(self.alpha) - shift) % len(self.alpha)]

        return key
