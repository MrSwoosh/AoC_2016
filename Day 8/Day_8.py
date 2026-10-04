"""
Possible solution for Advent of Code 2016 Day 8
https://adventofcode.com/2016/day/8

Date: October 2026


Description
    The algorithm simulates a small screen consisting of a matrix with 6 rows and 50 columns.
    Each position in the matrix represents a pixel. A dot (.) represents an unlit pixel
    and a hash (#) represents a lit pixel.

    The input consists of instructions that modify the screen. There are three possible operations:
    rect AxB
        Turns on all pixels in a rectangle with width A and height B,
        starting in the upper-left corner of the screen.
    rotate row y=A by B
        Shifts all pixels in row A to the right by B positions.
        Pixels that move beyond the right edge wrap around to the left side.
    rotate column x=A by B
        Shifts all pixels in column A down by B positions.
        Pixels that move beyond the bottom edge wrap around to the top.

Time complexity
    load_data():       O(n * m)
    create_matrix():   O(m * n)
    solve_part_1():    O(n * m * n)
    draw_square():     O(m * n)
    shift_row():       O(m)
    shift_column():    O(m * n)
    lit_count():       O(m * n)
    solve_part_2():    O(m * n)

    Where n represents the number of instructions and m represents the number of pixels in one dimension of the matrix.
    More specifically, the matrix has a fixed size of 6 x 50, so the matrix-related operations are effectively
    constant time for the given problem.

Possible improvements
    shift_column() is unnecessarily complicated. The matrix is rotated four times to simulate a column rotation.
    A direct implementation that extracts the specified column, shifts its values and inserts them back into the matrix
    would be considerably easier to understand and maintain.

    solve_part_1() currently returns the final matrix, which is appropriate because the matrix is also required by
    solve_part_2(). An earlier implementation returned only the number of lit pixels, which would have required
    processing the instructions twice to solve both parts.
    Returning the matrix avoids this unnecessary second calculation.

    The matrix is represented as a list of strings. Since strings are immutable, changing individual pixels requires
    creating a new string or reconstructing the row. A representation using lists of characters would make individual
    pixel modifications more straightforward.

    The dimensions of the matrix are currently hard-coded in create_matrix(). Passing the width and height as
    parameters would make the function more reusable.

    The complexity notation can be simplified for this particular problem. Because the screen always consists of
    only 6 x 50 pixels, all matrix operations operate on a fixed-size data structure. Consequently, with respect to
    the number of input instructions, the complete solution effectively has O(n) time complexity.
"""


def load_data() -> list[str]:
    """
    Retrieves data from file
    :return: List with string elements
    """
    with open("dataset_day_8", "r") as file:
        return [line.strip() for line in file.readlines()]


def create_matrix() -> list[str]:
    """
    Creates matrix.
    :return: Matrix (list of strings)
    """
    return ['.' * 50 for x in range (6)]


def solve_part_1(instructions: list[str], matrix_1: list[str]) -> list[str]:
    """
    solve_part_1() processes every instruction sequentially.
    The instruction is first split into its type and parameters.
    Depending on the instruction, either draw_square(),
    shift_row() or shift_column() is called.
    The resulting matrix is returned after all instructions have been processed.
    :param instructions: Instructions for adjusting the matrix.
    :param matrix_1: Matrix to be used in solving part 1.
    :return: Adjusted matrix
    """
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

    return matrix_1


def draw_square(original_matrix: list[str], square_x: int, square_y: int) -> list[str]:
    """
    draw_square() modifies the specified number of rows and replaces the first specified number of pixels in each row with #.
    :param original_matrix: matrix pre-square
    :param square_x: Square width.
    :param square_y: Square height.
    :return: Adjusted matrix
    """
    for y in range(square_y):
        original_matrix[y] = '#' * square_x + original_matrix[y][square_x:]
    return original_matrix


def shift_row(original_matrix: list[str], row_number: int, num_shifts: int) -> list[str]:
    """
    shift_row() performs a circular right shift on one row. The row is divided into two parts:
    the pixels that need to wrap around and the remaining pixels. The two parts are then concatenated in reverse order.
    :param original_matrix: Matrix pre-shift
    :param row_number: Row number (int)
    :param num_shifts: Number of shifts (int)
    :return: Adjusted matrix
    """
    to_shift = original_matrix[row_number][len(original_matrix[row_number]) - num_shifts: ]
    remaining = original_matrix[row_number][: len(original_matrix[row_number]) - num_shifts]
    original_matrix[row_number] = to_shift + remaining

    return original_matrix


def shift_column(original_matrix: list[str], column_number: int, num_shifts: int) -> list[str]:
    """
    shift_column() performs a circular downward shift on a column.
    Because the matrix is represented as a list of strings,
    directly modifying a column is inconvenient.
    The function therefore rotates the entire matrix
    90 degrees counter-clockwise, performs the required row shift,
    and then rotates the matrix three more times.
    This effectively restores the original orientation while keeping
    the shifted column in the correct position.
    :param original_matrix: Matrix pre-shift
    :param column_number: Column number (int)
    :param num_shifts: Number of shifts (int)
    :return: Adjusted matrix
    """
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


def lit_count(final_matrix: list[str]) -> int:
    """
    lit_count() counts all lit pixels in the final matrix.
    Iterates over every row and uses count('#') to determine
    how many pixels are lit in that row.
    :param final_matrix: Final matrix needed for solution to part 1.
    :return: Solution to part 1 (int)
    """
    lit_pixels = 0
    for row in final_matrix:
        lit_pixels += row.count('#')
    return lit_pixels


def solve_part_2(matrix_2: list[str]) -> None:
    """
    Replaces '.' with ' ' in matrix for readability
    and prints matrix to show solution.
    :param matrix_2: Matrix which solved part 1.
    :return: None
    """
    matrix_to_print = []
    for i in range (len(matrix_2)):
        matrix_to_print.append(matrix_2[i].replace('.', ' '))

    for row in matrix_to_print:
        print(row)



if __name__ == '__main__':
    data = load_data()
    matrix = create_matrix()

    matrix = solve_part_1(data, matrix)
    print(f'Answer to part 1: {lit_count(matrix)}')

    print('Answer to part 2:')
    solve_part_2(matrix)
