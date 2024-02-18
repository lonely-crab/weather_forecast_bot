import redis
from typing import Any
import json
from telebot.types import Message
from datetime import datetime
import re

redis_db = redis.Redis(host="localhost", port=6379, db=0)


def _set_redis(user_id: str, key: str, value: dict | str) -> None:
    value = {key: value}
    old_value = json.loads(redis_db.get(user_id))
    if isinstance(old_value, list):
        old_value.append(value)
    else:
        old_value.update(value)
    new_value = json.dumps(old_value)
    redis_db.set(user_id, new_value)


def _get_redis(user_id: str, key: str) -> Any:
    value = json.loads(redis_db.get(user_id)).get(key)
    return value


def _delete_user(user_id: str | int) -> None:
    redis_db.delete(user_id)


def _delete_redis(user_id: str | int, key: str) -> None:
    value = json.loads(redis_db.get(user_id))
    value.pop(key)
    new_value = json.dumps(value)
    redis_db.set(user_id, new_value)


def _add_history(user_id: str | int, message: Message) -> None:
    message_text = message.text.join(["'", "'"])
    message_text = re.sub(r"\n", " ", message_text)
    history = " : ".join(
        [str(datetime.fromtimestamp(message.date)), message_text]
    )
    old_history = json.loads(redis_db.get(user_id)).get("history", [])
    if isinstance(old_history, str):
        old_history = json.loads(old_history)
    old_history.append(history)
    new_history = json.dumps(old_history)
    RedisDatabaseInterface.set_redis(user_id, "history", new_history)


class RedisDatabaseInterface:
    @classmethod
    def set_user(cls, user_id: str | int) -> None:
        redis_db.set(user_id, json.dumps({}))

    @classmethod
    def set_redis(
        cls, user_id: str | int, key: str, value: dict | str
    ) -> None:
        _set_redis(user_id, key, value)

    @classmethod
    def get_redis(cls, user_id: str | int, key: str) -> Any:
        return _get_redis(user_id, key)

    @classmethod
    def delete_user(cls, user_id: str | int) -> None:
        _delete_user(user_id)

    @classmethod
    def delete_redis(cls, user_id: str | int, key: str) -> None:
        _delete_redis(user_id, key)

    @classmethod
    def add_history(cls, user_id: str | int, message: Message) -> None:
        _add_history(user_id, message)
