from abc import ABC, abstractmethod

import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer


class AbstractVectorizer(ABC):
    @abstractmethod
    def sentence2vec(self, sentence: str) -> np.array:
        pass


class SentenceTfIdfVectorizer(AbstractVectorizer):
    def __init__(self, vectorizer: TfidfVectorizer):
        self.vectorizer = vectorizer

    @staticmethod
    def default() -> 'SentenceTfIdfVectorizer':
        df = pd.read_csv('./events/data/replicas-events.csv', sep=';')
        vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        vectorizer.fit(df['реплика'].values)

        return SentenceTfIdfVectorizer(vectorizer)

    def sentence2vec(self, sentence: str) -> np.array:
        return self.vectorizer.transform([sentence]).toarray()[0]
