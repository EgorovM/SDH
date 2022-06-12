from typing import Tuple

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from replicas import ReplicasContainer, Replica
from replicas.classifiers import AbstractEventClassifier, NeighbourClassifier
from utils.vectorizer import AbstractVectorizer, SentenceTfIdfVectorizer, get_sentence_vectorizer


class QuestionAnswer:
    def __init__(
        self,
        replicas: ReplicasContainer,
        text_classifier: AbstractEventClassifier = None,
        sentence_vectorizer: AbstractVectorizer = None,
    ) -> None:
        sentence_vectorizer = sentence_vectorizer or get_sentence_vectorizer()

        self.replicas = replicas
        self.text_classifier = text_classifier or NeighbourClassifier.from_replicas_container(
            self.replicas,
            sentence_vectorizer,
        )

    def predict(self, sentence: str) -> Tuple[str, float]:
        replica = Replica.from_sentence(sentence)
        answer, score = self.text_classifier.classify(replica, return_score=True)

        return answer, score

    @staticmethod
    def default() -> 'QuestionAnswer':
        df = pd.read_csv('./informations/data/question_answer.csv', sep=';')
        replica_container = ReplicasContainer()
        replica_container.extend(df['question'], df['answer'])

        vectorizer = TfidfVectorizer()
        vectorizer.fit(df['question'])
        sentence_vectorizer = SentenceTfIdfVectorizer(vectorizer)

        event_classifier = QuestionAnswer(
            replica_container,
            sentence_vectorizer=sentence_vectorizer
        )

        return event_classifier
