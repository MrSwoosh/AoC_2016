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
    load_data():            O(n * m)
    create_dictionary():    O(m * c)   -> O(m)
    build_dictionary:       O(n * m)
    Solve_part_1:           O(m * c)   -> O(m)
    Solve_part_2:           O(m * c)   -> O(m)

        Where:
            n = number of lines
            m = number of columns
            c + number of characters in (lower case) alphabet, which is a constant

Possible improvements:

"""


def load_data() -> list[str]:
    """
    Retrieves data from file
    :return: List with string elements
    """
    with open("dataset_day_6", "r") as file:
        return [line.strip() for line in file.readlines()]


def solve_part_1(dictionary: dict[int, dict[str, int]]) -> str:
    """
    Finds the character with the highest number of appearances for each column.
    Combines the resulting characters to a new string.

    :param dictionary: Holds a dictionary of character appearances for each column
    :return: Combined string of characters with the highest appearances for each column
    """
    result = []

    for i in range(len(data[0])):
        result.append(max(dictionary[i], key=dictionary[i].get))

    return ''.join(result)


def solve_part_2(dictionary: dict[int, dict[str, int]]) -> str:
    """
        Finds the character with the lowest number of appearances for each column.
        Combines the resulting characters to a new string.

        :param dictionary: Holds a dictionary of character appearances for each column
        :return: Combined string of characters with the lowest appearances for each column
        """
    result = []

    for i in range(len(data[0])):
        result.append(min(dictionary[i], key=dictionary[i].get))

    return ''.join(result)


def create_dictionary(num_columns: int) -> dict[int, dict[str, int]]:
    """
    Creates a dictionary with each letter of the alphabet for each column.
    Creation of the dictionary is hard coded, because it eliminates the need to
    check if a key exists when filling the dictionary with values for characters.

    Key of the dictionary is equal to the column number.

    :param num_columns: Number of columns in the dataset
    :return: dictionary of dictionaries with all letters of the alphabet for each column
    """
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


def build_dictionary(data: list[str], dictionary: dict[int, dict[str, int]]) -> dict[int, dict[str, int]]:
    """
    Iterate through each element in data. The index of the character in the element
    is its column. For each column the appearances of the character is added to the dictionary.

    Example:
        When:
            data = ['abcde', 'fghij', 'apppp']
        Then:
            dictionary[0]['a'] = 2
            dictionary[0]['f'] = 1
            dictionary[0]['e'] = 0
            dictionary[2]['c'] = 1
            dictionary[2]['h'] = 1
            dictionary[2]['f'] = 0
            dictionary[5] doesn't exist

    :param data: List of strings to be processed
    :param dictionary: Dictionary of dictionaries with all letters of the alphabet for each column, to be filled.
    :return: Filled dictionary of dictionaries with all letters of the alphabet for each column
    """
    for element in data:
        for i in range(len(element)):
            dictionary[i][element[i].lower()] += 1

    return dictionary


if __name__ == '__main__':
    data = load_data()

    dictionary = create_dictionary(len(data[0]))

    build_dictionary(data, dictionary)

    result_1 = solve_part_1(dictionary)
    print(f'Solution to part 1: {result_1}')

    result_2 = solve_part_2(dictionary)
    print(f'Solution to part 2: {result_2}')

