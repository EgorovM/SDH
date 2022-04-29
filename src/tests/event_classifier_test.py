import pandas as pd
import pytest

from replicas import ReplicasContainer
from events import Event
from events.classifiers import EventClassifier


@pytest.mark.parametrize('sentence,event', [
    ('бесишь', Event.OFF_TOP),
    ('у меня болит голова', Event.INFORMATION),
    ('хочу записаться к врачу', Event.CONSULTATION),
])
def test_event_classifier(sentence: str, event: Event):
    df = pd.read_csv('../events/data/replicas-events.csv', sep=';')

    replica_container = ReplicasContainer()
    replica_container.extend(df['реплика'], df['класс'])

    event_classifier = EventClassifier(replica_container)

    assert event_classifier.predict(sentence) == event
