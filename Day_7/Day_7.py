"""
Possible solution for Advent of Code 2016 Day 7
https://adventofcode.com/2016/day/7

Date: October 2026

Description:


    Part 1


    Part 2


Time complexity:
    load_data():    O(n * m)
    solve_part_1():
    solve_part_2():
    has_abba():
    split_ip():

        Where:


Possible improvements:

"""


def load_data() -> list[str]:
    with open('dataset_day_7') as file:
        return [line.strip() for line in file.readlines()]


def solve_part_1(ip_data: list[str]) -> int:
    valid_ips = 0
    for ip in ip_data:
        address_parts, hypernets = split_ip(ip)

        if not any(has_abba(hypernet) for hypernet in hypernets):
            if any(has_abba(address_part) for address_part in address_parts):
                valid_ips += 1

    return valid_ips


def solve_part_2():
    pass


def has_abba(string: str) -> bool:
    for i in range(len(string) - 3):
        if string[i] == string[i + 3]:
            if string[i + 1] == string[i + 2]:
                if string[i] != string[i + 1]:
                    return True

    return False


def split_ip(address: str) -> tuple[list[str], list[str]]:

    address_parts = []
    hypernets = []

    hyper = False
    hypernet = []
    address_part = []
    for i in range(len(address)):
        if address[i] == '[' or i == len(address) - 1:
            if i == len(address) - 1:
                address_part.append(address[i])

            hyper = True
            hypernet = []
            address_parts.append(''.join(address_part))

        elif address[i] == ']':
            hyper = False
            address_part = []
            hypernets.append(''.join(hypernet))

        else:
            if hyper:
                hypernet.append(address[i])
            else:
                address_part.append(address[i])

    return address_parts, hypernets


if __name__ == '__main__':
    data = load_data()

    result_part_1 = solve_part_1(data)
    print(f'Answer to part 1: {result_part_1}')
