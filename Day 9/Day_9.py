"""
Possible solutions for Advent of Code 2016 Day 9
https://adventofcode.com/2016/day/9

Date: October 2026


Description
    Given is 1 long string. The string contains multipliers and characters.
    Multipliers format: (<a>x<b>) where a = range scope of multiplier
    and b = the multiplication factor.

    Part 1
    Iterate through the string and count the number of characters.
    A multiplier increases the weight of a character in its scope.
    Any multiplier within the scope of a multiplier, is ignored.

    Part 2
    Similar to part 1, except multipliers within the scope of a multiplier
    does count. If any multiplier b is within the scope of multiplier a,
    then multiplier b is multiplied by multiplier a.

Time complexity
    load_data:  O(n)
    solve_part_1:  O(n)
    solve_part_2:  O(n^2)

    Where n is the length of the string

Possible improvements

"""


def load_data() -> str:
    """
    Retrieves the data from the input file.
    :return: String of input data
    """
    with open("dataset_day_9", "r") as file:
        return file.readline().strip()


def solve_part_1(line: str) -> int:
    """
    Iterates through the input line and calculates
    the number of characters in a simulated decompression.
    Searches for a multiplier in format '(<a>x<b>)',
    where a = range scope of multiplier and b = the multiplication factor.
    If no multiplier is active, a character counts as 1.
    Any multiplier in the scope will be treated as a group of characters instead of another multiplier.
    :param line: String for iteration
    :return: Simulated decompression file size (int)
    """
    file_size = 0

    counter = 0
    while counter < len(line):
        if line[counter] == "(":
            multiplier = ''

            sub_counter = counter + 1
            while True:
                if line[sub_counter] == ")":
                    multiplier = line[counter + 1:sub_counter]
                    sub_counter += 1
                    break
                sub_counter += 1

            a, b = multiplier.split('x')

            file_size += int(a) * int(b)
            counter = sub_counter + int(a)

        else:
            counter += 1
            file_size += 1

    return file_size


def solve_part_2(line: str) -> int:
    """
    For part 2, sub multipliers do count as multipliers. Meaning there are subcalculations needed.
    Works similar to solve_part_1, but adjusted to use recursion for subcalculations.
    :param line: String for iteration
    :return: Simulated decompression file size (int)
    """
    file_size = 0

    counter = 0
    while counter < len(line):
        if line[counter] == "(":
            multiplier = ''

            sub_counter = counter + 1
            while True:
                if line[sub_counter] == ")":
                    multiplier = line[counter + 1:sub_counter]
                    sub_counter += 1
                    break
                sub_counter += 1

            a, b = multiplier.split('x')

            file_size += solve_part_2(line[sub_counter:sub_counter + int(a)]) * int(b)
            counter = sub_counter + int(a)

        else:
            counter += 1
            file_size += 1

    return file_size


if __name__ == "__main__":
    data = load_data()

    result_1 = solve_part_1(data)
    print(f"Answer to part 1: {result_1}")

    result_2 = solve_part_2(data)
    print(f"Answer to part 2: {result_2}")

