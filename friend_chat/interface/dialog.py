# -*- coding:utf-8 -*-
"""

@Auther: niu
@FileName: dialog.py
@Introduction: 

"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Dialog:
    me: bool  # 表示是否本人的对话
    string: str  # 表示对话内容


class DialogQueueInterface(ABC):
    """
    固定容量的对话队列，当加入新对话时，判断队列容量是否溢出，如果容量溢出则溢出最小个数的最早加入的对话，
    """

    @abstractmethod
    def push(self, dialog: Dialog) -> None:
        pass


class CorpusQueueInterface(DialogQueueInterface):

    @abstractmethod
    def to_corpus(self) -> str:
        pass


class PromptQueueInterface(DialogQueueInterface):

    @abstractmethod
    def to_prompt(self) -> str:
        pass
