"""
Possible solution for Advent of Code 2016 Day 4.
https://adventofcode.com/2016/day/4

Date: October 2026

Description:
    Room names have been encrypted. Each name consists of strings separated by a dash,
    followed by a room number and a hash in brackets.
    Example: aaaaa-bbb-z-y-x-123[abxyz]
    Part 1
        For each letter count its appearance. Sort the number of appearances in descending order.
        If 2 letters appear the same number of times, order them alphabetically.
        The example given above is a valid room.

        If the sorted order is equal to the order of the hash, the room is valid.
        What is the sum of the room numbers of the valid rooms?
    Part 2
        Basic shift cipher. Shift each letter in the room name
        by the value of the room number. Only lower case letters are used.
        The shift creates the unencrypted room name.
        What is the room number of the room that contains the North Pole objects?


Time complexity:
    Solve_part_1: O(m * n)
    Solve_part_2: O(m * n)

    Where:
        m = number of rooms
        n = maximum length of room name

Possible improvements:
    load_data: building name can be more efficient.
    load_data: including '-' in name creation is not needed.
    Solve_part_2: transformation of '-' to ' ' is not needed.
        If transformation is removed, 1 less conditional is needed in pattern matching.
"""


def load_data() -> list[dict[str, str]]:
    """
    Loads and transforms data from input file.

    Input syntax:  <string>-...<int>[<string>]
         Example: aczupnetwp-dnlgpyrpc-sfye-dstaatyr-561[patyc]

    Transform and store input data to dictionary with labels 'hash', 'number' and 'name',
    with string values.
        Example:    aczupnetwp-dnlgpyrpc-sfye-dstaatyr-561[patyc]
                    -> {'hash': 'patyc', 'number': '561', 'name': 'aczupnetwp-dnlgpyrpc-sfye-dstaatyr'}

    :return: List of dictionaries with transformed data.
    """
    encrypted_data = []
    with open("dataset_day_4", 'r') as file:
        for row in file:
            labeled_data = dict()

            row = row.strip()[:-1].replace('[', '-')

            encrypted_name_parts = row.split('-')

            labeled_data["hash"] = encrypted_name_parts.pop()
            labeled_data["number"] = encrypted_name_parts.pop()

            name = encrypted_name_parts[0]

            for string in encrypted_name_parts[1:]:
                name += f"-{string}"

            labeled_data["name"] = name

            encrypted_data.append(labeled_data)

    return encrypted_data


def solve_part_1(encrypted_data) -> int:
    """
    Counts number of appearances of each letter in room name (ignores '-').
    Sorts descending on number of appearances of each letter in room name.
    Sorts equal appearances on alphabetical order.
    If the order of sorted letters is equal to the room hash,
    the room number is added to the sum of room numbers of valid rooms.

    :param encrypted_data: List of dictionaries with room data.
    :return: sum of room numbers of valid rooms
    """
    sum_valid_rooms = 0

    for room in encrypted_data:
        room_name = room['name'].replace('-', '')

        letter_appearances = dict()

        for char in room_name:
            if char not in letter_appearances:
                letter_appearances[char] = 1
            else:
                letter_appearances[char] += 1

        sorted_letters = list()

        for letter in letter_appearances:
            sorted_letters.append(letter * letter_appearances[letter])

        sorted_letters = sorted(sorted_letters, key=lambda x: (-len(x), x))

        if all(sorted_letters[i][0] == room['hash'][i] for i in range(len(room['hash']))):
            sum_valid_rooms += int(room['number'])

    return sum_valid_rooms


def solve_part_2(encrypted_data) -> int|None:
    """
    Transforms '-' to ' '.
    Shifts char based on room number.
    If new room name contains keywords, room number is returned.

    :param encrypted_data: List of dictionaries with room data.
    :return: room number if successful, None otherwise.
    """
    room_number = None
    for room in encrypted_data:
        room_number = int(room['number'])

        # Calculate substitution value before looping over name for pruning.
        substitution = room_number % 26

        decrypted_name = ""

        for char in room['name']:
            if char == '-':
                decrypted_name += " "
            else:
                char_value = ord(char) - ord('a') + substitution
                char_value %= 26

                decrypted_name += chr(char_value + ord('a'))

        if 'northpole' in decrypted_name or 'north pole' in decrypted_name or 'object' in decrypted_name:
            return room_number

    return room_number


if __name__ == "__main__":
    data = load_data()

    print(f"Solution to part 1: {solve_part_1(data)}")

    print(f"Solution to part 2: {solve_part_2(data)}")
