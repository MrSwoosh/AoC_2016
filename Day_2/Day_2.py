"""
Possible solution to Advent of Code 2016 Day 2.
https://adventofcode.com/2016/day/2

Creation date: 23-9-2025
Updated: 14-8-2026

Original algorithm was created before I started using Git.
I made some changes before uploading, because it was a very quick and dirty procedural algorithm.
Since it is a very small dataset for an easy puzzle, I didn't optimize anything.
Updates/changes:
    * Added documentation
    * Split algorithm into functions
    * Added if __name__ ...

Possible improvements:
    * Keypad datatypes do not match.
"""


def load_data() -> list[str]:
    """
    Loads the dataset
    """
    with open("dataset_day_2", "r") as file:
        return [line.strip() for line in file.readlines()]


def solve_part_1(instructions: list[str]) -> str:
    """
    Solution to part 1.

    Takes in a list with instructions.
    For each instruction, performs the moves step by step,
    and validates the position on the keypad.
    Returns the resulting 5 digit code to the keypad.
    """
    keypad = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    code = ''

    current_pos = (1, 1)

    for instruction in instructions:

        for move in instruction:

            match move:
                case "U":
                    current_pos = (max(0, current_pos[0] - 1), current_pos[1])
                case "D":
                    current_pos = (min(2, current_pos[0] + 1), current_pos[1])

                case "L":
                    current_pos = (current_pos[0], max(0, current_pos[1] - 1))
                case "R":
                    current_pos = (current_pos[0], min(2, current_pos[1] + 1))

                case _:
                    print("Something went wrong solving part 1..")

        code += str(keypad[current_pos[0]][current_pos[1]])

    return code


def solve_part_2(instructions: list[str]) -> str:
    """
    Solution to part 2.

    Similar to part 1, but uses a more complex keypad.

    Takes in a list with instructions.
    For each instruction, performs the moves step by step,
    and validates the position on the keypad.
    Returns the resulting 5 digit code to the keypad.
    """
    keypad = [
        ["0", "0", "1", "0", "0"],
        ["0", "2", "3", "4", "0"],
        ["5", "6", "7", "8", "9"],
        ["0", "A", "B", "C", "0"],
        ["0", "0", "D", "0", "0"]
    ]

    code = ''

    current_pos = (2, 0)

    for instruction in instructions:

        for move in instruction:
            match move:
                case "U":
                    next_pos = (max(0, current_pos[0] - 1), current_pos[1])
                case "D":
                    next_pos = (min(4, current_pos[0] + 1), current_pos[1])

                case "L":
                    next_pos = (current_pos[0], max(0, current_pos[1] - 1))
                case "R":
                    next_pos = (current_pos[0], min(4, current_pos[1] + 1))

                case _:
                    next_pos = current_pos  # This is just here because the IDE's yellow warning line bugs me
                    print("Something went wrong solving part 2..")

            if keypad[next_pos[0]][next_pos[1]] != "0":
                current_pos = next_pos

        code += (keypad[current_pos[0]][current_pos[1]])

    return code


if __name__ == "__main__":
    data = load_data()

    answer_part_1 = solve_part_1(data)

    answer_part_2 = solve_part_2(data)

    print(f"answer_part_1: {answer_part_1}")
    print(f"answer_part_2: {answer_part_2}")
