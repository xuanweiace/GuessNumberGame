from enum import Enum
import json

__all__ = ["FixedTypeListException", "FixedTypeList", "load_from_json", "dump_to_json"]


class FixedTypeListException(Exception):
    pass


class FixedTypeList(list):
    def __init__(self, element_type, *args):
        self.element_type = element_type
        list.__init__(self, *args)

    def __setitem__(self, ind, val):
        self.__check_insert_obj_type(val)
        list.__setitem__(self, ind, val)

    def insert(self, idx, val):
        self.__check_insert_obj_type(val)
        list.insert(self, idx, val)

    def append(self, val):
        self.__check_insert_obj_type(val)
        list.append(self, val)

    def __check_insert_obj_type(self, obj):
        if not isinstance(obj, self.element_type):
            raise FixedTypeListException(
                'object to be inserted is not same of element_type, %s, %s'
                % (str(type(obj)), str(self.element_type)))


def load_from_json(obj, json_str, input_encoding='utf-8'):
    '''
    obj表示预期转换成的对象
    input_encoding表示输入json字符串的编码格式
    '''
    # json_object = json.loads(json_str, input_encoding)
    json_object = json.loads(json_str)
    return _load_from_json_object(obj, json_object)

def load_from_json_obj(obj, json_obj):
    return _load_from_json_object(obj, json_obj)


def dump_to_json(obj, outpu_encoding='utf-8', no_extra_space=True,  output_bytes=False):
    '''
    obj为需要dump的对象
    output_encoding为输出json字符串的编码格式
    no_extra_space为True, 表示紧凑格式输出，不输出多余的空格
    '''
    json_object = _dump_to_json_object(obj)
    sep = (',', ':') if no_extra_space else None
    res = json.dumps(json_object, ensure_ascii=False,
            separators=sep)
    if output_bytes:
        return res.encode(outpu_encoding)
    return res

def dump_to_json_obj(obj):
    return _dump_to_json_object(obj)
    

def _is_native_json_type(obj):
    return obj is None or isinstance(obj, bool) \
            or isinstance(obj, str) \
            or isinstance(obj, float) \
            or isinstance(obj, int)


def _load_from_json_object(obj, json_object):
    if isinstance(obj, Enum):# 增加对枚举的支持，必须放在最前面，不然就进dict的逻辑了
        return obj.__class__(json_object["value"])
    elif isinstance(json_object, dict):
        return _load_from_json_dict(obj, json_object)
    elif isinstance(json_object, list):
        return _load_from_json_array(obj, json_object)
    else:
        return json_object


def _load_from_json_dict(obj, json_dict):
    for (k, v) in json_dict.items():
        if not hasattr(obj, k):
            raise ValueError("obj[%s] has no attribute[%s]" %
                    (str(type(obj)), k))
        subobj = getattr(obj, k)
        subobj = _load_from_json_object(subobj, v)
        
        setattr(obj, k, subobj)
    return obj


def _load_from_json_array(array_obj, json_array):
    if isinstance(array_obj, FixedTypeList):
        element_type = array_obj.element_type
        for json_element in json_array:
            element_obj = _load_from_json_object(element_type(), json_element)
            array_obj.append(element_obj)
    else:
        raise ValueError('must use FixedTypeList to store json array')
    return array_obj


def _dump_to_json_object(obj):
    if isinstance(obj, list):
        return _dump_array(obj)
    elif _is_native_json_type(obj):
        return obj
    else:
        return _dump_custom_object(obj)


def _dump_array(obj):
    sub_obj_list = []
    for s in obj:
        sub_obj_list.append(_dump_to_json_object(s))
    return sub_obj_list


def _dump_custom_object(obj):
    attr_list = [attr for attr in dir(obj)
                 if not attr.startswith('__')
                    and not callable(getattr(obj, attr))]
    json_object = {}
    for attr_name in attr_list:
        subobj = getattr(obj, attr_name)
        json_object[attr_name] = _dump_to_json_object(subobj)
    return json_object