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


Possible improvements
    Checking for the 2 values to find te solution to part 1 is now hard coded in Bot.recieve_value().
    This makes the algorithm tailored to my puzzle. Adjusting the algorithm to include
    the number as search parameters instead of hard code values, is (highly) needed.

    Previous version only used bots, no outputs. Outputs needed to be included but
    that would require including extra code for processing, or an additional dictionary.
    Current version still makes a bot for the output (functionality for outputs is mostly the same as bots),
    but adds 10_000 to its number. No bot has a number above 10_000,
    so there should not be an issue with the current input data.

    Bots don't really need their own number, because the label in BotnetHandler.botnet
    already has it.
"""


class BotHandler:

    def __init__(self):
        self.botnet = dict()


    def setup_botnet(self, botnet_connections):
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


    def process_values(self, value_assignments):
        for assignment in value_assignments:
            bot = assignment
            value = value_assignments[assignment]

            if bot not in self.botnet:
                self._create_bot(bot)
            bot = self.botnet[bot]

            for v in value:
                bot.receive_value(v)


    def _create_bot(self, bot_number):
        self.botnet[bot_number] = Bot(bot_number)


    def get_bot_for_part_1(self):
        for bot in self.botnet:
            if self.botnet[bot].target_for_part_1:
                return self.botnet[bot].number

        return None


    def get_output_values(self, output_list) -> int:
        value = 1
        for number in output_list:
            value *= self.botnet[number + 10_000].get_sum()

        return value


"""
    Bots will hold a value to indicate if they had to process 17 and 61.
    It is unclear whether a bot will have to process more than 2 microchips.
    For example, it could be possible it has to process 5 low value chips
    and 1 high value chip. If this is possible, it is impossible to search
    each node for the values. A log needs to be kept, but only for this
    specific combination.
"""
class Bot:

    def __init__(self, number):
        self.number = number
        self.target_for_part_1 = False

        self.high = None
        self.low = None
        self.received_values = []

        self.high_bot_destination = None
        self.low_bot_destination = None


    def set_destinations(self, low_destination, high_destination):
        self.high_bot_destination = high_destination
        self.low_bot_destination = low_destination


    def receive_value(self, value:int):
        self.received_values.append(value)

        if len(self.received_values) == 2:
            if 61 in self.received_values and 17 in self.received_values:
                self.target_for_part_1 = True

            self.received_values.sort()

            self.high = self.received_values.pop()
            self.low = self.received_values.pop()

            self._send_values()


    def get_sum(self):
        return sum(self.received_values)


    def _send_values(self):
        self.high_bot_destination.receive_value(self.high)
        self.low_bot_destination.receive_value(self.low)

        self._reset_values()


    def _reset_values(self):
        self.high = None
        self.low = None



def load_data():
    """
    Retrieves the data from the input file.
    :return: String of input data
    """
    with open('dataset_day_10') as file:
        return [line.strip() for line in file.readlines()]


def transform_data(raw_data):
    initial_value_distribution = dict()
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
    return bot_handler.get_bot_for_part_1()


def solve_part_2(botnet_handler, outputs) -> int:
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

