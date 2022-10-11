from typing import List

from events import Event


class Replica:
    def __init__(self, sentence: str, event: Event = Event.COMMON) -> None:
        self.sentence = sentence
        self.event = event

    def __hash__(self):
        return self.sentence.__hash__()

    @staticmethod
    def from_sentence(sentence: str) -> "Replica":
        return Replica(sentence, Event.OFF_TOP)


class ReplicasContainer:
    def __init__(self, replicas: List[Replica] = None) -> None:
        self.replicas = replicas or []

    def extend(self, sentences: List[str], event_types: List[Event]):
        replicas = [
            Replica(sentence, event_type)
            for sentence, event_type in zip(sentences, event_types)
        ]
        self.replicas.extend(replicas)

    def __getitem__(self, item: int) -> Replica:
        return self.replicas[item]
