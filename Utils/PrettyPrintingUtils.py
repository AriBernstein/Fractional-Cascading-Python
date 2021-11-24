
from typing import Iterable

def pretty_list(l:Iterable, opening_brace:chr='[', closing_brace:chr=']',
                left_indent_len=0) -> str:
    
    ret = f"{' ' * left_indent_len}{opening_brace}" 
    for e in l: ret += f"{e}, "
    return f"{ret[:-2]}{closing_brace}" if len(l) > 0 else ret + closing_brace