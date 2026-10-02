"""
Possible solution for Advent of Code 2016 Day 6.
https://adventofcode.com/2016/day/6

Date: November 2025

Description:
    Given is a list of strings. Each line has the same length.
    Count the number of appearances of each letter for each column.

    Part 1
    For each column, combine the characters with the highest number
    of appearances.

    Part 2
    For each column, combine the characters with the lowest number
    of appearances.

Time complexity:
load_data(): O(n)
    Solve_part_1:       O(n * m)
    Solve_part_2:       O(m * c)   -> O(m)
    build_dictionary:   O(m * c)   -> O(m)

        Where:
            n = number of lines
            m = number of columns
            c + number of characters in (lower case) alphabet

Possible improvements:
    solve_part_1 fills the dictionary and finds the max value for each column.
    The same dictionary is used for part 2 to find the lowest value. According to the single
    responsibility principle, filling the dictionary should happen in a separate function,
    and the functions for the solutions should only focus on finding their respective value.
"""


def load_data() -> list[str]:
    """
    Retrieves data from file
    :return: List with string elements
    """
    with open("dataset_day_6", "r") as file:
        return [line.strip() for line in file.readlines()]


def solve_part_1(data: list[str],
                 dictionary: dict[int, dict[str, int]]
                 ) -> str:
    result = ''

    for element in data:
        for i in range(len(element)):
            dictionary[i][element[i].lower()] += 1

    for i in range(len(data[0])):
        result += max(dictionary[i], key=dictionary[i].get)

    return result


def solve_part_2( dictionary: dict[int, dict[str, int]]) -> str:
    result = ''

    for element in data:
        for i in range(len(element)):
            dictionary[i][element[i]] += 1

    for i in range(len(data[0])):
        result += min(dictionary[i], key=dictionary[i].get)

    return result


def build_dictionary(num_columns: int) -> dict[int, dict[str, int]]:
    dictionary = dict()

    characters = {'a', 'b', 'c', 'd', 'e', 'f',
                  'g', 'h', 'i', 'j', 'k', 'l',
                  'm', 'n', 'o', 'p', 'q', 'r',
                  's', 't', 'u', 'v', 'w',
                  'x', 'y', 'z'}

    for i in range(num_columns):
        dictionary[i] = dict()

        for c in characters:
            dictionary[i][c] = 0

    return dictionary



if __name__ == '__main__':
    data = load_data()

    dictionary = build_dictionary(len(data[0]))

    result_1 = solve_part_1(data, dictionary)
    print(f'Solution to part 1: {result_1}')

    result_2 = solve_part_2(dictionary)
    print(f'Solution to part 2: {result_2}')

