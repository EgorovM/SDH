from events import Event
from replicas import ReplicasContainer, Replica

from replicas.classifiers import AbstractEventClassifier, CosineDistanceEventClassifier
from utils.vectorizer import AbstractVectorizer, SentenceTfIdfVectorizer


class EventClassifier:
    def __init__(
        self,
        replicas: ReplicasContainer,
        text_classifier: AbstractEventClassifier = None,
        sentence_vectorizer: AbstractVectorizer = None,
    ) -> None:
        sentence_vectorizer = sentence_vectorizer or SentenceTfIdfVectorizer.default()

        self.replicas = replicas
        self.event_classifier = text_classifier or CosineDistanceEventClassifier.from_replicas_container(
            self.replicas,
            sentence_vectorizer,
        )

    def predict(self, sentence: str) -> Event:
        replica = Replica.from_sentence(sentence)
        event = self.event_classifier.classify(replica)
        return event
