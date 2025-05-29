#encoding: utf-8
import os, json, functools

class ParseObject:
    def __init__(self, obj, flatten: bool=False, ignore: bool=False, unlist: bool=False):
        self.obj = obj
        self.flatten: bool = flatten
        self.ignore: bool = ignore
        self.unlist: bool = unlist
        
    def __repr__(self):
        return str(self.__dict__)
        
    def make(obj):
        if not isinstance(obj, ParseObject):
            return ParseObject(obj)
        else:
            return obj

def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        ret = json.load(f)
        print(f"载入 {filename} -> {len(ret)} Items.")
        return ret
        
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ParseObject):
            return obj.obj
        else:
            return super().default(obj)

# 判断ops里记录的操作类型
def parse_op(op, pobj: ParseObject) -> ParseObject:
    if isinstance(op, dict):
        # 嵌套操作：进入
        return map_value(lambda x: parse_dict(op, x), pobj)
    elif isinstance(op, list):
        # 列表操作：依次执行
        ret = pobj
        for o in op:
            ret = parse_op(o, ret)
            if not ret.obj:
                break
        return ret
    elif isinstance(op, str):
        # 单个操作：执行
        meth = f"do_{op}"
        return globals()[meth](pobj)

# 判断pobj类型决定是对单还是对群（？
def map_value(fn, pobj: ParseObject) -> ParseObject:
    if not pobj.obj:
        return ParseObject(None)
    elif isinstance(pobj.obj, list):
        return ParseObject([fn(ParseObject(x)) for x in pobj.obj])
    else:
        return fn(pobj)
		
def do_ignore(pobj: ParseObject) -> ParseObject:
    pobj.ignore = True
    return pobj

def do_flatten(pobj: ParseObject) -> ParseObject:
	pobj.flatten = True
	return pobj

# { a: ... } => ...	 展开只有一项的dict/list
def do_extract(pobj: ParseObject) -> ParseObject:
    if pobj.obj == None:
        return pobj
    elif isinstance(pobj.obj, dict) and len(pobj.obj) == 1:
        print("extract dict:", next(iter(pobj.obj.keys())))
        ret = next(iter(pobj.obj.values()))
        return ParseObject.make(ret)
    elif isinstance(pobj.obj, list) and len(pobj.obj) == 1:
        print("extract list")
        return ParseObject.make(pobj.obj[0])
    else:
        print("Not a len=1 dict/list", pobj)
        raise
        
# [ a ] -> a
def do_unlist(pobj: ParseObject) -> ParseObject:
    pobj.unlist = True
    return pobj
    
# [ { key, value, valueStr } ...] => { key: value/valueStr ... }
def do_parse_blackboard(pobj: ParseObject):
    #print("parse_blackboard", pobj)
    ret = {}
    for item in pobj.obj:
        if item.get("valueStr", None):
            ret[item["key"]] = item["valueStr"]
        else:
            ret[item["key"]] = item["value"]
    return ParseObject(ret)

# [ {"count", "id", "type" } ] -> { "id": "count" ... }
# 不调用map_value（通用的数组处理）
def do_parse_cost(pobj: ParseObject) -> ParseObject:
    #print("parse_cost", pobj)
    if not pobj.obj:
        return ParseObject(None)
    else:
	    return ParseObject({item["id"]: item["count"] for item in pobj.obj})
	    
def do_parse_rarity(pobj: ParseObject):
    if isinstance(pobj.obj, str):
        new_value = pobj.obj.split('_')[1]
        print(f"{pobj.obj} -> {new_value}")
        pobj.obj = int(new_value)
        return pobj
    else:
        print("** not a string:", pobj)

def parse_dict(ops, pobj: ParseObject) -> ParseObject:
    ret = {}
    wildcard_op = ops.get("*", None)
    for k in pobj.obj.keys():
        op = ops.get(k, None)        
        result = None
        if op:
            result = parse_op(op, ParseObject(pobj.obj[k]))
        elif wildcard_op:
            # 如果定义了"*"的操作
            print("*", k)
            result = parse_op(wildcard_op, ParseObject(pobj.obj[k]))
        
        if result:
            if isinstance(result.obj, list) and len(result.obj)==1 and result.obj[0].unlist:
                print("unlist", k)
                result = result.obj[0]
            if result.flatten:
                print("flatten", k)
                ret.update(result.obj)
            elif result.ignore:
                pass
               # print("ignore", k)
            else:
                ret[k] = result.obj
        else:
            # 保留没有记录的Key
            ret[k] = pobj.obj[k]   
    
    # 处理 "_"
    self_op = ops.get("_", None)
    if self_op:
        return parse_op(self_op, ParseObject(ret))
    else:
        return ParseObject(ret)
        
#if __name__ == "__main__":
#    char = load_json("collect/char_003_kalts.json")
#    ops = load_json("transform.json")
#    result = parse_dict(ops, ParseObject(char))
#    with open(f"trans/char_003_kalts.json", "w", encoding="utf-8") as g:
#        json.dump(result, g, ensure_ascii=False, indent=2, sort_keys=True, cls=MyEncoder)
