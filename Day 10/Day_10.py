"""
Possible solutions for Advent of Code 2016 Day 10
https://adventofcode.com/2016/day/10

Date: October 2026


Description


    Part 1


    Part 2


Time complexity
    load_data:
    solve_part_1:
    solve_part_2:


Possible improvements

"""


def load_data():
    """
    Retrieves the data from the input file.
    :return: String of input data
    """
    with open("dataset_day_9", "r") as file:
        return file.readline().strip()


def solve_part_1(instructions) -> int:
    pass


def solve_part_2(instructions) -> int:
    pass



if __name__ == '__main__':
    data = load_data()

    result_1 = solve_part_1(data)
    print(f"Answer to part 1: {result_1}")

    result_2 = solve_part_2(data)
    print(f"Answer to part 2: {result_2}")
