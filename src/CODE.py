from ER import *


REQ_SUCCESS = 20000


def pack_success_dict(data: dict):
    return {"code":20000, "msg": "success", "data": data}

def pack_err_dict(code: int, msg: str):
    return {"code":code, "msg": msg, "data": None}
