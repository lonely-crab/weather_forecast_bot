import redis
from typing import Any
import json


redis_db = redis.Redis(host='localhost', port=6379, db=0)


def _set_redis(user_id: str, key: str, value: dict | str) -> None:
    value = {key: value}
    old_value = json.loads(redis_db.get(user_id))
    old_value.update(value)
    new_value = json.dumps(old_value)
    redis_db.set(user_id, new_value)


def _get_redis(user_id: str, key: str) -> Any:
    value = json.loads(redis_db.get(user_id)).get(key)
    return value


def _delete_user(user_id: str) -> None:
    redis_db.delete(user_id)


def _delete_redis(user_id: str, key: str) -> None:
    value = json.loads(redis_db.get(user_id))
    value.pop(key)
    new_value = json.dumps(value)
    redis_db.set(user_id, new_value)

class RedisDatabaseInterface:
    @classmethod
    def set_user(cls, user_id) -> None:
        redis_db.set(user_id, json.dumps({}))

    @classmethod
    def set_redis(cls, user_id, key, value) -> None:
        _set_redis(user_id, key, value)

    @classmethod
    def get_redis(cls, user_id, key) -> Any:
        return _get_redis(user_id, key)

    @classmethod
    def delete_user(cls, user_id) -> None:
        _delete_user(user_id)

    @classmethod
    def delete_redis(cls, user_id, key) -> None:
        _delete_redis(user_id, key)


# # print(_get_redis("395159496", "location"))
# RedisDatabaseInterface.set_user("395159496")
# print(redis_db.get("395159496"))
# _set_redis("395159496", "location", {"latitude": 0.0, "longitude": 0.0})
