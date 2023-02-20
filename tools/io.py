"""
create_time: 2023/2/17 14:31
author: TsangHans
"""
from typing import List, Tuple


def read_dialog(dialog: str, u_prefix, me_prefix) -> List[Tuple[bool, str]]:
    """两人的对话，每行表示一次发言，每一次发言内没有多余的换行符。"""
    rows = dialog.split("\n")
    res = []
    for r in rows:
        # 开头为 u_prefix 视为人类的发言，开头为 me_prefix 视为 bot 的发言
        if r.startswith(u_prefix):
            me = False
        elif r.startswith(me_prefix):
            me = True
        else:
            raise ValueError(f"Unmatch prefix in dialog ' {r} '.")
        if me:
            text = r[len(me_prefix):]
        else:
            text = r[len(u_prefix):]
        res.append((me, text))
    return res
