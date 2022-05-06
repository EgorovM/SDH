import datetime

from typing import List
from sessions.stages import Stages
from sessions.scenarios import (
    EventClassificationHandler,
    DiseaseClassificationHandler
)

HANDLERS = {
    Stages.intro: EventClassificationHandler(),
    Stages.consultation: DiseaseClassificationHandler(),
    Stages.off_top: EventClassificationHandler(),
    Stages.information: EventClassificationHandler(),
}


class Action:
    def __init__(self, content=None, code=None):
        self.code = code
        self.content = content
        self.timestamp = int(datetime.datetime.now().timestamp())

    @staticmethod
    def message_action(message: str):
        return Action(content=message, code='message')

    def serialize(self):
        return {
            'code': self.code,
            'content': self.content,
            'timestamp': self.timestamp
        }


class UserSession:
    actions: List[Action]

    def __init__(self, user_id: int, stage=Stages.intro):
        self.user_id = user_id
        self.stage = stage
        self.actions = []

    def add_action(self, action: Action):
        self.actions.append(action)

    def get_response(self, message: str) -> str:
        handler = HANDLERS[self.stage]
        response = handler.handle(message)

        self.stage = response.next_stage
        self.add_action(Action.message_action(message))

        return response.message

    def serialize(self):
        return {
            'user_id': self.user_id,
            'stage': self.stage.value,
            'actions': [action.serialize() for action in self.actions],
        }

    @staticmethod
    def from_json(json_content: dict) -> 'UserSession':
        user_session = UserSession(
            user_id=json_content['user_id'],
            stage=Stages(json_content['stage'])
        )

        for action_json in json_content['actions']:
            user_session.add_action(Action(
                content=action_json['content'], code=action_json['code']
            ))

        return user_session
