import string

ALPHA = {
    'en': string.ascii_lowercase,
    'ru': 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
}


class Vigenere:
    def __init__(self, key, lang):
        self.key = key.lower()
        self.alpha = ALPHA[lang.lower()]

    def transform_string(self, text, sign=1):
        result = ''
        key_nums = [self.alpha.index(self.key[i]) for i in range(len(self.key))]
        # file must be properly encoded
        i = 0
        for c in text:
            if c.isalpha():
                if c.islower():
                    result += self.alpha[(self.alpha.index(c) +
                                          sign * key_nums[i % len(self.key)]) % len(self.alpha)]
                else:
                    result += self.alpha[(self.alpha.index(c.lower()) +
                                          sign * key_nums[i % len(self.key)]) % len(self.alpha)].upper()
                i += 1
            else:
                result += c

        return result

    def encrypt(self, text):
        return self.transform_string(text)

    def decrypt(self, text):
        return self.transform_string(text, sign=-1)
