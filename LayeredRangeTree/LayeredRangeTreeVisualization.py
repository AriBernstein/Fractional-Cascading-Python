from typing import Union
from Utils.GeneralUtils import StringContainer
from LayeredRangeTree.LayeredRangeTree import LayeredRangeTree
from LayeredRangeTree.LayeredRangeTreeNode import RangeTreeNode, \
    LayeredRangeTreeNode, LayeredRangeTreeSubNode

"""
Methods which create a text visualization of the Range Tree. Outside-facing 
method is visualize_range_tree.
"""

# Globals
_HORIZONTAL_LINE_CHARS = _LAST_CHILD_POINTER = _NOT_LAST_CHILD_POINTER = \
    _PADDING_CHARS = _TWO_CHILDREN_INDENT = _WHITE_SPACE_INDENT = _OUT_STR = ""
_VERTICAL_SPACING = 2
_SAFE_CHARS = False

def _v_line_char() -> chr:
    """
    Returns: character representing a single horizontal cross-section of a
    vertical line. """
    
    return '|' if _SAFE_CHARS else '│'

def _determine_left_child_pointer(n:RangeTreeNode) -> str:
    return _LAST_CHILD_POINTER \
        if n.right_child() == None else _NOT_LAST_CHILD_POINTER


def _traverse(cur_str:StringContainer, padding:str, pointer:str,
              cur_root:RangeTreeNode, has_right_sibling:bool) -> None:
    """
    Recursively traverse range tree to populate StringContainer object.

    Args:
        cur_str (StringContainer): Visualization thus far.
        
        padding (str): Left indent.
        
        pointer (str): Left side for this recursive call.
        
        cur_root (RangeTreeNode): The current RangeTreeNode.
        
        has_right_sibling (bool): 
            If true, then begin horizontal line as a perpendicular line coming 
            out of a vertical line. Otherwise being horizontal line as a right 
            angle.  """
    
    if not cur_root:
        return
    
    # Append vertical line spacing:
    for _ in range(_VERTICAL_SPACING):
        cur_str += f"\n{padding}{_v_line_char()}"
        cur_str += " " if pointer != _WHITE_SPACE_INDENT else ""
    
    # Append line rows with values:
    cur_str += f"\n{padding}{pointer} {cur_root.visualizer_str()}"

    # Calculate and append padding for next row:
    new_padding = StringContainer(padding)
    new_padding += _TWO_CHILDREN_INDENT \
        if has_right_sibling else _WHITE_SPACE_INDENT
    
    # Determine pointer for next row:
    pointer_left = _determine_left_child_pointer(cur_root)
    
    # And recurse :)
    _traverse(cur_str, str(new_padding), pointer_left, 
              cur_root.left_child(), cur_root.right_child() != None)
    _traverse(cur_str, str(new_padding), _LAST_CHILD_POINTER,
              cur_root.right_child(), False)
    
    
def _traverse_pre_order(cur_root:RangeTreeNode) -> str:
    """
    Helper function to call recursive search methods initially.

    Args cur_root (RangeTreeNode): The root of the RangeTree.

    Returns: str: String visualization of the Range Tree.    """
        
    if not cur_root:
        return "Empty Range Tree."
    
    visualize_str = StringContainer()
    visualize_str += cur_root.visualizer_str()
    
    pointer_left = _determine_left_child_pointer(cur_root)
 
    _traverse(visualize_str, "", pointer_left,
              cur_root.left_child(), cur_root.right_child() != None)
    
    _traverse(visualize_str, "", _LAST_CHILD_POINTER,
              cur_root.right_child(), False)
    
    return str(visualize_str)
    

def visualize_layered_range_tree(
    root:Union[RangeTreeNode, LayeredRangeTree], vertical_spacing:int=2, 
    indent_per_level:int=7, safe_chars:bool=False, print_tree=False) -> str:
    """
    Initialize globals and traverse range tree to generate visualization string.

    Args:
        root (Union[RangeTreeNode, RangeTree]): 
            The root of the Range Tree or the Range Tree itself.
        
        vertical_spacing (int, optional): 
            Number of vertical spaces between each horizontal line (defaults 2).
        
        indent_per_level (int, optional): 
            Length of horizontal lines outside of information.
            
        safe_chars (bool, optional): 
            If true, use chars that are easier for consoles to display. 
            Otherwise (default), use characters that benefit the visualization 
            but may be more prone to console printing bugs.
            
        print_tree (bool, optional): 
            If true, print tree to console. (Defaults to False.)

    Returns: str: String visualization of the Range Tree.    """
    
    # Reset/reassign global graphic variables for visualization
    global _HORIZONTAL_LINE_CHARS, _NOT_LAST_CHILD_POINTER, \
        _LAST_CHILD_POINTER, _PADDING_CHARS, _TWO_CHILDREN_INDENT, \
            _WHITE_SPACE_INDENT, _VERTICAL_SPACING, _OUT_STR, _SAFE_CHARS
    
    _OUT_STR = ""
    _SAFE_CHARS = safe_chars
    
    # -> Horizontal lines including transitions from vertical lines.
    _HORIZONTAL_LINE_CHARS = ("-" if safe_chars else '─') * indent_per_level
    _NOT_LAST_CHILD_POINTER = "├" + _HORIZONTAL_LINE_CHARS
    _LAST_CHILD_POINTER = "└" + _HORIZONTAL_LINE_CHARS
    
    # -> Spacing for strings that only represent vertical lines.
    _VERTICAL_SPACING = vertical_spacing
    _PADDING_CHARS = " " * (indent_per_level + 1)
    _TWO_CHILDREN_INDENT = _v_line_char() + _PADDING_CHARS
    _WHITE_SPACE_INDENT = ' ' + _PADDING_CHARS
    
    root = root.root() if isinstance(root, LayeredRangeTree) else root
    ret_str = _traverse_pre_order(root)
    
    if print_tree:
        print(ret_str)
    
    return ret_str