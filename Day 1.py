"""
Possible solution to Advent of Code 2016 Day 1
https://adventofcode.com/2016/day/1

Given a list of navigation instructions where:
    instruction[0] = direction ('L', 'R')
        L = turn left
        R = turn right
    instruction[1:] = travel distance (integer)
For each instruction adjust the direction,
then travel the distance, within a grid.
Finally, calculate the Manhattan Distance
between start- and endpoint.

Solutions to part 1 and 2 are separated on purpose.
The most efficient solution would be to solve both parts at the same run,
making the total time complexity O(n) instead of 2 separate O(n) solutions.
But part 2 unlocks after part 1 has been solved.
The separation of the solutions reflects this order.

Time complexity:
    First solution: O(I)
        I = number of instructions
    Second solution: O(S)
        S = total number of traveled steps

Possible improvements:
    find_first_solution()
        * directions could be replaced with Enum
    find_second_solution()
        * +1 and -1 for x, dx, y and dy can be improved
        * Reduce number of conditionals
            Return would be a good replacement,
            but then the print statement with the solution
            can't be in the same function.
        * is the print statement in else true?
            If an instruction in the dataset was L0 or R0,
            the start position and target position are correct and equal.
            Which means there is no error.
"""



test = False


"""
Load the puzzle input from disk.

Returns:
    List of navigation instructions.
"""
def load_from_file() -> list[str]:
    with open("dataset_day_1", "r") as file:
        return file.readline().strip().split(", ")


"""
Execute all navigation instructions.

Prints the Manhattan distance for part 1 and returns the end position after each instruction for use in part 2.

Args:
    data: Navigation instructions.

Returns:
    List with end positions of every instruction.
"""
def find_first_solution(data: list[str]) -> list[tuple[int, int]]:

    positions_seen = []

    adjustment = {'L': -1, 'R': 1}

    direction = 0

    x, y = 0, 0

    for instruction in data:
        direction += adjustment[instruction[0]]

        direction += 4
        direction %= 4

        distance = int(instruction[1:])

        match direction:
            case 0:
                y += distance
            case 1:
                x += distance
            case 2:
                y -= distance
            case 3:
                x -= distance

        positions_seen.append((x, y))

    print(f"First solution: {abs(x) + abs(y)}")

    return positions_seen


"""
Find the first location that is visited twice.

Prints the Manhattan distance to that location.

Args:
    positions_visited:
        End position after every instruction.
"""
def find_second_solution(positions_visited: list[tuple[int, int]]) -> None:

    x, y = 0, 0

    visited = {(x, y)}

    visited_twice = None

    for position in positions_visited:

        if visited_twice is None:
            dx, dy = position

            if dx != x:

                if x < dx:
                    for x_dx in range(x+1, dx+1):
                        if (x_dx, y) in visited:
                            visited_twice = (x_dx, y)
                            break
                        else:
                            visited.add((x_dx,y))

                elif dx < x:
                    for dx_x in range(x-1, dx-1, -1):
                        if (dx_x, y) in visited:
                            visited_twice = (dx_x , y)
                            break
                        else:
                            visited.add((dx_x , y))

            elif dy != y:

                if y < dy:
                    for y_dy in range(y+1, dy+1):
                        if (x, y_dy) in visited:
                            visited_twice = (x, y_dy)
                            break
                        else:
                            visited.add((x, y_dy))

                elif dy < y:
                    for dy_y in range(y-1, dy-1, -1):
                        if (x, dy_y) in visited:
                            visited_twice = (x, dy_y)
                            break
                        else:
                            visited.add((x, dy_y))

            else:
                print("Something went wrong in function find_second_solution()")

            x, y = dx, dy

        else:
            break

    print(f"Second solution: {abs(visited_twice[0]) + abs(visited_twice[1])}")


if __name__ == "__main__":

    raw_data = ["R8", "R4", "R4", "R8"] if test else load_from_file()

    if test: print("Expected solution to part 1: 8")

    positions = find_first_solution(raw_data)

    if test: print("Expected solution to part 2: 4")

    find_second_solution(positions)
