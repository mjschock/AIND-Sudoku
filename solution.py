assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

def get_boxes():
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

def eliminate(values):
    def get_peers_by_key(key):
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

    def remove_value_from_peers_by_key(value, key):
        peers = get_peers_by_key(key)

        for peer in peers:
            values[peer] = values[peer].replace(value, "")

    for key in values:
        value = values[key]

        if len(value) == 1:
            remove_value_from_peers_by_key(value, key)

    return values

def get_units():
    boxes = get_boxes()
    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
    unitlist = row_units + column_units + square_units
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    return units

def only_choice(values):
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

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
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
