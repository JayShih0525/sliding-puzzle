import random
import heapq
from js import document, window
from pyodide.ffi import create_proxy
import time
import threading

# Constants
GRID_SIZE = 3
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

class SlidingPuzzle:
    def __init__(self):
        self.tiles = GOAL_STATE.copy()
        self.empty_index = self.tiles.index(0)
        self.grid_size = GRID_SIZE
        self.count = 0
        self.best = 0
        self.record = self.tiles.copy()

    @staticmethod
    def is_solvable(state):
        inversions = sum(
            1 for i in range(len(state)) for j in range(i + 1, len(state))
            if state[i] > state[j] != 0
        )
        return inversions % 2 == 0


    @staticmethod
    def heuristic(state):
        """Manhattan distance heuristic."""
        distance = 0
        for i, value in enumerate(state):
            if value == 0:
                continue
            goal_row, goal_col = divmod(value - 1, GRID_SIZE)
            current_row, current_col = divmod(i, GRID_SIZE)
            distance += abs(goal_row - current_row) + abs(goal_col - current_col)
        return distance

    def solve(self):
        """Solve the puzzle using the A* algorithm."""
        if not self.is_solvable(self.tiles):
            return "unsolvable"

        pq = []
        heapq.heappush(pq, (0, self.tiles[:], []))
        visited = set()

        while pq:
            cost, current_state, path = heapq.heappop(pq)

            if current_state == GOAL_STATE:
                return path

            visited.add(tuple(current_state))

            zero_index = current_state.index(0)
            for neighbor in self.get_neighbors(zero_index):
                new_state = current_state[:]
                new_state[zero_index], new_state[neighbor] = new_state[neighbor], new_state[zero_index]

                if tuple(new_state) not in visited:
                    new_cost = len(path) + 1 + self.heuristic(new_state)
                    heapq.heappush(pq, (new_cost, new_state, path + [new_state]))

        return []

    def shuffle(self):
        self.count = 0
        while True:
            random.shuffle(self.tiles)
            if SlidingPuzzle.is_solvable(self.tiles):
                break
        self.empty_index = self.tiles.index(0)
        self.best = len(self.solve()) 
        self.record = self.tiles.copy()


    def again(self):
        self.count = 0
        self.tiles = self.record.copy()
        self.empty_index = self.tiles.index(0)
        self.best = len(self.solve())
        self.record = self.tiles.copy()

    def move_tile(self, index):
        if index in self.get_neighbors(self.empty_index):
            self.tiles[self.empty_index], self.tiles[index] = self.tiles[index], self.tiles[self.empty_index]
            self.empty_index = index
            self.count += 1

    def get_neighbors(self, index):
        neighbors = []
        row, col = divmod(index, self.grid_size)
        if row > 0: neighbors.append(index - self.grid_size)
        if row < self.grid_size - 1: neighbors.append(index + self.grid_size)
        if col > 0: neighbors.append(index - 1)
        if col < self.grid_size - 1: neighbors.append(index + 1)
        return neighbors

    def is_solved(self):
        return self.tiles == GOAL_STATE

puzzle = SlidingPuzzle()


def render_puzzle():
    grid = document.getElementById("puzzle-grid")
    grid.innerHTML = ""
    for i, value in enumerate(puzzle.tiles):
        tile = document.createElement("div")
        tile.classList.add("tile")
        if value == 0:
            tile.classList.add("empty")
        else:
            tile.innerText = str(value)
            tile.onclick = lambda e, idx=i: handle_tile_click(idx)
        grid.appendChild(tile)

    move_count = document.getElementById("move-count")
    move_count.innerText = f"Moves: {puzzle.count}" 


def handle_tile_click(index):
    puzzle.move_tile(index)
    render_puzzle()
    check_puzzle_solved()


def handle_shuffle(event=None):
    puzzle.shuffle()
    render_puzzle()


def handle_again(event=None):
    puzzle.again()
    render_puzzle()


def handle_solve(event=None):
    if(not puzzle.is_solved()):
        solution_path = puzzle.solve()
        next_state = solution_path[0]
        puzzle.tiles = next_state.copy()
        puzzle.empty_index = next_state.index(0)
        puzzle.count += 1
        render_puzzle()
    check_puzzle_solved()


def attach_listeners():
    shuffle_btn = document.getElementById("shuffle-btn")
    shuffle_btn.addEventListener("click", create_proxy(handle_shuffle))

    again_btn = document.getElementById("again-btn")
    again_btn.addEventListener("click", create_proxy(handle_again))

    solve_btn = document.getElementById("solve-btn")
    solve_btn.addEventListener("click", create_proxy(handle_solve))


def check_puzzle_solved(event=None):
    if puzzle.is_solved():
        render_puzzle()

        def show_prompt():
            name = window.prompt("Congratulations! Enter your name:", "")
            if not name or not name.strip():
                name = 'Unknown'

            name = name[:15]
            move = puzzle.count
            best = puzzle.best
            window.writeData("data", name, move, best)
            window.readAndDisplayData("data")

        window.setTimeout(create_proxy(show_prompt), 10)




attach_listeners()
handle_shuffle()
render_puzzle()