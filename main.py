import heapq


# This line imports the heapq module, which provides an implementation of the heap queue algorithm. The algorithm is used to manage the priority queue for the A* algorithm.

class PuzzleNode:
    def __init__(self, state, parent=None, move=""):
        self.state = state
        self.parent = parent
        self.move = move
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0
        self.cost = self.calculate_cost()

    # This section defines the PuzzleNode class. Each instance of this class represents a state in the puzzle. The __init__ method initializes a node with a specific state, a parent node (default is None for the root), a move to reach this state from the parent, and calculates the depth and cost.

    def __lt__(self, other):
        return self.cost < other.cost

    # This method enables comparison between PuzzleNode instances based on their costs. It's used for sorting nodes in the priority queue.

    def calculate_cost(self):
        total_cost = self.depth
        for i in range(3):
            for j in range(3):
                value = self.state[i][j]
                if value != 0:
                    goal_row, goal_col = divmod(value - 1, 3)
                    total_cost += abs(i - goal_row) + abs(j - goal_col)
        return total_cost

    # This method calculates the total cost of a node using the A* heuristic. It adds the depth and the Manhattan Distance for each tile in the puzzle state.

    def get_neighbors(self):
        neighbors = []
        i, j = self.find_empty()
        possible_moves = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        for move in possible_moves:
            if 0 <= move[0] < 3 and 0 <= move[1] < 3:
                new_state = [row.copy() for row in self.state]
                new_state[i][j], new_state[move[0]][move[1]] = new_state[move[0]][move[1]], new_state[i][j]
                neighbors.append(PuzzleNode(new_state, self, move))
        return neighbors

    # This method generates neighboring states by moving the empty tile in all possible directions. It creates new PuzzleNode instances for each valid move.

    def find_empty(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return i, j

    # This method finds the position of the empty tile in the puzzle state.

    def is_goal(self, goal_state):
        return self.state == goal_state

    # This method checks whether the current puzzle state is the goal state.

    def get_solution_path(self):
        current = self
        path = []
        while current:
            path.append(current)
            current = current.parent
        return reversed(path)


# This method retrieves the solution path from the current node to the root by traversing the parent pointers.

def solve_8_puzzle(initial_state, goal_state):
    initial_node = PuzzleNode(initial_state)
    goal_node = PuzzleNode(goal_state)

    open_set = [initial_node]
    closed_set = set()

    while open_set:
        current_node = heapq.heappop(open_set)

        if current_node.is_goal(goal_state):
            return current_node.get_solution_path()

        closed_set.add(tuple(map(tuple, current_node.state)))

        for neighbor in current_node.get_neighbors():
            if tuple(map(tuple, neighbor.state)) not in closed_set:
                neighbor.cost = neighbor.calculate_cost()
                heapq.heappush(open_set, neighbor)

    return None

# This function implements the A* algorithm to solve the 8-puzzle problem. It starts with the initial state, iteratively expands nodes, and updates the priority queue
# based on their costs until the goal state is reached.

# Example usage:
initial_state = [
    [1, 2, 3],
    [4, 0, 5],
    [6, 7, 8]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

solution_path = solve_8_puzzle(initial_state, goal_state)

if solution_path:
    for step, node in enumerate(solution_path):
        print(f"Step {step} - Move: {node.move}")
        for row in node.state:
            print(row)
        print("\n")
else:
    print("No solution found.")
# This section demonstrates the usage of the implemented algorithm with an example initial state and goal state. It prints the solution path, including each step and
# the resulting state.
# Overall, the code follows a clear and modular structure, implementing the A* algorithm with the Manhattan Distance heuristic for solving the 8-puzzle problem.