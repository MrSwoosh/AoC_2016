"""
Possible solution for Advent of Code 2016.
https://adventofcode.com/2016/day/11
Date: 04-02-2026
Complexity:
    Possible new states = O(n^2) (1 move = O(n^1), 2 moves = O(n^2))
    Sorting = O(n log n)
    Validation = O(n^2) (nested loop = O(n^2), sorting = O(n log n), validation + sorting = O(n^2))
    Generating new states = O(n^4) (for every combination a validation = O(n^2 * n^2) = O(n^4))
    Total BFS = O(S * n^4) where S = possible states
    Exponential complexity, nearly impossible without pruning and symmetry reduction


The algorithm is divided into 3 classes:
    DataHandler
        Handles all data related tasks:
            Extract data from source file
            Transform data to usable format
    StateHandler
        Handles all state related tasks:
            Create initial state
            Create extended state
            Create new possible states
            Validate possible states
    Solver
        Searches for the least amount of steps to reach a goal state

Suggestions for improvements:
    -Initial state is not sorted.
    -Exception handling
        Currents version has no exception handling, because the algorithm is
        intended for 1 time use by 1 user.
        Exception handling should at least be used when accessing the
        file with input data.
    -Complexity
        -Current validation uses nested loop -> O(n^2),
        but could be reduced to O(n) by using a dict for each floor,
        then assigning all generators and chips on that floor,
        then checking if values are allowed.
        Example code:
            floors = {
                1: {"gens": set(), "chips": set()},
                2: {"gens": set(), "chips": set()},
                ...
            }
            for floor in floors:
                if floor["gens"]:
                    for chip in floor["chips"]:
                        if chip not in floor["gens"]:
                            return False
        -Memoization might improve complexity. (not tested, just a thought)
        When elevator is at floor 4 and the first element is at (4, 4),
        focussing on the next element closest to the top level and storing its
        total steps in a dict, will cut out all future searches for that position.
        Example:
          If state = (4, (4, 4), (3, 3)) the shortest path to (4, (4, 4), (4, 4)) is 4 steps.
          When steps are already calculated, retrieving the value from dict['element'] is O(1).
          Total steps is then the number of steps to get state[0:2] to (4, (4, 4)) + dict['element']
          Will only work if there are no generators of chips from other elements on the same floor or higher
          than the element to be calculated.
    -Readability
        Use alias for type annotations
"""


from collections import deque

test = False


