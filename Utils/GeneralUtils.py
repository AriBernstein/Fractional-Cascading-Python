from typing import Iterable, Iterator, List

from Utils.CustomExceptions import InvalidInputException, InvalidTypeException

class StringContainer:
    
    """
    Class to contain a string to be passed as a reference and mutated over 
    method calls.   """
    
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
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, StringContainer) or isinstance(__o, str):
            return self._str == str(__o)
        return False
    
    def __iadd__(self, __o:object) -> None:
        if isinstance(__o, str) or isinstance(__o, chr):
            self._str += __o
        elif isinstance(__o, StringContainer):
            self._str += str(__o)
        else:
            raise InvalidTypeException(
                type(__o), "str or StringContainer", "StringContainer -> +=")
        return self
    

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
        

def matrix_col_subset(matrix:Iterator[Iterator[object]],
                      l_col_index:int, r_col_index:int) -> List[List[object]]:
    """
    Return a column-wise subset of the matrix containing columns between 
    l_col_index & r_col_index (inclusive). 
    
    Ex. given the following matrix, l_col_index = 0, r_col_index 2     
            [1,  2,  3,  4]      [1,  2,  3]
            [5,  6,  7,  8]  ->  [5,  6,  7]
            [9, 10, 11, 12]      [9, 10, 11]

    Args:
        matrix (Iterator[Iterator[object]]): 2D array of any indexable type.
        
        l_col_index (int): Inclusive leftmost column subset index.
        
        r_col_index (int): Inclusive rightmost column subset index. 

    Returns:
        List[List[object]]: [description]
    """
    if l_col_index < 0:
        raise InvalidInputException("l_col_index", str(l_col_index), "greater than 0")
    if r_col_index < 0:
        raise InvalidInputException("r_col_index", str(l_col_index), "greater than 0")
    if l_col_index > r_col_index:
        raise InvalidInputException(
            "l_col_index & r_col_index", f"l_col_index = {l_col_index}, " + \
                f"r_col_index = {r_col_index}", "l_col_index to be less " + \
                    "than or equal to r_col_index")

    return [sub_list[l_col_index:r_col_index + 1] for sub_list in matrix]


################### Utils for Pretty Printing Data Structures ##################
def pretty_list(l:Iterable, opening_brace:chr='[', closing_brace:chr=']',
                delim:str=",", left_indent_len=0, line_len_limit=None) -> str:
    
    ret = f"{' ' * left_indent_len}{opening_brace}" 
    line_len = initial_len = len(ret)
    for e in l:
        new_elem_str = f"{e}{delim} "
        
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

    Raises Exception: If i has more digits than n.

    Returns str: String containing integer i, front-padded to n characters. """
    
    i_str = str(i)
    i_len = len(i_str)
    
    if i_len > n:
        raise Exception(
            "Int i has {i_len} digits but the maximum allowed is {n}.")
    
    return f"{' ' * (n - i_len)}{i_str}"