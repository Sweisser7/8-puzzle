import heapq

from memory_profiler import profile


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

    def __lt__(self, other):
        return self.cost < other.cost

    def calculate_cost(self):
        total_cost = self.depth + self.manhattan_distance()
        return total_cost

    def manhattan_distance(self):
        distance = 0
        for i in range(3):
            for j in range(3):
                value = self.state[i][j]
                if value != 0:
                    goal_row, goal_col = divmod(value - 1, 3)
                    distance += abs(i - goal_row) + abs(j - goal_col)
        return distance

    def get_neighbors(self):
        neighbors = []
        i, j = self.find_empty()
        possible_moves = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
        for move in possible_moves:
            if 0 <= move[0] < 3 and 0 <= move[1] < 3:
                new_state = [row.copy() for row in self.state]
                new_state[i][j], new_state[move[0]][move[1]] = new_state[move[0]][move[1]], new_state[i][j]
                neighbors.append(PuzzleNode(new_state, self, move))
        return neighbors

    def find_empty(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return i, j

    def is_goal(self, goal_state):
        return self.state == goal_state

    def get_solution_path(self):
        current = self
        path = []
        while current:
            path.append(current)
            current = current.parent
        return reversed(path)

@profile
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
