"""
Possible solution for Advent of Code 2016 day 17.
https://adventofcode.com/2016/day/17
Date: 22-07-2026
Complexity:

A brief note about the structure/syntax:
    Python is my preferred language for DSA puzzles, prototyping and small programs.
    But the university forces me to use Java 8 in order to learn OO Programming, Design and Analysis.
    When I started learning Java, I spend far too much time and energy on bashing the need to declare datatypes at every turn.
    But after a few months of yelling at my screen, I started declaring the types automatically and to my surprise it really helped me understand someone else's code
    much faster. The latter helped me when working for clients to such a degree, I became a big fan of declaring types everywhere I can.
    The structure/syntax you see in this script, is an attempt to implement every convention and tip I could find to convey as much detail as possible, while still keeping it clear and clean.
    There is a stronger focus on type annotations than on documentation, because the annotation will make the documentation redundant.


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
    Open/closed state of doors are determined by an MD5 hash.
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

    Every A* algorithm I've seen, sorts the frontier (list) to calculate
    the paths in ascending order (on estimated total distance). But I don't like that,
    because there is no need for it. You need to calculate the paths in ascending order,
    but there is no need to sort the frontier after every calculation.
    You just need the current lowest estimated distance.
    So min() is enough and results in O(n) instead of O(n log n),
    to determine the next path to calculate.
    The use of a (dynamic) array as the datatype for the frontier also bugs me,
    because even though lists are very useful, if they keep changing size,
    they're also inefficient. The use of a (hash)map would be an improvement,
    but making the type declarations clear sounds like a maze. The next best thing
    would be a Linked List. I haven't used a Linked List for anything yet and I would
    like to have that opportunity. Therefor I will be using a Linked List for the frontier
    on every attempt to solve this challenge, unless it turns out to be extremely ineffective.

Suggestions for improvements:

"""

import hashlib


test = True
passcode = 'hijkl' if test else 'edjrjqaa'


"""
Utility class to separate hashing from other classes,
in case hashing method changes for part 2.

Static class inside main script, 
to prevent the need to import Hashing.py
"""
class Hashgenerator:

    @staticmethod
    def generate_hash(code          : str,
                      current_path  : str
                      )             -> str:
        return hashlib.md5((code + current_path).encode("utf-8")).hexdigest()


"""
Utility class to group all types of calculation together,
for easy maintenance/expansion.

Static class inside main script, 
to prevent the need to import Calculator.py
"""
class Calculator:

    @staticmethod
    def estimate_distance(start_position  : tuple[int, int],
                          goal_position     : tuple[int, int]
                          )                 -> int:
        x1, y1 = start_position
        x2, y2 = goal_position

        return abs(x1 - x2) + abs(y1 - y2)


    @staticmethod
    def estimate_total_distance(steps_traveled  : int,
                                steps_to_go     : int
                                )               -> int:
        return steps_traveled + steps_to_go


class Validdirections:

    @staticmethod
    def get_valid_directions(position   : tuple[int, int],
                             hash_path  : str
                             )          -> list[str]:
        open_states = {'b', 'c', 'd', 'e', 'f'}

        valid_directions = []

        x, y = position

        # Is Up valid?
        if 0 < x:
            if hash_path[0] in open_states:
                valid_directions.append('U')
        # Is Down valid?
        if x < 3:
            if hash_path[1] in open_states:
                valid_directions.append('D')
        # Is Left valid?
        if 0 < y:
            if hash_path[2] in open_states:
                valid_directions.append('L')
        # Is Right valid?
        if y < 3:
            if hash_path[3] in open_states:
                valid_directions.append('R')

        return valid_directions




"""
Class to handle all needs regarding Path objects.

Path objects are connected via a Linked List.

Keeps track of the first Path object to have a starting point for list iterations.

Transforms a path into new paths, or auto deletes it when there are no new possible paths.
"""
class Pathmanager:
    passcode    = str()
    first       = None


    def __init__(self,
                 passcode   : str
                 )          -> None:
        self. passcode = passcode


    def create_paths(self,
                     position   : tuple[int, int],
                     path       : str
                     )          -> None:
        hashed_path = Hashgenerator.generate_hash(self.passcode, path)
        directions = Validdirections.get_valid_directions(position, hashed_path)

        for d in directions:
            new_position = self.get_next_position(position, d)

            new_path = Path(path)




            if self.first is not None:
                new_path.set_prev_path(self.first)

            self.first = new_path


    def get_next_position(self,
                          current_position  : tuple[int, int],
                          direction         : str
                          )                 -> tuple[int, int]:
        match direction:
            case 'U':
                return (current_position[0] - 1, current_position[1])
            case 'D':
                return (current_position[0] + 1, current_position[1])
            case 'L':
                return (current_position[0], current_position[1] - 1)
            case 'R':
                return (current_position[0], current_position[1] + 1)

        raise ValueError(f"Unknown direction: {direction}")





class Path:
    estimated_total_distance    = int()
    estimated_distance          = int()
    path                        = str()
    position                    = tuple()

    prev_path                   = None
    next_path                   = None


    def __init__(self,
                 estimated_total_distance   : int,
                 estimated_distance         : int,
                 path                       : str,
                 position                   : tuple[int, int]
                 )                          -> None:
        self.estimated_total_distance = estimated_total_distance
        self.estimated_distance = estimated_distance
        self.path = path
        self.position = position


    def set_prev_path(self,
                      path: Path
                      )     -> None:
        self.prev_path = path


    def set_next_path(self,
                      path: Path
                      )     -> None:
        self.next_path = path


if __name__ == "__main__":
    pass
