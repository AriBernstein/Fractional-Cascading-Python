from Utils.GeneralUtils import StringContainer
from RangeTree.RangeTreeNode import RangeTreeNode

_POINTER_CHARS = _ONE_CHILD_POINTER = _TWO_CHILD_POINTER = ""
_PADDING_CHARS = _TWO_CHILDREN_INDENT = _WHITE_SPACE_INDENT = ""
_VERTICAL_SPACING = 2
_OUT_STR = ""


def _traverse(cur_str:StringContainer, padding:str, pointer:str,
              cur_root:RangeTreeNode, has_right_sibling:bool) -> None:
    
    # print(f"_traverse - cur_root: {cur_root}")
    
    if not cur_root:
        return
    
    # Append vertical line spacing:
    for _ in range(_VERTICAL_SPACING):
        cur_str += f"\n{padding}"
        cur_str += "|" if pointer == _WHITE_SPACE_INDENT else "| "
    
    # Append line rows with values:
    cur_str += f"\n{padding}{pointer} {cur_root.visualizer_str()}"
    
    # Calculate and append padding for next row:
    new_padding = StringContainer(padding)
    new_padding += _TWO_CHILDREN_INDENT \
        if has_right_sibling else _WHITE_SPACE_INDENT
    
    # Determine pointer for next row:
    pointer_left = _TWO_CHILD_POINTER if \
        cur_root.right_child() != None else _ONE_CHILD_POINTER
    
    # And recurse :)
    _traverse(cur_str, str(new_padding), pointer_left, cur_root.left_child(),
              cur_root.right_child() != None)
    _traverse(cur_str, str(new_padding), _ONE_CHILD_POINTER,
              cur_root.right_child(), False)
    
    
def _traverse_pre_order(root:RangeTreeNode) -> str:
    
    if not root:
        return "Empty Range Tree."
    
    visualize_str = StringContainer()
    visualize_str += root.visualizer_str()
    
    pointer_left = _TWO_CHILD_POINTER \
        if root.right_child() != None else _ONE_CHILD_POINTER
    
    _traverse(visualize_str, "", pointer_left, root.left_child(), root.right_child() != None)
    _traverse(visualize_str, "", _ONE_CHILD_POINTER, root.right_child(), False)
    
    return str(visualize_str)
    

def visualize(root:RangeTreeNode, vertical_spacing:int=2, 
              indent_per_level:int=7, safeChars:bool=False) -> str:
    
    global _POINTER_CHARS, _ONE_CHILD_POINTER, _TWO_CHILD_POINTER, \
        _PADDING_CHARS, _TWO_CHILDREN_INDENT, _WHITE_SPACE_INDENT, \
            _VERTICAL_SPACING, _OUT_STR
    
    _OUT_STR = ""   # Reset
            
    _VERTICAL_SPACING = vertical_spacing

    _POINTER_CHARS = ("-" if safeChars else '─') * indent_per_level
    _ONE_CHILD_POINTER = "└" + _POINTER_CHARS
    _TWO_CHILD_POINTER = "├" + _POINTER_CHARS
    
    _PADDING_CHARS = " " * (indent_per_level + 1)
    _TWO_CHILDREN_INDENT = "│" + _PADDING_CHARS
    _WHITE_SPACE_INDENT = ' ' + _PADDING_CHARS
    
    ret = _traverse_pre_order(root)
    
    return str(ret)
    
    
    