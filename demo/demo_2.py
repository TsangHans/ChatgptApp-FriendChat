"""
create_time: 2023/2/20 17:10
author: TsangHans

加载上一次的对话，并从那儿继续
"""
from friend_chat import FriendChatBot

if __name__ == "__main__":
    last_convs_fp = "demo_corpus/demo_corpus_1"
    convs_save_fp = "demo_corpus/demo_corpus_2"
    fcb = FriendChatBot()
    fcb.load(last_convs_fp, show=True)
    while True:
        message = input("You: ")
        if message == "\q":
            fcb.save(convs_save_fp)
            break
        resp = fcb.send(message)
        print("Friend:", resp)