class DataHandler:
    """
    Responsible for extracting and transforming raw puzzle input
    into a structured representation usable by the solver.

    This class performs a lightweight ETL pipeline:
        - Extract: Read textual puzzle input from file
        - Transform: Normalize textual descriptions
        - Load: Convert into structured floor-position mapping

    Output format:
        dict[str, list[int]]
        {
            "<element_name>": [generator_floor, microchip_floor]
        }

    Design assumptions:
        - Input format strictly follows AoC 2016 Day 11 specification
        - Floors are numbered 1..4
        - Each element appears exactly once as generator and microchip
        - No runtime validation of malformed input is performed

    This class is intentionally isolated to decouple parsing logic
    from state-space search logic.
    """
    def __init__(self, test_scenario: bool) -> None:
        """
        Initializes the data source location.

        Parameters
        ----------
        test_scenario: bool
            If True, loads test_input.
            If False, loads input.

        Notes
        -----
        No validation is performed to ensure file existence.
        In production-grade code, file access should be wrapped
        in proper exception handling.
        """
        self.file_location = "test_input" if test_scenario else "dataset_day_11"

    def etl(self) -> dict[str, list[int]]:
        """
        Executes the full ETL pipeline.

        Steps
        -----
        1. Reads file line by line.
        2. Normalizes textual floor descriptions.
        3. Extracts device descriptions.
        4. Maps generators and chips to floor numbers.

        Returns
        -------
        dict[str, list[int]]
            Mapping from element name to:
                [generator_floor, microchip_floor]

        Complexity
        ----------
        O(n) where n = number of textual tokens in input.
        Input size is very small, so negligible.

        Assumptions
        -----------
        - Floor 4 contains no relevant data and is skipped.
        - Input grammar remains consistent.
        """
        with open(self.file_location, 'r') as file:
            raw_floor_settings: list[tuple[int, list[str]]] = []  # Syntax example: [(1, ['hydrogen microchip', 'lithium microchip'])]
            for floor_index, values in enumerate(file):

                # 4th row has no valuable data, therefore can be skipped
                if floor_index + 1 == 4:
                    continue

                cleaned_row = self._adjust_row(values)  # Syntax example: "first, hydrogen microchip, lithium microchip"

                items = cleaned_row.split(", ")[1:]  # Syntax example: ['hydrogen microchip', 'lithium microchip']

                raw_floor_settings.append((floor_index + 1, items))

            floor_positions = self._match_generator_and_chip_on_element(raw_floor_settings)  # Syntax example: {'hydrogen': [2, 1], 'lithium': [3, 1]}

            return floor_positions

    def _adjust_row(self, row_old: str) -> str:
        """
        Normalizes a single input line.

        Performs deterministic string substitutions to remove
        grammatical structure and retain only:
            "<floor_name>, <device>, <device>, ..."

        Parameters
        ----------
        row_old : str
            Raw input line from file.

        Returns
        -------
        str
            Cleaned comma-separated representation.

        Notes
        -----
        This method relies on fixed textual patterns.
        If input grammar changes, transformation may break.
        A regex-based parser would be more robust.
        """
        row_old = row_old.strip()  # Syntax example: The second floor contains a hydrogen generator.

        # Remove unwanted characters
        row_being_processed = (row_old.replace("The ", '')
                               .replace(" floor contains a", ',')
                               .replace(", and a", ',')
                               .replace(" and", ',')
                               .replace("a ", "")
                               .replace('.', '')
                               .replace("floor ", '')
                               .replace("-compatible", ''))

        # Renaming for readability
        new_row = row_being_processed  # Syntax example: second, hydrogen generator

        return new_row

    def _match_generator_and_chip_on_element(self, raw_floor_settings: list[tuple[int, list[str]]]) -> dict[str, list[int]]:
        """
        Converts floor-wise device listing into element-wise mapping.

        Input example:
            [(1, ['hydrogen microchip']),
             (2, ['hydrogen generator'])]

        Output:
            {'hydrogen': [2, 1]}

        Returns
        -------
        dict[str, list[int]]
            element -> [generator_floor, microchip_floor]

        Complexity
        ----------
        O(n) where n = number of devices.

        Design choice
        -------------
        Using list[int] instead of tuple[int, int]
        to allow direct indexed mutation during construction.
        """
        floor_positions: dict[str, list[int]] = {}  # Syntax example -> plutonium: [generator, microchip] -> {'plutonium': [1, 3]}


        for floor in raw_floor_settings:  # Syntax example: [1, ['hydrogen microchip', 'lithium microchip']]
            floor_number = floor[0]
            devices = floor[1]

            for device in devices:
                element, part = device.split(" ")

                if element not in floor_positions:
                    floor_positions[element] = [0, 0]
                if "generator" in part:
                    floor_positions[element][0] = floor_number
                if "micro" in part:
                    floor_positions[element][1] = floor_number

        return floor_positions


