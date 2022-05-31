from abc import ABC, abstractmethod
from typing import List, Union, Tuple

import numpy as np

from events import Event
from replicas import Replica, ReplicasContainer
from utils.vectors import vectors_similarity
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
        return self.sentence_vectorizer.sentence2vec(
            sentence=replica.sentence
        )


class NeighbourClassifier(AbstractEventClassifier):
    def __init__(self, sentence_vectorizer: AbstractVectorizer):
        super().__init__(sentence_vectorizer)

        self.top_k = 1
        self.replicas = ReplicasContainer()

    def fit(self, replicas: ReplicasContainer) -> None:
        self.replicas = replicas

    def classify(self, replica: Replica, return_score: bool = False) -> Union[Event, Tuple[Event, float]]:
        similars = [(r, self.similarity(r, replica)) for r in self.replicas]
        similars.sort(key=lambda x: x[1], reverse=True)
        replica, score = similars[0]

        if return_score:
            return replica.event, score

        return replica.event

    def similarity(self, replica1: Replica, replica2: Replica) -> float:
        vector1 = self.as_vector(replica1)
        vector2 = self.as_vector(replica2)

        return vectors_similarity(vector1, vector2)

    @staticmethod
    def from_replicas_container(
        replicas: ReplicasContainer,
        sentence_vectorizer: AbstractVectorizer
    ) -> 'NeighbourClassifier':
        classifier = NeighbourClassifier(sentence_vectorizer)
        classifier.fit(replicas)

        return classifier
