from collections import namedtuple
from googletrans import Translator


moke_translate = namedtuple('Translate', ['text'])

class MokeTranslator:
    def translate(self, word: str) -> str:
        return moke_translate(word)


en_translator = MokeTranslator()


def translate_word(word: str) -> str:
    return en_translator.translate(word).text


def en_vectorizer(vectorizer) -> None:
    keys = list(vectorizer.vocabulary_.keys())

    for key in keys:
        key_en = translate_word(key)
        vectorizer.vocabulary_[key_en] = vectorizer.vocabulary_[key]
        del vectorizer.vocabulary_[key]
