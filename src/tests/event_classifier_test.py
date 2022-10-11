import pytest

from events import Event
from events.classifiers import EventClassifier


@pytest.mark.parametrize(
    "sentence,event",
    [
        ("бесишь", Event.OFF_TOP),
        ("у меня болит голова", Event.INFORMATION),
        ("хочу записаться к врачу", Event.CONSULTATION),
    ],
)
def test_event_classifier(sentence: str, event: Event):
    event_classifier = EventClassifier.default()

    assert event_classifier.predict(sentence) == event
