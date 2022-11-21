from ER import *


REQ_SUCCESS = 20000
NOTIFY = 21000

def pack_success_dict(data: dict):
    return {"code":REQ_SUCCESS, "msg": "success", "data": data}

def pack_err_dict(code: int, msg: str):
    return {"code":code, "msg": msg, "data": None}

def pack_notify_dict(api:str, data:dict):
    return {"api":api, "code":NOTIFY, "msg": "success", "data": data}