# -*- coding:utf-8 -*-
"""

@Auther: niu
@FileName: chat_bot.py
@Introduction: 

"""
from abc import ABC, abstractmethod


class ChatBotInterface(ABC):

    @abstractmethod
    def load(self, filepath: str, show: bool = False) -> None:
        pass

    @abstractmethod
    def save(self, filepath: str) -> None:
        pass

    @abstractmethod
    def send(self, prompt: str) -> str:
        pass


class ChatBotManagerInterface(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    def get(self, user_id: str) -> ChatBotInterface:
        raise NotImplementedError()
