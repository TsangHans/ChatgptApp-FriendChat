"""
create_time: 2023/2/20 16:50
author: TsangHans

从零开始一个会话
"""
from friend_chat import FriendChatBot

if __name__ == "__main__":
    convs_save_fp = "demo_corpus/demo_corpus_1"

    fcb = FriendChatBot()
    while True:
        message = input("You: ")
        if message == "\q":
            fcb.save(convs_save_fp)
            break
        resp = fcb.send(message)
        print("Friend:", resp)