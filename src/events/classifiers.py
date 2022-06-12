import pandas as pd

from events import Event
from replicas import ReplicasContainer, Replica

from replicas.classifiers import AbstractEventClassifier, NeighbourClassifier
from utils.vectorizer import AbstractVectorizer, get_sentence_vectorizer


class EventClassifier:
    def __init__(
        self,
        replicas: ReplicasContainer,
        text_classifier: AbstractEventClassifier = None,
        sentence_vectorizer: AbstractVectorizer = None,
    ) -> None:
        sentence_vectorizer = sentence_vectorizer or get_sentence_vectorizer()

        self.replicas = replicas
        self.event_classifier = text_classifier or NeighbourClassifier.from_replicas_container(
            self.replicas,
            sentence_vectorizer,
        )

    def predict(self, sentence: str) -> Event:
        replica = Replica.from_sentence(sentence)
        event = self.event_classifier.classify(replica)
        return event

    @staticmethod
    def default():
        df = pd.read_csv('./events/data/replicas-events.csv', sep=';')
        question_df = pd.read_csv('./informations/data/question_answer.csv', sep=';')
        question_df['класс'] = [Event.INFORMATION.value for _ in range(question_df.shape[0])]
        question_df['реплика'] = question_df['question']
        df = pd.concat([df, question_df])

        replica_container = ReplicasContainer()
        replica_container.extend(df['реплика'], list(map(Event.from_number, df['класс'])))

        event_classifier = EventClassifier(replica_container)

        return event_classifier
