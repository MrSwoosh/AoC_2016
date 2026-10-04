"""
Possible solution for Advent of Code 2016 Day 8
https://adventofcode.com/2016/day/8

Date: October 2026


Description


Time complexity


Possible improvements
    Rotation of matrix in shift_column() is far too messy, improve it!
    solve_part_1() returns an int. Needs to return the matrix, so it can be used in solve_part_2()
"""


def load_data():
    """
    Retrieves data from file
    :return: List with string elements
    """
    with open("dataset_day_8", "r") as file:
        return [line.strip() for line in file.readlines()]


def create_matrix() -> list[str]:
    return ['.' * 50 for x in range (6)]


def solve_part_1(instructions, matrix_1) -> int:

    for instruction in instructions:
        instruction_type, *instruction_parameters = instruction.split(" ")
        match instruction_type:
            case 'rect':
                x, y = map(int, instruction_parameters[0].split('x'))
                matrix_1 = draw_square(matrix_1, x, y)
            case 'rotate':
                match instruction_parameters[0]:
                    case 'row':
                        row = int(instruction_parameters[1].split('=')[1])
                        shifts = int(instruction_parameters[-1])
                        matrix_1 = shift_row(matrix_1, row, shifts)
                    case 'column':
                        column = int(instruction_parameters[1].split('=')[1])
                        shifts = int(instruction_parameters[-1])
                        matrix_1 = shift_column(matrix_1, column, shifts)


    return lit_count(matrix_1)


def draw_square(original_matrix, square_x, square_y):
    for y in range(square_y):
        original_matrix[y] = '#' * square_x + original_matrix[y][square_x:]
    return original_matrix


def shift_row(original_matrix, row_number, num_shifts):
    to_shift = original_matrix[row_number][len(original_matrix[row_number]) - num_shifts: ]
    remaining = original_matrix[row_number][: len(original_matrix[row_number]) - num_shifts]
    original_matrix[row_number] = to_shift + remaining

    return original_matrix


def shift_column(original_matrix, column_number, num_shifts):
    rotated_matrix = []

    for x in range(len(original_matrix[0])-1, -1, -1):
        new_row = []
        for y in range(len(original_matrix)):
            new_row.append(original_matrix[y][x])
        rotated_matrix.append(''.join(new_row))

    original_matrix = shift_row(rotated_matrix, len(rotated_matrix) - column_number - 1, num_shifts)

    for _ in range(3):
        rotated_matrix = []

        for x in range(len(original_matrix[0]) - 1, -1, -1):
            new_row = []
            for y in range(len(original_matrix)):
                new_row.append(original_matrix[y][x])
            rotated_matrix.append(''.join(new_row))

        original_matrix = rotated_matrix

    return original_matrix


def lit_count(final_matrix) -> int:
    lit_pixels = 0
    for row in final_matrix:
        lit_pixels += row.count('#')
    return lit_pixels


if __name__ == '__main__':
    data = load_data()
    matrix = create_matrix()

    solution_1 = solve_part_1(data, matrix)
    print(f'Answer to part 1: {solution_1}')



