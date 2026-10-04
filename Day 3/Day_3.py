"""
Possible solution to Advent of Code 2016 Day 3
https://adventofcode.com/2016/day/3

Creation date: 23-9-2025
Modifying date: 31-08-2026

Given a list with sets of numbers, find valid sets.
A set is valid if:
    all combination of any 2 numbers > remaining number.

Time complexity:
    Loading data: O(n) where n = number of rows in input file
    First solution: O(n) where n = number of elements in list.
    Second solution: O(((n / 3) * 3) + n) -> O(n)

Possible improvements:
    Exception in case file is not found
    Safeguards to check if each row in input file follows correct syntax.
    Safeguards to check if input syntax can be devided by 3.
"""



def load_data() -> list[list[int]]:
    """
        Load and transform data from the data file.
        Input: file containing rows with numbers in string.
        Output: list of lists of integers.
        Converts numbers regardless of whitespace length.
        Time complexity: O(n) where n = number of rows in input file
    """
    with open("dataset_day_3", "r") as file:
        return [list(map(int, line.split())) for line in file]


def find_first_solution(measurements_list: list[list[int]]) -> int:
    """
        Searches for first solution.
        Checks for each element if all combinations of any 2 numbers > remaining number.

        Time complexity: O(n) where n = number of elements in list.
    """
    return sum(a + b > c and a + c > b and b + c > a for a, b, c in measurements_list)


def find_second_solution(measurements_list: list[list[int]]) -> int:
    """
        Searches for second solution.
        Creates a new list from original list,
        by popping 3 sequential elements from the list and combining their respective indexes into a new element.
        Effectively forming a 3x3 matrix out of 3 original elements and transposing it.

        The function for the first solution is used, but with the new measurements list.

        Time complexity creating the new list: O((n / 3) * 3) -> O(n)
        Time complexity searching the solution: O(n) where n = number of elements in list.
    """
    new_measurements_list = []
    for i in range(0, len(measurements_list), 3):
        for j in range(3):
            new_measurements_list.append(
                [measurements_list[i][j], measurements_list[i + 1][j], measurements_list[i + 2][j]])

    return find_first_solution(new_measurements_list)


if __name__ == "__main__":
    data = load_data()

    first_solution = find_first_solution(data)

    second_solution = find_second_solution(data)

    print(f"First solution: {first_solution}")
    print(f"Second solution: {second_solution}")