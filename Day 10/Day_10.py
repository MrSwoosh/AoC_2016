"""
Possible solutions for Advent of Code 2016 Day 10
https://adventofcode.com/2016/day/10

Date: October 2026


Description
    Bots in a factory receive and transmitting microchips.
    If a bots holds 2 microchips, it will send both chips to other bots.
    The receiving bots will be determined by a preset destination,
    noted in the puzzle input data. The values to be distributed are noted
    in the puzzle input data as well.

    Giving the bots preset connections, makes them nodes in a graph.

    Part 1
    Process the values in the puzzle input data.

    Part 2

Time complexity
    load_data():            O(n)
    transform_data():       O(n)
    setup_botnet():         O(b)
    process_values():       O(v)
    receive_values():       O(1)
    _send_values():         O(1)
    get_bot_for_part_1():   O(b)
    get_output_values():    O(k)
    get_sum():              O(1)

    Where:
        n = Number of lines in input file
        b = Number of bots/connections
        v = Number of value instructions
        k = Number of outputs requested

    Dictionary lookups and insertions are O(1) on average. A bot holds at most
    two values before processing them, so sorting the values in receive_value()
    also takes O(1). Processing the values therefore requires a constant amount
    of work per value transfer.

    The overall time complexity is O(n), because the input data is processed
    linearly and all other operations are either constant time or linear in the
    number of bots, which is bounded by the size of the input.

Possible improvements
    Checking for the 2 values to find te solution to part 1 is currently hard coded in Bot.recieve_value().
    This makes the algorithm tailored to my puzzle. Adjusting the algorithm to include
    the number as search parameters instead of hard code values, is (highly) needed.

    The current implementation represents output bins as Bot objects by
    adding 10,000 to their number. This works for the current input because
    bot numbers are below 10,000, but it is not a clean representation of
    output bins. A separate dictionary for outputs, or a common destination
    abstraction, would make the implementation more robust.

    Bot.number is not required for the bot network itself because the bot
    number is already used as the key in BotHandler.botnet. Removing this
    attribute would avoid storing duplicate information.

    The current implementation stores received_values as a list. Since a
    bot only needs to hold two values before processing them, this could be
    represented using two variables instead. This would make the intended
    maximum capacity of a bot more explicit.

    The implementation assumes that a bot will never need to process more than
    two values simultaneously. This is consistent with the puzzle rules, but
    the implementation could validate this assumption more explicitly.
"""


class BotHandler:
    """
    The BotHandler class manages the complete bot network.
    It stores all bots in a dictionary and is responsible for creating bots,
    establishing their connections, processing the initial value assignments,
    and retrieving the solutions for both puzzle parts.
    """

    def __init__(self):
        """
        Initializes an empty dictionary that will contain all bots in the bot network.

        Time complexity: O(1)
        """
        self.botnet = dict()


    def setup_botnet(self, botnet_connections: dict[int, list[int]]) -> None:
        """
        Creates the bots defined by the connection data and assigns their destinations.

        For every bot, the method checks whether the source and destination bots already exist.
        Missing bots are created and the destination references are then assigned.

        Time complexity: O(b), where b is the number of bot connections.

        :param botnet_connections: Dictionary[int, List[int]] with bot connections (like edges in a graph)
        """
        for bot in botnet_connections:
            low_bot_number = botnet_connections[bot][0]
            high_bot_number = botnet_connections[bot][1]

            # Check if bot exists
            if bot not in self.botnet:
                self._create_bot(bot)

            # Check if receiving bot exists
            if low_bot_number not in self.botnet:
                self._create_bot(low_bot_number)

            # Check if receiving bot exists
            if high_bot_number not in self.botnet:
                self._create_bot(high_bot_number)

            # Retrieve bots
            low_bot = self.botnet[low_bot_number]
            high_bot = self.botnet[high_bot_number]

            # Assign destination bots
            self.botnet[bot].set_destinations(low_bot, high_bot)


    def process_values(self, value_assignments: dict[int, list[int]]) -> None:
        """
        Processes the initial value assignments from the puzzle input.
        Each value is passed to the corresponding bot using receive_value().

        If a bot does not yet exist, it is created first.

        Time complexity: O(v), where v is the number of initial value assignments.
            receive_value() takes O(1) for each value.

        :param value_assignments: Dictionary[int, List[int]] with values for processing
        """
        for assignment in value_assignments:
            bot = assignment
            value = value_assignments[assignment]

            if bot not in self.botnet:
                self._create_bot(bot)
            bot = self.botnet[bot]

            for v in value:
                bot.receive_value(v)


    def _create_bot(self, bot_number: int) -> None:
        """
        Creates a new Bot object and adds it to the bot network using the bot number as dictionary key.

        Time complexity: O(1)

        :param bot_number:
        """
        self.botnet[bot_number] = Bot(bot_number)


    def get_bot_for_part_1(self) -> int | None:
        """
        Searches the bot network for the bot that processed the target values for part 1.

        The method iterates over all bots until a bot with target_for_part_1 == True is found.

        Time complexity: O(b)

        :return: Bot number of bot that processed the target values for part 1
        """
        for bot in self.botnet:
            if self.botnet[bot].target_for_part_1:
                return self.botnet[bot].number

        return None


    def get_output_values(self, output_list: list[int]) -> int:
        """
        Retrieves the values from the specified output bins and multiplies them together.

        Output bins are represented by Bot objects with their number increased by 10,000.

        Time complexity: O(k), where k is the number of requested outputs (k = 3 for this puzzle).

        :param output_list: List with output numbers for value retrieval
        :return: Sum (int) of output values
        """
        value = 1
        for number in output_list:
            value *= self.botnet[number + 10_000].get_sum()

        return value



