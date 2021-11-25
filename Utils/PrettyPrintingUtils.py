
from typing import Iterable


def pretty_list(l:Iterable, opening_brace:chr='[', closing_brace:chr=']',
                left_indent_len=0, line_len_limit=None) -> str:
    
    ret = f"{' ' * left_indent_len}{opening_brace}" 
    line_len = initial_len = len(ret)
    for e in l:
        new_elem_str = f"{e}, "
        
        if line_len_limit:
            line_len += len(new_elem_str)
            if line_len > line_len_limit:
                ret += f"\n{' ' * left_indent_len}{opening_brace}"
                line_len = initial_len
                
        ret += new_elem_str
        
    return f"{ret[:-2]}{closing_brace}" if len(l) > 0 else ret + closing_brace

def pretty_dict(d:dict, key_list:list=None, left_indent_len:int=4) -> str:
    ret = ""
    if not key_list: key_list = d.keys
    for k in key_list: ret += f"{' ' * left_indent_len}{k} -> {d[k]}\n"
    return ret.rstrip()