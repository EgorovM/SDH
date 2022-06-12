from abc import ABC, abstractmethod

import pandas as pd
import numpy as np

from laserembeddings import Laser
from langdetect import detect
from sklearn.feature_extraction.text import TfidfVectorizer


# if all sentences are in the same language:

class AbstractVectorizer(ABC):
    @abstractmethod
    def sentence2vec(self, sentence: str) -> np.array:
        pass

    @staticmethod
    @abstractmethod
    def default():
        pass

    
class SentenceTfIdfVectorizer(AbstractVectorizer):
    def __init__(self, vectorizer: TfidfVectorizer):
        self.vectorizer = vectorizer

    def sentence2vec(self, sentence: str) -> np.array:
        return self.vectorizer.transform([sentence]).toarray()[0]

    @staticmethod
    def default() -> 'SentenceTfIdfVectorizer':
        df = pd.read_csv('./events/data/replicas-events.csv', sep=';')
        vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        vectorizer.fit(df['реплика'].values)

        return SentenceTfIdfVectorizer(vectorizer)


class LaserVectorizer(AbstractVectorizer):
    def __init__(self):
        self.laser = Laser()

    def sentence2vec(self, sentence: str) -> np.array:
        language = detect(sentence)

        embeddings = self.laser.embed_sentences(
            [sentence],
            lang=language or 'en'
        )

        return embeddings[0]

    @staticmethod
    def default() -> 'LaserVectorizer':
        return LaserVectorizer()


def get_sentence_vectorizer():
    return LaserVectorizer.default()
