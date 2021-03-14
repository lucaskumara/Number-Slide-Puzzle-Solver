class PuzzleState:

    def __init__(self, width, current_rows):
        self.width = width
        self.current_rows = current_rows
        self.blank_position = self.find_blank()

    def __eq__(self, other):
        return self.current_rows == other.current_rows

    def find_blank(self):
        '''Finds the row index and column index of the blank/x.'''
        for i in range(len(self.current_rows)):
            if 'x' in self.current_rows[i]:
                return (i, self.current_rows[i].index('x'))

    def get_moves(self):
        '''Returns a list of all possible moves from the current state.'''

        possible_moves = []
        row_index, column_index = self.blank_position

        # If a piece can move UP
        if row_index + 1 != self.width:

            # Modify rows
            up_rows = [row.copy() for row in self.current_rows]
            up_rows[row_index][column_index], up_rows[row_index + 1][column_index] = up_rows[row_index + 1][column_index], up_rows[row_index][column_index]

            # Create and add state to move list
            up_state = PuzzleState(self.width, up_rows)
            possible_moves.append(up_state)

        # If a piece can move DOWN
        if row_index != 0:

            # Modify rows
            down_rows = [row.copy() for row in self.current_rows]
            down_rows[row_index][column_index], down_rows[row_index - 1][column_index] = down_rows[row_index - 1][column_index], down_rows[row_index][column_index]

            # Create and add state to move list
            down_state = PuzzleState(self.width, down_rows)
            possible_moves.append(down_state)

        # If a piece can move LEFT
        if column_index + 1 != self.width:

            # Modify rows
            left_rows = [row.copy() for row in self.current_rows]
            left_rows[row_index][column_index], left_rows[row_index][column_index + 1] = left_rows[row_index][column_index + 1], left_rows[row_index][column_index]

            # Create and add state to move list
            left_state = PuzzleState(self.width, left_rows)
            possible_moves.append(left_state)

        # If a piece can move RIGHT
        if column_index != 0:

            # Modify rows
            right_rows = [row.copy() for row in self.current_rows]
            right_rows[row_index][column_index], right_rows[row_index][column_index - 1] = right_rows[row_index][column_index - 1], right_rows[row_index][column_index]

            # Create and add state to move list
            right_state = PuzzleState(self.width, right_rows)
            possible_moves.append(right_state)

        return possible_moves

    def display(self):
        '''Displays the state.'''
        for row in self.current_rows:
            print('\t'.join(row))
        print() # Separate the states