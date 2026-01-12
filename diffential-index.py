import itertools
import math

def find_min_moves(*increments: int, divisions: int=360) -> list[tuple[int, ...] | tuple[None, ...]]:
    """Find the minimum number of moves of the input increments to reach each division
    
    Args:
        *increments (int): The tooth increments to check against as varargs
        divisions (int): The total number of divisions (degrees) that you need to visit
    
    Returns:
        (list[tuple[int, ...]]): A list of the best moves for the input increments with the index being 
        the division value.
    
    Note:
        Returned move tuple is in the same order as the input increments. Best usage is to zip 
        the input values with the output:
        ```python
        >>> gears = (40, 45)
        >>> move_counts = [dict(zip(gears, moves)) for moves in min_moves_iter(*gears)]
        ```
    
    Note:
        This function will only return moves that land on valid integer ratios. Any moves that
        end up at a fractional division will be skipped. If a division has no valid moves, it will 
        be set to `tuple[None,...]`. 
    
    Usage:
        ```python
        >>> min_moves_iter(40, 45, divisions=360)[40]
        (0, -5)
        >>> min_moves_iter(40, 45)[85]
        (5, 5)
        ```
    """
    # Get units per move
    dpms = tuple(divisions // inc for inc in increments)
    # Initialize an array with best move per division
    _default: tuple[None, ...] = tuple(None for _ in range(len(increments)))
    best_moves: list[tuple[int, ...] | tuple[None, ...]] = [_default for _ in range(divisions)]
    # Iterate all possible moves
    for moves in itertools.product(*((range(-inc, inc+1)) for inc in increments)):
        # Get the final position of the current moveset
        pos = math.sumprod(moves, dpms) % divisions
        # Skip non-integer positions
        if not pos.is_integer():
            continue
        # Convert to integer
        pos = int(pos)
        # Set best to current if no existing moves
        if best_moves[pos] == _default:
            best_moves[pos] = moves
        # Set best to current if current requires less moves
        elif sum(map(abs, moves)) < sum(map(abs, best_moves[pos])): # type: ignore (None is filtered by previous condition)
            best_moves[pos] = moves
    return best_moves

def find_best_ratio(min_:int=1, max_:int=90, average: bool=False) -> tuple[tuple[int, int], tuple[int, int]]:
    """Uses find_min_moves to find an increment ratio that has the least number of max
    moves
    """
    best_ratio = (None, None)
    best_moves = (None, None)
    for i in range(min_, max_):
        for j in range(min_, max_):
            moves = find_min_moves(i, j)
            if any(None in move for move in moves):
                continue
            print(i, j)
            average_moves = sum(sum(map(abs, move)) for move in moves) / len(moves)
            max_moves = max(sum(map(abs, move)) for move in moves)
            print('\tAverage: ', average_moves)
            print('\tMax: ', max_moves)
            if best_ratio == (None, None):
                best_ratio = (i, j)
                best_moves = (max_moves, average_moves)
            if average and average_moves < best_moves[1] or max_moves < best_moves[0]:
                best_moves = (max_moves, average_moves)
                best_ratio = (i, j)
    return best_ratio, best_moves

def main():
    #increments = (13, 7, 80)
    increments = (40, 45)
    results = find_min_moves(*increments)
    for degree, moves in enumerate(results):
        if None in moves:
            print(f'Degree: {degree}° is unreachable!')
            continue
        print(f"Degree: {degree}° requires {sum(map(abs, moves))} moves: {dict(zip(increments, moves))}") # type: ignore (None is filtered by previous condition)

if __name__ == "__main__":
    main()