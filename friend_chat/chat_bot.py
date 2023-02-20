# -*- coding:utf-8 -*-
"""

@Auther: niu
@FileName: chat_bot.py
@Introduction: 

"""

import openai
import config

from tools.io import read_dialog
from friend_chat.interface.chat_bot import ChatBotInterface, ChatBotManagerInterface
from friend_chat.dialog import PromptQueue, CorpusQueue, Dialog

openai.api_key = config.OPENAI_API_KEY


class FriendChatBot(ChatBotInterface):
    def __init__(self):
        self._max_tokens = 2048
        self._u_prefix = "You: "
        self._me_prefix = "Friend: "
        self._prop_q = PromptQueue(max_size=self._max_tokens, u_prefix=self._u_prefix, me_prefix=self._me_prefix)
        self._corp_q = CorpusQueue(u_prefix=self._u_prefix, me_prefix=self._me_prefix)

    def __del__(self):
        """用于抛出异常后保存临时会话"""
        with open("conversation.tmp", "w", encoding="utf-8") as fw:
            fw.write(self._corp_q.to_corpus())

    def load(self, filepath: str, show: bool = False) -> None:
        with open(filepath, "r", encoding="utf-8") as fr:
            dialog = fr.read()
        if show:
            print(dialog)
            print("----以上是历史消息----")
        rows = read_dialog(dialog, self._u_prefix, self._me_prefix)
        for me, text in rows:
            dia = Dialog(me=me, string=text)
            self._prop_q.push(dia)
            self._corp_q.push(dia)


    def save(self, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as fw:
            fw.write(self._corp_q.to_corpus())

    def send(self, message: str) -> str:
        dia = Dialog(me=False, string=message)
        self._prop_q.push(dia)
        self._corp_q.push(dia)

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=self._prop_q.to_prompt(),
            temperature=0.5,
            max_tokens=self._max_tokens,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
            stop=[self._u_prefix]
        )

        resp = response.to_dict()["choices"][0].to_dict()["text"]
        resp = resp.replace("\n", "")
        resp = resp.replace(" ", "")
        dia = Dialog(me=True, string=resp)
        self._prop_q.push(dia)
        self._corp_q.push(dia)
        return resp


class ChatBotManager(metaclass=ChatBotManagerInterface):
    def __init__(self):
        self._d = {}

    def get(self, user_id: int) -> FriendChatBot:
        if user_id not in self._d:
            self._d[user_id] = FriendChatBot()
        return self._d[user_id]
