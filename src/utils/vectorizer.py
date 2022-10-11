from abc import ABC, abstractmethod
from typing import List

import pandas as pd
import numpy as np
import spacy

from gensim.models import KeyedVectors
from laserembeddings import Laser
from sklearn.feature_extraction.text import TfidfVectorizer

from utils.preprocessing import CachedNormalizer


class AbstractVectorizer(ABC):
    def __init__(self) -> None:
        self.normalizer = CachedNormalizer()

    def batch_sentence2vec(
        self, sentences: List[str], language: str = "ru"
    ) -> np.array:
        sentences = self.normalizer.normalize(sentences)
        return self._batch_sentence2vec(sentences, language)

    def sentence2vec(self, sentence: str, language: str = "ru") -> np.array:
        return self.batch_sentence2vec([sentence], language=language)[0]

    @abstractmethod
    def _batch_sentence2vec(
        self, sentences: List[str], language: str = "ru"
    ) -> np.array:
        pass

    @staticmethod
    @abstractmethod
    def default():
        pass


class SentenceTfIdfVectorizer(AbstractVectorizer):
    def __init__(self, vectorizer: TfidfVectorizer):
        self.vectorizer = vectorizer
        super().__init__()

    def _batch_sentence2vec(
        self, sentences: List[str], language: str = "ru"
    ) -> np.array:
        return self.vectorizer.transform(sentences).toarray()

    @staticmethod
    def default() -> "SentenceTfIdfVectorizer":
        df = pd.read_csv("./events/data/replicas-events.csv", sep=";")
        vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        vectorizer.fit(df["реплика"].values)

        return SentenceTfIdfVectorizer(vectorizer)


class Word2VecVectorizer(AbstractVectorizer):
    DEFAULT_MODEL_PATH = "./utils/models/ruscorpora_upos_skipgram_300_5_2018.vec.gz"

    def __init__(self, word2vec: KeyedVectors) -> None:
        self.word2vec = word2vec
        self.sp = spacy.load("en_core_web_sm")
        super().__init__()

    def sentence2vec(self, sentence: str, language: str = "ru") -> np.array:
        vector = np.zeros((self.word2vec.vector_size,))
        count = 1

        for word in self.sp(sentence):
            key = "_".join([word.text, word.pos_])

            if key in self.word2vec:
                vector += self.word2vec[key]
                count += 1

        return vector / count

    def _batch_sentence2vec(
        self, sentences: List[str], language: str = "ru"
    ) -> np.array:
        return np.array(
            [self.sentence2vec(sentence, language) for sentence in sentences]
        )

    @staticmethod
    def default() -> "SentenceTfIdfVectorizer":
        word2vec = KeyedVectors.load_word2vec_format(
            Word2VecVectorizer.DEFAULT_MODEL_PATH
        )
        return Word2VecVectorizer(word2vec)


class LaserVectorizer(AbstractVectorizer):
    def __init__(self):
        self.laser = Laser()
        super().__init__()

    def _batch_sentence2vec(
        self, sentences: List[str], language: str = "ru"
    ) -> np.array:
        embeddings = self.laser.embed_sentences(sentences, lang=language)
        return embeddings

    @staticmethod
    def default() -> "LaserVectorizer":
        return LaserVectorizer()


def get_sentence_vectorizer():
    return LaserVectorizer.default()