class Bot:
    """
    The Bot class represents a bot or output bin in the network.
    A bot can receive values, store them until it has two values,
    and then send the lower and higher values to its configured destinations.

    Bots will hold a value to indicate if they had to process 17 and 61.
    It is unclear whether a bot will have to process more than 2 microchips.
    For example, it could be possible it has to process 5 low value chips
    and 1 high value chip. If this is possible, it is impossible to search
    each node for the values. A log needs to be kept, but only for this
    specific combination.
    """

    def __init__(self, number: int):
        """
        Initializes a bot with its number, empty value storage, and no destinations.

        Time complexity: O(1)

        :param number: Bot number
        """
        self.number = number
        self.target_for_part_1 = False

        self.high = None
        self.low = None
        self.received_values = []

        self.high_bot_destination = None
        self.low_bot_destination = None


    def set_destinations(self, low_destination: Bot, high_destination: Bot) -> None:
        """
        Assigns the destination bots for the lower and higher values.

        Time complexity: O(1)

        :param low_destination: Bot to receive low value
        :param high_destination: Bot to receive high value
        """
        self.high_bot_destination = high_destination
        self.low_bot_destination = low_destination


    def receive_value(self, value:int) -> None:
        """
        Adds a value to the bot.

        When the bot has received two values, it checks whether the values
        are the target values for part 1. It then sorts the values,
        stores the higher and lower value separately, and sends them to the configured destinations.

        Because a bot processes at most two values at a time,
        the sorting operation is performed on a constant-sized list.

        Time complexity: O(1)

        :param value: Value (int) to be added to the bot
        """
        self.received_values.append(value)

        if len(self.received_values) == 2:
            if 61 in self.received_values and 17 in self.received_values:
                self.target_for_part_1 = True

            self.received_values.sort()

            self.high = self.received_values.pop()
            self.low = self.received_values.pop()

            self._send_values()


    def get_sum(self) -> int:
        """
        Returns the sum of the values currently stored by the bot/output bins.
        Bots delete their values when they're sent. Output bins don't send their values.

        Time complexity: O(1), because a bot contains at most two values.

        :return: Sum of stored values
        """
        return sum(self.received_values)


    def _send_values(self):
        """
        Sends the higher value to the high-value destination
        and the lower value to the low-value destination.
        After sending both values, the bot resets its stored high and low values.

        Time complexity: O(1)
        """
        self.high_bot_destination.receive_value(self.high)
        self.low_bot_destination.receive_value(self.low)

        self._reset_values()


    def _reset_values(self):
        """
        Resets the stored high and low values of the bot to None.

        Time complexity: O(1)
        """
        self.high = None
        self.low = None



def load_data() -> list[str]:
    """
    Retrieves the data from the input file.

    Time complexity: O(n), where n is the number of input lines.

    :return: String of input data
    """
    with open('dataset_day_10') as file:
        return [line.strip() for line in file.readlines()]


def transform_data(raw_data: list[str]) -> tuple[dict[int, list[int]],dict[int, list[int]]]:
    """
    Parses the raw input and separates it into two dictionaries:

    Time complexity: O(n)

    :param raw_data: List with strings to be parsed and transformed into dictionaries
    :return: tuple with dictionaries, where dictionaries are keyed by bot number
    """

    # initial_value_distribution, containing the initial values assigned to bots
    initial_value_distribution = dict()
    # connections, containing the destination bots for every bot
    connections = dict()

    for row in raw_data:
        row_parts = row.split(" ")

        if row.startswith("bot"):
            bot = int(row_parts[1])
            low_bot = int(row_parts[6])
            high_bot = int(row_parts[-1])

            if row_parts[5] == 'output':
                low_bot += 10_000
            if row_parts[-2] == 'output':
                low_bot += 10_000

            if bot in connections:
                print(f'Conflicting instructions were found for bot {bot}.\nPlease check input file.')
            else:
                connections[bot] = [low_bot, high_bot]

        elif row.startswith("value"):
            bot = int(row_parts[-1])
            value = int(row_parts[1])

            if bot not in initial_value_distribution:
                initial_value_distribution[bot] = [value]
            else:
                if len(initial_value_distribution[bot]) == 2:
                    print(f'Bot {bot} has already been assigned 2 values.\nPlease check input file.')
                else:
                    initial_value_distribution[bot].append(value)

    return initial_value_distribution, connections


def solve_part_1(bot_handler) -> int|None:
    """
    Calls get_bot_for_part_1() to retrieve the number of the bot that compared the target values.

    Time complexity: O(b)

    :param bot_handler: BotHandler object
    :return: Bot number needed; solution to part 1
    """
    return bot_handler.get_bot_for_part_1()


def solve_part_2(botnet_handler: BotHandler, outputs: list[int]) -> int:
    """
    Calls get_output_values() to retrieve the values from the requested outputs and calculate their product.

    Time complexity: O(k)

    :param botnet_handler: BotHandler object
    :param outputs: Output bin numbers required for calculation
    :return: Sum of values of outputs in param outputs
    """
    return botnet_handler.get_output_values(outputs)



if __name__ == '__main__':
    data = load_data()

    value_assignment, bot_connections = transform_data(data)

    botnet_Handler = BotHandler()
    botnet_Handler.setup_botnet(bot_connections)
    botnet_Handler.process_values(value_assignment)

    result_1 = solve_part_1(botnet_Handler)
    print(f"Answer to part 1: {result_1}")

    result_2 = solve_part_2(botnet_Handler, [0, 1, 2])
    print(f"Answer to part 2: {result_2}")

