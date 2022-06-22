import datetime

from typing import List
from langdetect import detect
from sessions.stages import Stages
from sessions.scenarios import (
    Response,
    EventClassificationHandler,
    DiseaseClassificationHandler,
    InformationHandler,
    ConversationBotHandler
)
from sessions.multilanguage import action_responses, bot_responses
from utils.multilanguage import translate_word

HANDLERS = {
    Stages.intro: EventClassificationHandler(),
    Stages.consultation: DiseaseClassificationHandler(),
    Stages.off_top: ConversationBotHandler(),
    Stages.information: InformationHandler(),
}


class Action:
    def __init__(
            self,
            stage: Stages = None,
            content: str = None,
            code: str = None,
            author: str = None,
            timestamp: int = None,
    ):
        self.code = code
        self.content = content
        self.author = author or 'user'
        self.stage = stage or Stages.unknown
        self.timestamp = timestamp or int(datetime.datetime.now().timestamp())

    @staticmethod
    def message_action(message: str, stage: Stages = None, author: str = None) -> 'Action':
        return Action(stage=stage, content=message, code='message', author=author)

    @staticmethod
    def like_action(stage: Stages = None) -> 'Action':
        return Action(stage=stage, code='like')

    @staticmethod
    def dislike_action(stage: Stages = None) -> 'Action':
        return Action(stage=stage, code='dislike')

    @staticmethod
    def switch_to_operator_action(stage: Stages = None) -> 'Action':
        return Action(stage=stage, code='switch_to_operator')

    @staticmethod
    def break_action(stage: Stages = None) -> 'Action':
        return Action(stage=stage, code='break')

    def serialize(self):
        return {
            'code': self.code,
            'content': self.content,
            'timestamp': self.timestamp,
            'author': self.author,
            'stage': self.stage.name,
        }


class UserSession:
    actions: List[Action]
    require_history_actions: List[Stages] = [Stages.consultation]

    def __init__(self, user_id: int, stage: Stages = Stages.intro, language: str = None):
        self.user_id = user_id
        self.stage = stage
        self.language = language
        self.actions = []

    def add_action(self, action: Action):
        self.actions.append(action)

    def get_previous_message(self, message: str) -> str:
        if self.stage in self.require_history_actions:
            previous_messages = []

            for action in reversed(self.actions):
                if (
                    action.stage == self.stage and
                    action.author == 'user'
                ):
                    previous_messages.append(action.content)
                else:
                    break

            message += ' ' + ' '.join(previous_messages)

        return message

    def get_response(self, message: str) -> str:
        message = self.get_previous_message(message)
        self.language = detect(message)
        
        handler = HANDLERS[self.stage]
        
        try:
            response = handler.handle(message)
        except Exception as e:
            response = Response(
                message=bot_responses['internal_error'].format(error=e),
                next_stage=self.stage
            )

        if not isinstance(response.message, str):
            response_message = response.message.get_response(self.language)
        else:
            response_message = response.message

        self.add_action(Action.message_action(message, stage=self.stage))
        self.add_action(Action.message_action(response_message, stage=self.stage, author='bot'))

        self.stage = response.next_stage
        
        if self.language == 'en':
            response_message = translate_word(response_message)

        return response_message

    def process_action(self, action_name: str) -> str:
        if action_name == 'like':
            self.add_action(Action.like_action(self.stage))
        elif action_name == 'dislike':
            self.add_action(Action.dislike_action(self.stage))
        elif action_name == 'switch_to_operator':
            self.add_action(Action.switch_to_operator_action(self.stage))
            self.stage = Stages.intro
        elif action_name == 'break_conversation':
            self.add_action(Action.break_action(self.stage))
            self.stage = Stages.intro
        
        response = action_responses.get(action_name, 'do_not_know')

        if not isinstance(response, str):
            response_message = response.get_response(self.language or 'en')
        else:
            response_message = response

        self.add_action(Action.message_action(
            message=response_message,
            stage=self.stage,
            author='bot'
        ))

        return response_message

    def serialize(self):
        return {
            'user_id': self.user_id,
            'language': self.language,
            'stage': self.stage.name,
            'actions': [action.serialize() for action in self.actions],
        }

    @staticmethod
    def from_json(json_content: dict) -> 'UserSession':
        user_session = UserSession(
            user_id=json_content['user_id'],
            stage=Stages[json_content['stage']],
            language=json_content['language']
        )

        for action_json in json_content['actions']:
            user_session.add_action(Action(
                content=action_json['content'],
                code=action_json['code'],
                author=action_json.get('author', 'user'),
                stage=Stages[action_json.get('stage', Stages.unknown.name)],
                timestamp=action_json['timestamp'],
            ))

        return user_session
