"""
Possible solution for Advent of Code 2016 Day 5.
https://adventofcode.com/2016/day/5

Date: November 2025

Description:
    Find a password by hashing a given string.

    Part 1
    Paste an increasing integer value to the string and hash it. If the first 5 characters
    of the resulting hash are only zero's, paste the 6th character to the password.
    Continue until all 8 characters of the password have been found.

    Part 2
    Paste an increasing integer value to the string and hash it. If the first 5 characters
    of the resulting hash hare only zero's, the 7th character indicates the position
    in the password that may receive the 6th character in the hash. Only place the
    character in the password if no other character has been found for that position.
    Continue until all 8 characters of the password have been found.

Time complexity:
    Solve_part_1: O(n)
    Solve_part_2: O(n)

        Where n = number of hashes, meaning n could be infinite

Possible improvements:
    Overall: Combine hashing for both parts, to reduce number of iterations needed.
"""


import hashlib


def solve_part_1(seed: str, password_length: int) -> str:
    """
    Takes an input string and pasts an integer value to it.
    Hash the resulting string. If string starts with '00000',
    paste value on index 5 to password.
    Increase integer value and repeat until password has been found.

    :param seed: String used as a seed value for hashing
    :param password_length: Integer value to set the length of password
    :return: Constructed password
    """
    password_part1 = ""

    counter = 0
    while len(password_part1) < password_length:

        hash_result = hashlib.md5((seed + str(counter)).encode()).hexdigest()

        if hash_result.startswith("00000"):
            password_part1 += hash_result[5]

        counter += 1


    return password_part1


def solve_part_2(seed: str, password_length: int) -> str:
    """
    Takes an input string and pasts an integer value to it.
    Hash the resulting string. If string starts with '00000',
    value on index 7 indicates where the character of index 6 is to be inserted
    in password. Only insert character if no other character has been found.
    Increase integer value and repeat until complete password has been found.

    :param seed: String used as a seed value for hashing
    :param password_length: Integer value to set the length of password
    :return: Constructed password
    """
    password_part2 = ['' for i in range(password_length)]

    digits_found = 0
    counter = 0
    while digits_found < password_length:

        hash_result = hashlib.md5((seed + str(counter)).encode()).hexdigest()

        if hash_result.startswith("00000"):
            try:
                pos = int(hash_result[5])
                if pos < password_length and password_part2[pos] == '':
                    password_part2[pos] = hash_result[6]
                    digits_found += 1
            except ValueError:
                pass

        counter += 1

    return ''.join(password_part2)



if __name__ == "__main__":
    seed = "uqwqemis"

    print(f"Result part 1 = {solve_part_1(seed)}")

    print(f"Result part 2 = {solve_part_2(seed, 8)}")