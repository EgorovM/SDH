from pymongo.database import Database
from pymongo.results import UpdateResult

from sessions.user import UserSession


def insert_user_session(db: Database, user_session: UserSession) -> UpdateResult:
    json_content = user_session.serialize()

    return db.user_sessions.update_one(
        {"user_id": user_session.user_id}, {"$set": json_content}, True
    )


def get_user_session_by_id(db: Database, user_id: int) -> UserSession:
    # TODO: добавить сессию по времени
    json_content = db.user_sessions.find_one({"user_id": user_id})

    if not json_content:
        return UserSession(user_id=user_id)

    user_session = UserSession.from_json(json_content)

    return user_session
