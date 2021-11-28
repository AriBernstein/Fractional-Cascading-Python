from typing import Iterable, Iterator, List

class StringContainer:
    
    def __init__(self, initial_str:str="") -> None:
        self._str = initial_str
        self._i = 0
    
    def append(self, new_str:str):
        self._str += new_str
    
    def __iter__(self) -> Iterator:
        return self
    
    def __next__(self) -> chr:
        if self._i < len(self._str):
            self._i += 1
            return self._str[self._i - 1]
        raise StopIteration
    
    def __str__(self) -> str:
        return self._str
    
    def __repr__(self) -> str:
        return str(self)
    

class ColIterator:
    """
    Given a matrix containing x lists of y items, iterate through items in the 
    y dimension. """
    
    def __init__(self, data_set:Iterable[Iterable[object]], 
                 sub_list_index:int) -> None:
        self._matrix = data_set
        self._i = 0
        self._j = sub_list_index
    
    def __iter__(self) -> Iterator:
        return self
    
    def __next__(self) -> object:
        if self._i < len(self._matrix):
            self._i += 1
            return self._matrix[self._i - 1][self._j]
        raise StopIteration
        

def matrix_subset(matrix:Iterator[Iterator[object]], 
                  l_index:int, r_index:int) -> List[List[object]]:
    return [sub_list[l_index:r_index + 1] for sub_list in matrix]


################### Utils for Pretty Printing Data Structures ##################
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
    for k in key_list: 
        ret += f"{' ' * left_indent_len}{k} -> {d[k]}\n"
    return ret.rstrip()

def pad_ints(i:int, n:int) -> str:
    """
    Convert integer i into string of length equal to n.

    Args:
        i (int): integer in to be converted into a string.
        n (int): length of string output.

    Raises:
        Exception: If i has more digits than n.

    Returns:
        str: String containing integer i, front-padded to n characters. """
    
    i_str = str(i)
    i_len = len(i_str)
    
    if i_len > n:
        raise Exception(
            "Int i has {i_len} digits but the maximum allowed is {n}.")
    
    return f"{' ' * (n - i_len)}{i_str}"