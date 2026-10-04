"""
Possible solution for Advent of Code 2016 Day 7
https://adventofcode.com/2016/day/7

Date: October 2026


Description:
    A list of IPv7 addresses is given. An address consists of supernet
    sequences and hypernet sequences. Hypernet sequences are enclosed
    between square brackets.

    Part 1
    An address supports TLS (Transport-Layer Snooping) when:

    - At least one supernet sequence contains an ABBA pattern.
    - No hypernet sequence contains an ABBA pattern.

    An ABBA is a four-character sequence of the form ABBA, where the
    first and fourth characters are equal, the second and third
    characters are equal, and A and B are different.

    The algorithm first separates every IP address into its supernet
    and hypernet sequences using split_ip(). It then searches both
    groups for an ABBA pattern using has_abba(). First in the hypernet sequence,
    to reduce the number of iterations needed; if the hypernet sequence contains a pattern,
    the address can't support TLS. An IP is counted when at least one ABBA occurs in
    a supernet sequence and none occurs in a hypernet sequence.

    Part 2
    An IPv7 address supports SSL (Super-Secret Listening) when a
    corresponding ABA pattern occurs in a supernet sequence and its
    corresponding BAB pattern occurs in a hypernet sequence.

    An ABA is a three-character sequence of the form ABA, where the
    first and third characters are equal and the middle character is
    different. For example, "xyx" is an ABA. Its corresponding BAB is
    "yxy".

    The algorithm first separates every IP address into supernet and
    hypernet sequences. get_pattern() then extracts all ABA patterns
    from the supernets and all BAB patterns from the hypernets.
    The two sets are compared by compare_patterns(). If a
    pattern occurs in both sets, the IP supports SSL.


Time complexity:
    load_data():        O(n * m)
    solve_part_1():     O(n * m)
    solve_part_2():     O(n * m)
    has_abba():         O(m)
    get_pattern():      O(m)
    compare_patterns(): O(m)
    split_ip():         O(m)

    Where:
        n = number of IP addresses
        m = maximum length of an IP address


Possible improvements:
    solve_part_1/2 both split the IP address, should be reduced to 1 split
    Make names more descriptive
    split_ip() could use regex,
        but current functionality is more efficient
        because it only iterates through the string once.
"""


def load_data() -> list[str]:
    """
    Every line in the input file is read and stripped.
    :return: List of strings
    """
    with open('dataset_day_7') as file:
        return [line.strip() for line in file.readlines()]


def solve_part_1(ip_data: list[str]) -> int:
    """
    The algorithm processes all n IP addresses. For each address,
    split_ip() scans the complete address in O(m) time. The calls to
    has_abba() together inspect all characters in the resulting
    sequences. Because the sequences together contain O(m)
    characters, this also takes O(m) time per IP address.
    :param ip_data: List op IP addresses (string)
    :return: solution to part 1 (int)
    """
    tls_ips = 0
    for ip in ip_data:
        supernets, hypernets = split_ip(ip)

        if not any(has_abba(hypernet) for hypernet in hypernets):
            if any(has_abba(address_part) for address_part in supernets):
                tls_ips += 1

    return tls_ips


def has_abba(string: str) -> bool:
    """
    The function checks every group of four consecutive characters.
    Searches for string format '<x><y><y><x>'
    For a string of length m, there are m - 3 possible starting
    positions. Each position requires a constant amount of work.
    :param string: Part of IP address (string)
    :return: Whether the string contains a valid pattern consecutive characters (bool)
    """
    for i in range(len(string) - 3):
        if string[i] == string[i + 3]:
            if string[i + 1] == string[i + 2]:
                if string[i] != string[i + 1]:
                    return True

    return False


def solve_part_2(ip_data: list[str]) -> int:
    """
    Each IP address is split in O(m) time. get_pattern() scans all
    characters in the supernet and hypernet sequences, which together
    contain O(m) characters. compare_patterns() performs set
    membership checks, which are O(1) on average, for each extracted
    pattern.
    :param ip_data: List op IP addresses (string)
    :return: solution to part 1 (int)
    """
    ssl_ips = 0
    for ip in ip_data:
        supernets, hypernets = split_ip(ip)

        supernet_patterns = get_patterns(supernets)
        hypernet_patterns = get_patterns(hypernets, True)

        if compare_patterns(supernet_patterns, hypernet_patterns):
            ssl_ips += 1

    return ssl_ips


def get_patterns(nets: list[str], hyp=False) -> set[str]:
    """
    The function examines every group of three consecutive
    characters in every supplied sequence. If a valid ABA is found,
    it is added to a set. If a pattern is found in a hypernet sequence,
    its pattern is flipt from '<x><y><x>' tot '<y><x><y>' for easy
    comparison by compare_patterns().
    :param nets: List of supernet sequences
    :param hyp: List of hypernet sequences
    :return: Set of (string) patterns
    """
    patterns = set()

    for net in nets:
        for i in range(len(net) - 2):
            if net[i] == net[i + 2] and net[i] != net[i + 1]:
                if hyp:
                    patterns.add(net[i+1] + net[i]+ net[i+1])
                else:
                    patterns.add(net[i:i + 3])

    return patterns


def compare_patterns(sup_nets: set[str], hyp_nets: set[str]) -> bool:
    """
    The function iterates over the patterns in sup_nets and checks
    whether each pattern exists in hyp_nets. Since hyp_nets is a set,
    membership checking takes O(1) time on average.
    :param sup_nets: Set of supernet patterns
    :param hyp_nets: Set of hypernet patterns
    :return: Whether any supernet pattern has a corresponding hypernet pattern (bool)
    """
    return any(s_net in hyp_nets for s_net in sup_nets)


def split_ip(address: str) -> tuple[list[str], list[str]]:
    """
    The function scans the complete IP address exactly once. For
    every character it performs a constant amount of work and adds
    characters to either a supernet or hypernet sequence.
    :param address:
    :return:
    """
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

    result_part_2 = solve_part_2(data)
    print(f'Answer to part 2: {result_part_2}')
