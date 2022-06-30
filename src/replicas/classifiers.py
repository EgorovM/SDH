from abc import ABC, abstractmethod
from typing import List, Union, Tuple

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from events import Event
from replicas import Replica, ReplicasContainer
from utils.vectorizer import AbstractVectorizer


class AbstractEventClassifier(ABC):
    def __init__(self, sentence_vectorizer: AbstractVectorizer):
        self.sentence_vectorizer = sentence_vectorizer

    @abstractmethod
    def fit(self, replicas: List[Replica]) -> None:
        pass

    @abstractmethod
    def classify(self, replica: Replica) -> Event:
        pass

    def as_vector(self, replica) -> np.array:
        sentence = self.sentence_vectorizer.normalizer.normalize([replica.sentence])[0]
        return self.sentence_vectorizer.sentence2vec(
            sentence=sentence
        )


class NeighbourClassifier(AbstractEventClassifier):
    def __init__(self, sentence_vectorizer: AbstractVectorizer):
        super().__init__(sentence_vectorizer)

        self.top_k = 1
        self.replicas = ReplicasContainer()
        self.vectors = None

    def fit(self, replicas: ReplicasContainer) -> None:
        self.replicas = replicas
        self.vectors = self.sentence_vectorizer.batch_sentence2vec([
            replica.sentence for replica in replicas
        ])

    def classify(self, replica: Replica, return_score: bool = False) -> Union[Event, Tuple[Event, float]]:
        if self.vectors is None:
            raise Exception('fit not called yet')

        similars = cosine_similarity([self.as_vector(replica)], self.vectors)[0]
        similars = sorted(zip(self.replicas, similars), key=lambda x: x[1], reverse=True)
        replica, score = similars[0]

        if return_score:
            return replica.event, score

        return replica.event

    @staticmethod
    def from_replicas_container(
        replicas: ReplicasContainer,
        sentence_vectorizer: AbstractVectorizer
    ) -> 'NeighbourClassifier':
        classifier = NeighbourClassifier(sentence_vectorizer)
        classifier.fit(replicas)

        return classifier
