from googletrans import Translator


en_translator = Translator()

def translate_word(word: str) -> str:
    return en_translator.translate(word).text


def en_vectorizer(vectorizer) -> None:
    keys = list(vectorizer.vocabulary_.keys())

    for key in keys:
        key_en = en_translator.translate(key).text
        vectorizer.vocabulary_[key_en] = vectorizer.vocabulary_[key]
        del vectorizer.vocabulary_[key]
