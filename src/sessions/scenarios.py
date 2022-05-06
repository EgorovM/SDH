from abc import ABC, abstractmethod
from diseases import Disease
from diseases.classificators import DiseasesClassification
from events.classifiers import EventClassifier
from events import Event
from sessions.stages import Stages


class Response:
    def __init__(self, message: str, next_stage: Stages):
        self.message = message
        self.next_stage = next_stage


class AbstractHandler(ABC):
    @abstractmethod
    def handle(self, message: str) -> Response:
        pass

    @abstractmethod
    def next_stage(self, *args, **kwargs) -> Stages:
        pass

    @abstractmethod
    def get_human_readable(self, *args, **kwargs) -> str:
        pass

    @property
    @abstractmethod
    def code(self):
        return 'abstract_code'


class EventClassificationHandler(AbstractHandler):
    def __init__(self):
        self.classifier = EventClassifier.default()

    def next_stage(self, event: Event) -> Stages:
        if event == Event.INFORMATION:
            return Stages.information

        if event == Event.OFF_TOP:
            return Stages.off_top

        if event == Event.CONSULTATION:
            return Stages.consultation

        return Stages.intro

    def get_human_readable(self, event: Event) -> str:
        # TODO: переписать, чтобы можно было вручную эти ответы добавлять
        if event == Event.OFF_TOP:
            return 'Привет! Расскажи как дела?'

        if event == Event.CONSULTATION:
            return 'Привет! Расскажи подробнее про свои симптомы, пожалуйста'

        if event == Event.INFORMATION:
            # TODO: сразу взять ответ
            return 'Привет! Сейчас найду...'

        return 'Извините, я вас не понимаю. Попробуйте, пожалуйста, уточнить вопрос :)'

    def handle(self, message: str) -> Response:
        event = self.classifier.predict(message)
        response = Response(
            message=self.get_human_readable(event),
            next_stage=self.next_stage(event)
        )
        return response

    def code(self):
        return 'event_classification'


class DiseaseClassificationHandler(AbstractHandler):
    def __init__(self):
        self.classifier = DiseasesClassification()
        self.proba_threshold = 0.4

    def get_human_readable(self, disease: Disease, probability: float) -> str:
        if probability > self.proba_threshold:
            return f'У вас кажется {disease.name} с вероятностью {round(probability, 3)}. Лечитесь, не болейте!'

        # TODO: вычлинять симптомы и их справшивать
        return f'Расскажите еще что-нибудь, пожалуйста.'

    def next_stage(self, probability) -> Stages:
        if probability > self.proba_threshold:
            return Stages.intro

        return Stages.consultation

    def handle(self, message: str) -> Response:
        disease, probability = self.classifier.most_possible_disease(message)
        response = Response(
            message=self.get_human_readable(disease, probability),
            next_stage=self.next_stage(probability)
        )
        return response

    def code(self):
        return 'disease_classification'

