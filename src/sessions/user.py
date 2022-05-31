import datetime

from typing import List
from sessions.stages import Stages
from sessions.scenarios import (
    EventClassificationHandler,
    DiseaseClassificationHandler,
    InformationHandler,
    ConversationBotHandler
)

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
            timestamp: int = None
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
            'stage': self.stage.name
        }


class UserSession:
    actions: List[Action]
    require_history_actions: List[Stages] = [Stages.consultation]

    def __init__(self, user_id: int, stage=Stages.intro):
        self.user_id = user_id
        self.stage = stage
        self.actions = []

    def add_action(self, action: Action):
        self.actions.append(action)

    def get_previous_message(self, message) -> str:
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
        handler = HANDLERS[self.stage]
        response = handler.handle(message)

        self.add_action(Action.message_action(message, stage=self.stage))
        self.add_action(Action.message_action(response.message, stage=self.stage, author='bot'))

        self.stage = response.next_stage

        return response.message

    def process_action(self, action_name: str) -> str:
        answer = 'Извините, я не знаю такого действия'

        if action_name == 'like':
            self.add_action(Action.like_action(self.stage))
            answer = 'Спасибо, мы учтли!'
        elif action_name == 'dislike':
            self.add_action(Action.dislike_action(self.stage))
            answer = 'Хорошо, мы учтем! Попытаемся исправится в следующем обновлении'
        elif action_name == 'switch_to_operator':
            self.add_action(Action.switch_to_operator_action(self.stage))
            self.stage = Stages.intro
            answer = 'Хорошо, переключаю на оператора...'
        elif action_name == 'break_conversation':
            self.add_action(Action.break_action(self.stage))
            self.stage = Stages.intro
            answer = 'Вы остановили общение. Хорошего дня!'

        self.add_action(Action.message_action(
            message=answer,
            stage=self.stage,
            author='bot'
        ))

        return answer

    def serialize(self):
        return {
            'user_id': self.user_id,
            'stage': self.stage.name,
            'actions': [action.serialize() for action in self.actions],
        }

    @staticmethod
    def from_json(json_content: dict) -> 'UserSession':
        user_session = UserSession(
            user_id=json_content['user_id'],
            stage=Stages[json_content['stage']]
        )

        for action_json in json_content['actions']:
            user_session.add_action(Action(
                content=action_json['content'],
                code=action_json['code'],
                author=action_json.get('author', 'user'),
                stage=Stages[action_json.get('stage', Stages.unknown.name)],
                timestamp=action_json['timestamp']
            ))

        return user_session
