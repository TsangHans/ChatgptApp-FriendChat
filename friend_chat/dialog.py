# -*- coding:utf-8 -*-
"""

@Auther: niu
@FileName: dialog.py
@Introduction: 

"""
from collections import deque
from typing import List

from friend_chat.interface.dialog import Dialog, PromptQueueInterface, CorpusQueueInterface


class PromptQueue(PromptQueueInterface):
    def __init__(self, max_size: int, u_prefix: str, me_prefix: str):
        self._encoding = "utf-8"

        self._size = len(me_prefix.encode(self._encoding))
        self._dq: deque[Dialog] = deque()
        self._max_size = max_size
        self._u_prefix = u_prefix
        self._me_prefix = me_prefix

    def _get_dialog_size(self, dialog: Dialog):
        return (len(dialog.string.encode(self._encoding)) + (
            len(self._me_prefix.encode(self._encoding)) if dialog.me else len(self._u_prefix.encode(self._encoding)))
                ) + len("\n".encode(self._encoding))

    def push(self, dialog: Dialog) -> None:
        self._dq.append(dialog)
        self._size += self._get_dialog_size(dialog)

        diff = self._size - self._max_size
        if diff > 0:
            while self._size > self._max_size:
                del_dialog = self._dq.popleft()
                self._size -= self._get_dialog_size(del_dialog)

    def to_prompt(self) -> str:
        res = ""
        for dialog in self._dq:
            res += self._me_prefix if dialog.me else self._u_prefix
            res += dialog.string
            res += "\n"

        res += self._me_prefix
        return res


class CorpusQueue(CorpusQueueInterface):
    def __init__(self, u_prefix: str, me_prefix: str):
        self._encoding = "utf-8"

        self._size = len(me_prefix.encode(self._encoding))
        self._q: List[Dialog] = []
        self._u_prefix = u_prefix
        self._me_prefix = me_prefix

    def push(self, dialog: Dialog) -> None:
        self._q.append(dialog)

    def to_corpus(self) -> str:
        res = ""
        for dialog in self._q:
            if self._q[-1].me or dialog != self._q[-1]:
                res += self._me_prefix if dialog.me else self._u_prefix
                res += dialog.string
            if dialog != self._q[-1]:
                res += "\n"
        return res