class StateHandler:
    """
    Encapsulates all state-space logic.

    Responsibilities:
        - State construction
        - Goal state creation
        - State expansion
        - State validation
        - Canonical sorting for symmetry reduction

    State representation:
        list[int | tuple[int, int]]

        Index 0:
            Elevator floor position

        Index i (i >= 1):
            (generator_floor, microchip_floor)

    Example:
        [1, (2, 1), (3, 1)]

    Design rationale
    ----------------
    - List chosen for mutability during expansion
    - Tuple for element pairs to preserve atomicity
    - Sorting used to eliminate symmetric states (pruning)
    """

    def __init__(self) -> None:
        pass

    def create_initial_state(self, floor_settings: dict[str, list[int]]) -> list[int | tuple[int, int]]:
        """
        Constructs initial solver state.

        Elevator always starts at floor 1.

        Parameters
        ----------
        floor_settings : dict[str, list[int]]

        Returns
        -------
        list[int | tuple[int, int]]

        Complexity
        ----------
        O(n) where n = number of elements.

        Note
        ----
        State is NOT sorted here.
        Sorting occurs during validation to canonicalize state.
        """
        # Initiate state with lift on floor 1
        initial_state = [1]  ## Syntax example: [1, (2, 1), (3, 1)]

        for element in floor_settings:
            initial_state.append((floor_settings[element][0], floor_settings[element][1]))

        return initial_state


    def add_extra_pairs(self, initial_state: list[int | tuple[int, int]]) -> list[int | tuple[int, int]]:
        """
        Extends state with two additional element pairs
        for Part 2 of the puzzle.

        Adds:
            (1, 1), (1, 1)

        Returns
        -------
        Extended state (new list)

        Design note
        -----------
        Returns a new list to preserve immutability
        of the original state.
        """
        return initial_state + [(1, 1), (1, 1)]  # Syntax example: [1, (2, 1), (3, 1), (1, 1), (1, 1)]


    def create_goal_state(self, initial_state: list[int | tuple[int, int]]) -> list[int | tuple[int, int]]:
        """
        Generates goal state.

        Goal condition:
            - Elevator at floor 4
            - All generators and chips at floor 4

        Returns
        -------
        Goal state with identical structure as initial state.
        """
        return [4 if isinstance(x, int) else (4, 4) for x in initial_state]  # Syntax example: [4, (4, 4), (4, 4)]


    def create_new_states(self, current_state: list[int | tuple[int, int]],
                          seen: set[tuple[int | tuple[int, int], ...]]) \
                        -> tuple[
                        list[list[int | tuple[int, int]]],
                        set[tuple[int | tuple[int, int], ...]]]:
        """
        Generates all valid successor states from current state.

        Strategy
        --------
        1. Identify movable items on current elevator floor.
        2. Generate all 1-item and 2-item move combinations.
        3. Apply vertical movement (+1 or -1).
        4. Apply pruning rules.
        5. Validate resulting state.
        6. Deduplicate using `seen`.

        Returns
        -------
        list of validated states,
        updated seen set

        Complexity
        ----------
        Worst case:
            O(n^4)

        Reason:
            - O(n^2) move combinations
            - Each validation O(n^2)

        Pruning rules implemented:
            - No movement below floor 1 or above floor 4
            - Avoid useless downward/upward moves
            - Avoid revisiting canonical states

        This is the core branching logic of the BFS.

        Suggestion for improvement:
            - Transfer parts of logic to helper methods.
        """

        new_states = list()
        lift = current_state[0]

        """
        Limit possible new states to positions equal to lift position (pruning).
        Takes a current state, example: [1, (2, 1), (3, 1)]
        Checks for every tuple (column) if a position equals lift position.
        If true, saves index of tuple and found equal position in new tuple.
        Syntax example: [(1, 1), (2, 1)] 
            where: 
                [_][0] = index in current_state
                [_][1] = index in current_state[[_][0]]
        """
        columns = list()
        for _ in range(1, len(current_state)):
            if current_state[_][0] == lift:
                columns.append((_, 0))
            if current_state[_][1] == lift:
                columns.append((_, 1))

        for dx in [-1, 1]:
            # Prevent impossible and useless states
            match dx:
                case -1:
                    # If elevator is at ground floor, it can't go down. (pruning)
                    if lift == 1:
                        continue
                    # If all elements and generators are above the lift, lift doesn't need to go down. (pruning)
                    if all(floor > lift for pair in current_state[1:] for floor in pair):
                        continue
                case 1:
                    # If the lift is at the top level, it can't go up. (pruning)
                    if lift == 4:
                        continue
                    # If all elements and generators are below the lift, lift doesn't need to go up. (pruning)
                    if all(floor < lift for pair in current_state[1:] for floor in pair):
                        continue
                    
            # Create possible new states
            for _ in range(len(columns)):  # Syntax example columns: [(1, 1), (2, 1)]
                for __ in range(_, len(columns)):

                    c1 = columns[_]
                    c2 = columns[__]

                    possible_new_state = current_state.copy()  # Shallow copy is sufficient for tuples

                    possible_new_state[0] += dx  # Set next position for lift

                    if c1[1] == 0:
                        possible_new_state[c1[0]] = (possible_new_state[c1[0]][0] + dx, possible_new_state[c1[0]][1])
                    elif c1[1] == 1:
                        possible_new_state[c1[0]] = (possible_new_state[c1[0]][0], possible_new_state[c1[0]][1] + dx)

                    # If c1 == c2, only 1 non-lift position is adjusted, else 2 non-lift positions
                    if c1 != c2:
                        if c2[1] == 0:
                            possible_new_state[c2[0]] = (possible_new_state[c2[0]][0] + dx, possible_new_state[c2[0]][1])
                        elif c2[1] == 1:
                            possible_new_state[c2[0]] = (possible_new_state[c2[0]][0], possible_new_state[c2[0]][1] + dx)
                    if possible_new_state:= self._validate_state(possible_new_state, seen):  # Validation returns sorted state
                        new_states.append(possible_new_state)
                        seen.add(tuple(possible_new_state))

        return new_states, seen

    def _validate_state(self, possible_state: list[int | tuple[int, int]],
                        seen: set[tuple[int | tuple[int, int], ...]]) \
                        -> list[int | tuple[int, int]] | None:
        """
        Validates possible state.

        Validation criteria:
            1. Form not in seen set.
            2. No microchip is exposed to another generator
               without its own generator present.

        Returns
        -------
        Sorted valid state OR None if invalid.

        Complexity
        ----------
        O(n^2) due to nested comparison loop.

        Suggestion for improvement:
            Floor-based hash structure could reduce to O(n).
            See documentation at the top for example code.
        """
        sorted_possible_new_state = self._sort(possible_state)

        if tuple(sorted_possible_new_state) in seen:
            return None

        for _ in range(1, len(sorted_possible_new_state)):
            # sorted_possible_new_state[_][0] = generator
            # sorted_possible_new_state[_][1] = chip
            if sorted_possible_new_state[_][0] != sorted_possible_new_state[_][1]:  # If chip and generator positions are equal, they are always valid.
                # Chip is on a floor without it's own generator, therefore exposed
                for __ in range(1, len(sorted_possible_new_state)):
                    if sorted_possible_new_state[__][0] == sorted_possible_new_state[_][1]:
                        # chip is on a floor with another generator, therefore will be destroyed
                        return None

        return sorted_possible_new_state

    def _sort(self, unsorted_state: list[int | tuple[int, int]]) -> list[int | tuple[int, int]]:
        """
        Sorts state for symmetry reduction.

        Sorting ensures states differing only by
        element ordering are treated as identical.

        Example:
            [1, (2,1), (3,1)]
            [1, (3,1), (2,1)]

        Both become:
            [1, (2,1), (3,1)]

        Returns
        -------
        Sorted state preserving elevator position.

        Complexity
        ----------
        O(n log n)
        """
        lift = unsorted_state[0]
        sorted_state = sorted(unsorted_state[1:])
        return [lift] + sorted_state


