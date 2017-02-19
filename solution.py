assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'
unitAscending = ['I1', 'H2', 'G3', 'F4', 'E5', 'D6', 'C7', 'B8', 'A9']
unitDescending = ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def remove_pair_from_peers_in_unit(values, unit, pair):
    "Removes a pair of values from all peers in a unit."
    for box in unit:
        vals = values[box]
        if vals != pair:
            values[box] = vals.replace(pair[0], "").replace(pair[1], "")

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    units = get_units()
    for key in values:
        units_by_key = units[key]
        for unit in units_by_key:
            boxes_with_2_vals = []
            for box in unit:
                vals = values[box]
                if len(vals) == 2:
                    boxes_with_2_vals.append(box)
            if len(boxes_with_2_vals) > 1:
                for outer_box in boxes_with_2_vals:
                    for inner_box in boxes_with_2_vals:
                        if inner_box != outer_box and values[inner_box] == values[outer_box]:
                            pair = values[inner_box]
                            remove_pair_from_peers_in_unit(values, unit, pair)
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

def get_boxes():
    "Returns the cross product of the rows and columns."
    return cross(rows, cols)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'.
            If the box has no value, then the value will be '123456789'.
    """
    boxes = get_boxes()
    return dict(zip(boxes, ['123456789' if x == '.' else x for x in grid]))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    boxes = get_boxes()
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for row in rows:
        print(''.join(values[row+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if row in 'CF': print(line)
    print

def remove_value_from_peers_by_key(values, peers, box):
    "Removes a value from all peers of a box by it's key."
    value = values[box]

    for peer in peers:
        values[peer] = values[peer].replace(value, "")

def eliminate(values):
    "Eliminates from row, col, and 3x3 grid peers any value that is already determined."
    def get_peers_by_key(key):
        "Returns a set of all row, col, and 3x3 grid peers for a box."
        row = key[0]
        col = key[1]
        row_peers = cross(row, '123456789')
        col_peers = cross('ABCDEFGHI', col)

        if 'ABC'.find(row) != -1:
            row_range = 'ABC'
        elif 'DEF'.find(row) != -1:
            row_range = 'DEF'
        else:
            row_range = 'GHI'
        if '123'.find(col) != -1:
            col_range = '123'
        elif '456'.find(col) != -1:
            col_range = '456'
        else:
            col_range = '789'

        square_peers = cross(row_range, col_range)
        peers = list(set(row_peers + col_peers + square_peers) - set([key]))
        return peers

    for key in values:
        value = values[key]

        if len(value) == 1:
            remove_value_from_peers_by_key(values, get_peers_by_key(key), key)

    return values

def eliminate_diagonal(values):
    "Eliminates from the diagonal peers any value that is already determined."
    for unit in unitAscending:
        val = values[unit]
        if len(val) == 1:
            remove_value_from_peers_by_key(values, list(set(unitAscending) - set([unit])), unit)

    for unit in unitDescending:
        val = values[unit]
        if len(val) == 1:
            remove_value_from_peers_by_key(values, list(set(unitDescending) - set([unit])), unit)

    return values

def get_units():
    "Returns a dictionary that maps each box to it's row, column, and 3x3 grid units."
    boxes = get_boxes()
    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
    unitlist = row_units + column_units + square_units
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    return units

def only_choice(values):
    "Selects the only choice for a box if it's row, column, and 3x3 grid peers don't contain that value."
    units = get_units()
    for key in units:
        vals = values[key]
        for unit in units[key]:
            vals_in_use = [list(values[x]) for x in unit if x != key]
            vals_in_use_set = set([])

            for val_in_use_set in vals_in_use:
                vals_in_use_set = vals_in_use_set | set(val_in_use_set)

            for val in vals:
                if val not in vals_in_use_set:
                    values[key] = val

    return values

def get_set_of_peer_vals(values, peers, box):
    "Returns a set of all the peer values"
    set_of_peer_vals = set([])
    for peer in peers:
        if peer != box:
            set_of_peer_vals = set_of_peer_vals | set(list(values[peer]))
    return set_of_peer_vals

def only_choice_diagonal(values):
    "Selects the only choice for a box if none of diagonal peers contain that value."
    for box in unitAscending:
        set_of_peer_vals = get_set_of_peer_vals(values, unitAscending, box)
        vals = values[box]
        for val in vals:
            if val not in set_of_peer_vals:
                values[box] = val

    for box in unitDescending:
        set_of_peer_vals = get_set_of_peer_vals(values, unitDescending, box)
        vals = values[box]
        for val in vals:
            if val not in set_of_peer_vals:
                values[box] = val

    return values

def reduce_puzzle(values):
    "Runs through the contraints repeatedly until the values don't change or a box is empty"
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        values = eliminate_diagonal(values)
        values = only_choice(values)
        values = only_choice_diagonal(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Recursively searches for a solution, iterating upon a tree of options using depth first search"
    values = reduce_puzzle(values)
    if values is False:
        return False # something's wrong

    solved_values = len([box for box in values.keys() if len(values[box]) == 1])
    if solved_values == len(values):
        return values # solved
    # stalled

    # Choose one of the unfilled squares with the fewest possibilities
    min_possibility_count = None
    min_possibility_count_box = None

    for box in values.keys():
        possibility_count = len(values[box])

        if possibility_count != 1:
            if min_possibility_count is None or possibility_count < min_possibility_count:
                min_possibility_count = possibility_count
                min_possibility_count_box = box

    vals_to_try = values[min_possibility_count_box]
    for val in vals_to_try:
        values_copy = values.copy()
        values_copy[min_possibility_count_box] = val
        values_copy = search(values_copy)
        if values_copy != False:
            return values_copy

    return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
