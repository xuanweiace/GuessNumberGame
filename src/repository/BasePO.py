
# 其他所有的PO都是他的子类，为了方便crud的时候接口统一
class BasePO:
    def __init__(self, id, name, type) -> None:
        self.id = id
        self.name = name
        self.type = type
        
    
    