class Solver:
    """
    Implements Breadth-First Search (BFS)
    to find the minimum number of steps
    required to reach the goal state.

    BFS guarantees optimal solution
    in unweighted state graph.

    Uses:
        - deque for FIFO frontier
        - set for visited states

    Memory intensive due to exponential state growth.
    """
    def __init__(self, state_handler: StateHandler):
        self.seen: set[tuple[int | tuple[int, int], ...]] = set()
        self.state_handler = state_handler

    def solve(self, initial_state: list[int | tuple[int, int]]) -> int:
        """
        Executes BFS from initial state
        until goal state is reached.

        Returns
        -------
        int
            Minimum number of steps required.

        Algorithm
        ---------
        Standard BFS:
            - Pop from frontier
            - Check goal
            - Expand neighbors
            - Enqueue unseen states

        Complexity
        ----------
        O(S * n^4)
            S = number of reachable states

        BFS is optimal but memory-heavy.
        """
        goal_state = self.state_handler.create_goal_state(initial_state)

        frontier = deque()
        frontier.append((0, initial_state))

        while frontier:
            state_to_process = frontier.popleft()

            # If goal state is reacher, return number of steps
            if state_to_process[1] == goal_state:
                return state_to_process[0]

            next_states = self._get_new_states(state_to_process[1])

            for next in next_states:
                frontier.append((state_to_process[0]+1, next))

    def _get_new_states(self, current_state: list[int | tuple[int, int]]) -> list[list[int | tuple[int, int]]]:
        """
        Wrapper around StateHandler.create_new_states.

        Separates solver orchestration
        from state generation logic.

        Returns
        -------
        List of validated successor states.
        """
        new_states, self.seen = self.state_handler.create_new_states(current_state, self.seen)

        return new_states


def main():
    """
    Entry point.

    Executes:
        - Data extraction
        - Initial state construction
        - Part 1 solution
        - Part 2 solution

    Note
    -----
    Separate solver instances are used to avoid
    shared visited-state contamination.
    """

    data_handler = DataHandler(test)
    data = data_handler.etl()
    
    state_handler = StateHandler()
    
    initial_state = state_handler.create_initial_state(data)

    solver_part_1 = Solver(state_handler)
    result_part_1 = solver_part_1.solve(initial_state)

    extended_state = state_handler.add_extra_pairs(initial_state)  # Part 2 requires additional elements
    solver_part_2 = Solver(state_handler)
    result_part_2 = solver_part_2.solve(extended_state)

    print(f"The path to the goal state of part 1 requires: {result_part_1} steps")
    print(f"The path to the goal state of part 2 requires: {result_part_2} steps")


if __name__ == "__main__":
    main()
