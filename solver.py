import sys
import itertools

from puzzlestate import PuzzleState

def get_initial_rows(width):
    '''Gets the initial state of the puzzle from user input.'''

    # Continuously read puzzle in row by row
    rows = []

    for _ in range(width):
        values = input().split('\t')
        rows.append(values[:width])  # Ignore values that exceed width

    return rows

def get_goal_rows(width):
    '''Determines the goal rows given the rows and dimension of a puzzle state.'''

    # Create a sorted list of rows to represent the goal
    rows = []
    row = []

    for i in range(1, width ** 2):
        row.append(str(i))

        if len(row) == width:
            rows.append(row)
            row = []

    # Add the final blank/x
    row.append('x')
    rows.append(row)

    return rows

class Solver:

    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

class BFSSolver(Solver):

    def __init__(self, initial_state, goal_state):
        super().__init__(initial_state, goal_state)
        self.queue = [initial_state] # List to be used as a queue
        self.visited = [initial_state]
        self.pairs = [] # Pairs of states and their 'parent'

    def solve(self):
        '''Solves the puzzle using the breadth first search method.'''

        while self.queue != []:
            current_state = self.queue.pop(0)

            # Check if we found the goal
            if current_state == self.goal_state:
                break

            move_states = current_state.get_moves()

            # Loop through possible moves
            for state in move_states:
                if state not in self.visited:
                    self.queue.append(state) # Add to end of queue
                    self.visited.append(state) # Add to list of visited states

                    self.pairs.append((state, current_state))

    def get_solution(self):
        '''Gets the solution from the list of pairs created when solved. Only works if solution exists.'''
        path = [self.goal_state]
        current = self.goal_state

        while path[0] != self.initial_state:
            for pair in self.pairs:
                if pair[0] == current:
                    path.insert(0, pair[1])
                    current = pair[1]
                    break

        return path

class IDDFSSolver(Solver):

    def __init__(self, initial_state, goal_state):
        super().__init__(initial_state, goal_state)
        self.solution = []

    def solve(self):
        '''Solves the puzzle using an iterative deepening depth first search method.'''
        

        # Infinite loop from 0 onward
        for i in itertools.count(start=0):
            
            # Set reset values
            self.path = []
            self.max_depth = i

            # Call dfs on initial state
            self.dfs(self.initial_state, 0)

            if self.solution != []:
                break

    def dfs(self, state, current_depth):
        '''Does a standard depth first search.'''

        # Add current state to path
        self.path.append(state)

        # Check if state is goal state
        if state == self.goal_state:
            self.solution = self.path[:]

        # If the current depth is within the maximum, expand
        elif current_depth < self.max_depth:
            move_states = state.get_moves()

            for move in move_states:
                if move not in self.path:
                    self.dfs(move, current_depth + 1)

        self.path.pop()

    def get_solution(self):
        '''Returns the solution.'''
        return self.solution

class AStarSearch(Solver):

    def __init__(self, initial_state, goal_state):
        super().__init__(initial_state, goal_state)
        self.prio_queue = [] # List to be used as a priority queue
        self.visited = []
        self.pairs = []

    def solve(self):
        '''Solves the puzzle using the a* search method.'''

        # Set values for starting state
        self.initial_state.cost = 0
        self.initial_state.dist = self.est_moves(self.initial_state)

        # Add to queue and visited states
        self.prio_queue.append(self.initial_state)
        self.visited.append(self.initial_state)

        while self.prio_queue != []:
            current_state = self.remove_closest(self.prio_queue)

            # Stop searching if we found the goal
            if current_state == self.goal_state:
                break

            move_states = current_state.get_moves()

            # Find cost and distance of valid moves
            for state in move_states:
                if state not in self.visited: # Ignore visited states (explained in writeup)

                    # Cost is 1 higher than parent cost, set the remaining 'dist'
                    state.cost = current_state.cost + 1
                    state.dist = self.est_moves(state)

                    self.prio_queue.append(state)
                    self.visited.append(state) # Also explained in writeup
                    self.pairs.append((state, current_state)) # (child, parent)

    def remove_closest(self, queue):
        '''Removes the puzzle state with smallest cost + dist.'''
        closest = queue[0]

        for state in queue:
            if state.cost + state.dist < closest.cost + closest.dist:
                closest = state

        queue.remove(closest)
        return closest

    def est_moves(self, state):
        '''Returns the estimated number of moves to solve the puzzle.'''

        all_values = [value for row in state.current_rows for value in row]
        correct_values = [str(i) for i in range(1, state.width ** 2)] + ['x']
        
        counter = 0
        for i in range(len(all_values)):
            if all_values[i] != correct_values[i]:
                counter += 1

        return counter - 1

    def get_solution(self):
        '''Gets the solution from the list of pairs created when solved. Only works if solution exists.'''
        path = [self.goal_state]
        current = self.goal_state

        while path[0] != self.initial_state:
            for pair in self.pairs:
                if pair[0] == current:
                    path.insert(0, pair[1])
                    current = pair[1]
                    break

        return path

if __name__ == '__main__':

    # Read puzzle dimension
    width = int(input('Enter puzzle width: '))

    # Read puzzle rows and create puzzle states
    print('Enter puzzle values row by row (seperated with a tab): ')
    initial_rows = get_initial_rows(width)
    goal_rows = get_goal_rows(width)

    # Create initial and goal states
    initial_state = PuzzleState(width, initial_rows)
    goal_state = PuzzleState(width, goal_rows)

    # If entered puzzle is already solved
    if initial_state == goal_state:
        print('Solution:')
        initial_state.display()

    # Solve puzzle
    else:
        options = {
            'bfs': BFSSolver,
            'iddfs': IDDFSSolver,
            'a*': AStarSearch
        }

        # Initialize correct solver and solve puzzle
        solver = options[sys.argv[1]](initial_state, goal_state)

        print('Solving...')
        solver.solve()
        solution = solver.get_solution()

        print(f'Solution: {len(solution) - 1} move(s)')
        for state in solution:
            state.display()