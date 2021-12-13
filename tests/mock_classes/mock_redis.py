# pylint: disable=missing-docstring

from typing import Any, Optional

class MockRedis:

    in_memory_db: dict = {}

    def hset(self, h_name: str, key: str, value) -> None:
        assert isinstance(h_name, str)
        assert isinstance(key, str)
        assert value is not None

        if h_name not in self.in_memory_db:
            self.in_memory_db[h_name] = {}

        self.in_memory_db[h_name][key] = value

    def exists(self, h_name: str) -> bool:
        assert isinstance(h_name, str)
        return h_name in self.in_memory_db

    def hget(self, h_name: str, arg: str) -> Any:
        assert isinstance(h_name, str)
        assert isinstance(arg, str)
        return self.in_memory_db[h_name][arg]

    def delete(self, h_name: str) -> None:
        del self.in_memory_db[h_name]
