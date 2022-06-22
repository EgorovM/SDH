from abc import ABC, abstractmethod
from itertools import compress

from conversation import ConversationBot
from diseases import Disease
from diseases.classificators import DiseasesClassification
from diseases.symptoms import SYMPTOMS_NAMES
from events import Event
from events.classifiers import EventClassifier
from informations import QuestionAnswer
from sessions.stages import Stages
from sessions.multilanguage import BotResponse, bot_responses


information_question_answer = QuestionAnswer.default()
conversation_bot = ConversationBot()


class Response:
    def __init__(self, message: BotResponse, next_stage: Stages):
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
    def code(self) -> str:
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
            return bot_responses['start_off_top']

        if event == Event.CONSULTATION:
            return bot_responses['start_consultation']

        if event == Event.INFORMATION:
            return bot_responses['start_information']

        return bot_responses['do_not_know']

    def handle(self, message: str) -> Response:
        event = self.classifier.predict(message)

        if event == Event.INFORMATION:
            return InformationHandler().handle(message)

        response = Response(
            message=self.get_human_readable(event),
            next_stage=self.next_stage(event)
        )

        return response

    def code(self) -> str:
        return 'event_classification'


class DiseaseClassificationHandler(AbstractHandler):
    def __init__(self):
        self.classifier = DiseasesClassification()
        self.proba_threshold = 0.5

    def get_human_readable(self, message: str, disease: Disease, probability: float) -> str:
        if probability > self.proba_threshold:
            # TODO: как бот пришел к такому выводу
            symptoms_indexes = self.classifier.text_to_vector(message).toarray()[0]
            symptoms = compress(SYMPTOMS_NAMES, symptoms_indexes)

            disease_response = bot_responses['disease_review'].format(
                disease_name=disease.name,
                disease_probability=int(round(probability, 2) * 100),
            )
            detail_response = bot_responses.get(
                f'{disease.name}_details', 
                bot_responses['default_details']).format(
                symptoms_list=', '.join(symptoms)
            )

            return disease_response + detail_response

        symptom = self.classifier.find_symptom_to_ask(message)

        return symptom.question

    def next_stage(self, probability) -> Stages:
        if probability > self.proba_threshold:
            return Stages.intro

        return Stages.consultation

    def handle(self, message: str) -> Response:
        disease, probability = self.classifier.most_possible_disease(message)
        response = Response(
            message=self.get_human_readable(message, disease, probability),
            next_stage=self.next_stage(probability)
        )
        return response

    def code(self) -> str:
        return 'disease_classification'


class InformationHandler(AbstractHandler):
    def __init__(self):
        self.score_threshold = 0.85

    def handle(self, message: str) -> Response:
        response = Response(
            message=self.get_human_readable(message),
            next_stage=self.next_stage()
        )
        return response

    def next_stage(self, *args, **kwargs) -> Stages:
        return Stages.intro

    def get_human_readable(self, message: str) -> str:
        answer, score = information_question_answer.predict(message)

        if score < self.score_threshold:
            return bot_responses['cant_answer_information']

        return answer

    def code(self) -> str:
        return 'information'


class ConversationBotHandler(AbstractHandler):
    def handle(self, message: str) -> Response:
        return Response(
            message=self.get_human_readable(message),
            next_stage=self.next_stage()
        )

    def next_stage(self, *args, **kwargs) -> Stages:
        # TODO: придумать как выходить из бота
        return Stages.off_top

    def get_human_readable(self, message) -> str:
        return conversation_bot.get_answer(message)

    @property
    def code(self) -> str:
        return 'conversation_bot'
