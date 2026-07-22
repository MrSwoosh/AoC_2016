"""
Possible solution for Advent of Code 2016 day 17.
https://adventofcode.com/2016/day/17
Date: 22-07-2026
Complexity:

Case description:
    You are in the top left corner of a 4x4 grid (0,0).
    Your target is in the bottom right corner (3,3).
    Every grid position is surrounded by walls or doors.
    Example:
        #########
        #S| | | #
        #-#-#-#-#
        # | | | #
        #-#-#-#-#
        # | | | #
        #-#-#-#-#
        # | | |V#
        #########
        S = starting position
        E = end position
        # = wall
        | = door

    Only transitions to adjacent positions are allowed.
    Only transitions through 'open' doors are allowed.
    Open/closed state of doors are determined by a MD5 hash.
    The input for the hash is a passcode,
    plus a letter representation of each occurred transition (in order).
    Only hash[0:4] is used to determine door state.
    hash[0] = Up door
    hash[1] = Down door
    hash[2] = Left door
    hash[3] = Right door
    If hash[n] is an integer or 'a', the door is locked.
    Example:
        Position = (0,0)
        Passcode = 'hijkl'
        Path = ''
        hash[0:4] = passcode + path

        At the start there are no transitions,
        so only the passcode will be hashed.
        hash[0:4] = 'ced9'

        Up and Left are walls, so hash[0] and hash[2] are ignored.
        Hash[1] = e, so the Down door is open.
        Hash[3] = 9, so the Right door is closed.
        The only transition possible is going down.

        After transition:
            Position = (1,0)
            Path = 'D'
            hash[0:4] = passcode + path = f2bc

    How many steps are needed for the shortest path from S to E?

Algorithm description:
    First attempt will focus on A* algorithm with Manhattan Distance.

Suggestions for improvements:

"""

import hashlib


test = True

passcode = 'hijkl' if test else 'edjrjqaa'
path = ''


"""
Generates hash.
"""
def generate_hash(code: str, current_path: str) -> str :
    return hashlib.md5((code + current_path).encode("utf-8")).hexdigest()
