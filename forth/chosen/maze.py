#!/usr/bin/env python3

import argparse
import random
import string
import numpy
import queue


TRUE_DICT = {'can_move': True}


class Cell:
    def can_move(self, direction, game, player):
        return TRUE_DICT

    def __str__(self):
        return '.'

    def arrive(self, game, player):
        pass


class Exit(Cell):
    def __init__(self, direction):
        self.direction = direction

    def can_move(self, direction, game, player):
        if direction[0] == self.direction:
            raise GameEnd()
        else:
            return TRUE_DICT

    def __str__(self):
        return self.direction


class Stun(Cell):
    def __init__(self, duration=5):
        self.duration = duration
        self.stunned_players = {}

    def arrive(self, game, player):
        super().arrive(game, player)
        self.stunned_players[player.name] = game.turn

    def can_move(self, direction, game, player):
        stun_start = self.stunned_players.get(player.name, -self.duration)
        if game.turn > stun_start + self.duration:
            return TRUE_DICT
        else:
            return {'can_move': False, 'message': STUNNED}

    def __str__(self):
        return 'S'


def make_cell_keys():
    result = {direction: Exit(direction)
              for direction in [d[0] for d in DIRECTIONS.keys()]}
    result['S'] = Stun()
    result['.'] = Cell()
    return result


def make_parser():
    result = argparse.ArgumentParser()
    subparsers = result.add_subparsers(dest='command')
    for direction in DIRECTIONS.keys():
        subparsers.add_parser(direction)
    return result


DIRECTIONS = {'up': (-1, 0), 'right': (0, 1), 'left': (0, -1), 'down': (1, 0)}
INVERSED_DIRECTIONS = {value: key for key, value in DIRECTIONS.items()}
CELL_KEYS = make_cell_keys()
PARSER = make_parser()
MOVE_SUCCESS = "You moved."
WALL = "You can't move, there is a wall."
STUNNED = "You stunned."


class MazeException(Exception):
    def __str__(self):
        return "MazeException: " + self.describtion


class GameEnd(Exception):
    pass


class IncorrectInputFileError(MazeException):
    def __init__(self, name):
        self.describtion = "IncorrectInputFile: " + name


class DifficultParamsError(MazeException):
    def __init__(self, **kwargs):
        self.describtion = "Fail to generate correct field with params: "
        self.describtion += str(kwargs)


class NoExitError(MazeException):
    def __init__(self, player):
        self.describtion = "There are no available exits for player "
        self.describtion += player.name


class Game:
    def __init__(self, field_file, random_bots_number, smart_bots_number,
                 alive_players_number, silent=True):
        self.silent = alive_players_number == 0 and silent
        self.field = Field(field_file)
        self.players = []
        for i in range(alive_players_number):
            print("Enter {} player name: ".format(i + 1), end='')
            self.players.append(AlivePlayer(input().split('\n')[0]))

        self.players += [SmartBot(self.silent)
                         for _ in range(smart_bots_number)]
        self.players += [RandomBot(self.silent)
                         for _ in range(random_bots_number)]
        random.shuffle(self.players)
        self.turn = 1

    def game_print(self, *args, **kwargs):
        if not self.silent:
            print(*args, **kwargs)

    def inform(self, active, message):
        for player in self.players:
            player.finish_turn(active, message)

    def move(self, player, direction):
        old_position = self.positions[player.name]
        can_move = self.field.can_move(old_position, direction, self, player)
        if can_move['can_move']:
            new_position = get_new_position(old_position, direction)
            self.positions[player.name] = new_position
            self.field[self.positions[player.name]].arrive(self, player)
        self.inform(player, can_move['message'])

    def execute_correct_command(self, command, player):
        """
        Will execute command and return True if command is correct.

        Overwise returns False.
        """
        try:
            args = PARSER.parse_args(command.split())
        except SystemExit:
            return False

        if args.command in DIRECTIONS.keys():
            self.move(player, command)
            return True

    def choose_start(self):
        size = self.field.size - 1
        self.game_print("All player should choose their start positions.\n" +
                        "You should type two numbers from " +
                        "[0, {}]".format(size) +
                        " to set this position like this: '0 0'.")
        self.positions = {player.name: player.choose_start(self.field.size)
                          for player in self.players}

    def make_turn(self):
        self.game_print("Begin turn {}.".format(self.turn))

        for player in self.players:
            self.game_print(player.name + " turn.")
            try:
                player.turn(self)
            except GameEnd as error:
                self.game_print("Player " + player.name + " win!")
                self.winner = player
                raise error

        self.turn += 1

    def print_rules(self):
        rules = ("\nHello, everybody! You are in the Maze!\n" +
                 "Maze has size {}x{}.\n".format(self.field.size,
                                                 self.field.size) +
                 "Rules are pretty simple.\n" +
                 "Your goal is to get out of here.\n" +
                 "There are exits (at least one) somewhere in Maze.\n" +
                 "No one knows where exactly are they, but they should be " +
                 "somewhere in walls, which surround the Maze.\n" +
                 "If you move in right direction from exit cell you'll " +
                 "win!\n" +
                 "Type " + ", ".join(DIRECTIONS.keys()) + " to move in " +
                 "respective way.\nGood luck!\n")
        self.game_print(rules)

    def play_game(self, turn_limit=None):
        """
        Process game. If turn_limit is None game ends only if someone wins.

        Returns winner; if time is out returns None.
        """
        self.print_rules()
        self.choose_start()
        self.game_print("\nAnd the game begins!\n")
        try:
            while turn_limit is None or self.turn <= turn_limit:
                self.make_turn()
            self.game_print("Game over! Time out.")
        except GameEnd:
            return self.winner


class Field:
    def __init__(self, file_name=None, size=None):
        """
        If file_name is not None create Field using it.

        Overwise makes empty Field with specified size.
        """
        if file_name is None:
            if size is None:
                raise ValueError("Both file_name and size can't be None")
            self.size = size
            self._set_default_field()
        else:
            try:
                with open(file_name) as file:
                    self.size = int(file.readline())
                    self._set_default_field()

                    for i in range(self.size):
                        line = file.readline()
                        for j in range(self.size):
                            self.field[i][j] = CELL_KEYS[line[2 * j]]
                            if j != self.size - 1:
                                wall = line[2*j + 1] == "|"
                                self.vertical_walls[i][j] = wall

                        if i != self.size - 1:
                            line = file.readline()
                            for j in range(self.size):
                                wall = line[2 * j] == "-"
                                self.horizontal_walls[i][j] = wall
            except (ValueError, LookupError, FileNotFoundError):
                raise IncorrectInputFileError(file_name)

    def _set_default_field(self):
        self.field = [[Cell() for j in range(self.size)]
                      for i in range(self.size)]
        self.horizontal_walls = [[False for i in range(self.size)]
                                 for j in range(self.size - 1)]
        self.vertical_walls = [[False for i in range(self.size - 1)]
                               for j in range(self.size)]

    def __getitem__(self, position):
        return self.field[position[0]][position[1]]

    def __setitem__(self, position, value):
        self.field[position[0]][position[1]] = value

    def can_move(self, position, direction, game=None, player=None):
        if game is None:
            result = TRUE_DICT
        else:
            result = self[position].can_move(direction, game, player)

        if result['can_move']:
            if check_valid(self.size, position, direction):
                if DIRECTIONS[direction][1]:
                    new_cord = position[1] + min(DIRECTIONS[direction][1], 0)
                    wall = self.vertical_walls[position[0]][new_cord]
                else:
                    new_cord = position[0] + min(DIRECTIONS[direction][0], 0)
                    wall = self.horizontal_walls[new_cord][position[1]]
            else:
                wall = True
            result = {'message': WALL if wall else MOVE_SUCCESS,
                      'can_move': not wall}
        return result

    def __str__(self):
        result = ""
        for i, (hw, line) in enumerate(zip(self.horizontal_walls + [[[]]],
                                           self.field)):
            for wall, cell in zip(self.vertical_walls[i] + [[]], line):
                result += str(cell)
                result += '|' if wall else ' '
            result += '\n'
            result += '+'.join(['-' if wall else ' ' for wall in hw])
            result += '\n'
        return result


class RandomPriorityQueue(queue.PriorityQueue):
    """
    This class is implementation of priority queue in which

    elements with the same priority are erased in random order.

    Means that inserted elements are pairs (priority, value).
    """
    # Need it in this task to make SmartBot more independent from map
    def __init__(self):
        super().__init__()
        self.values = {}

    def put(self, element):
        try:
            priority, value = element
        except (ValueError, TypeError):
            raise ValueError('Incorrect elemnet for RandomPriorityQueue.' +
                             ' Expect pair (priority, value)') from None

        random_key = random.random()
        self.values[random_key] = value
        super().put((priority, random_key), False)

    def get(self):
        priority, random_key = super().get(False)
        value = self.values.pop(random_key)
        return priority, value


def get_position():
    try:
        return list(map(int, input().split()))
    except ValueError:
        return (-1, -1)


def get_new_position(position, direction):
    return tuple(pos + add
                 for pos, add in zip(position, DIRECTIONS[direction]))


def get_move_direction(position, previous_position):
    direction = tuple(pos - previous_pos
                      for pos, previous_pos
                      in zip(position, previous_position))
    return INVERSED_DIRECTIONS[direction]


def in_range(num, begin, end=None):
    """
    Return True if num is laying in [begin, end), overwise return False.

    If end is not stated end = begin, begin = 0.
    """
    if end is None:
        end = begin
        begin = 0

    return begin <= num and num < end


def check_valid(size, position, direction=None):
    if len(position) != 2:
        return False

    if direction is not None:
        position = get_new_position(position, direction)
    return in_range(position[0], size) and in_range(position[1], size)


def build_route(node, nodes):
    path = [node]
    while nodes[path[-1]]['ancestor'] is not None:
        path.append(nodes[path[-1]]['ancestor'])
    path = list(reversed(path))
    return [get_move_direction(node, previous_node)
            for node, previous_node in zip(path[1:], path)]


def set_walls(horizontal_walls, vertical_walls, position, direction):
    if DIRECTIONS[direction][1]:
        new_cord = position[1] + min(DIRECTIONS[direction][1], 0)
        vertical_walls[position[0]][new_cord] = True
    else:
        new_cord = position[0] + min(DIRECTIONS[direction][0], 0)
        horizontal_walls[new_cord][position[1]] = True


def multinomial_rvs(probs_dict):
    """
    Generate value from keys with probabilities given in values.

    If values in None(default) generate from range(len(probabilities))
    """
    stop_value = random.random()
    moving_sum = 0
    for value, prob in probs_dict.items():
        moving_sum += prob
        if moving_sum >= stop_value:
            return value


def choice(array, number):
    # just because np.choice can't deal with not 1-dim data
    encode_dict = {random.random(): element for element in array}
    codes = numpy.random.choice(list(encode_dict.keys()), number, False)
    return [encode_dict[code] for code in codes]


def get_potential_exits(size):
    return {(i, j): [d for d in DIRECTIONS.keys()
                     if not check_valid(size, (i, j), d)]
            for i in range(size) for j in range(size)
            if i == 0 or i == size - 1 or
            j == 0 or j == size - 1}


class Player:
    def __init__(self, name):
        self.name = name


class AlivePlayer(Player):
    def choose_start(self, size):
        print(self.name + " choose your position: ", end='')
        start = get_position()
        while not check_valid(size, start):
            print("Incorrect position! It should be like this 'a b'.\n" +
                  "a and b should be integers in [0, {}].".format(size - 1))
            print(self.name + " choose your position: ", end='')
            start = get_position()

        self.start = start
        return start

    def turn(self, game):
        while not game.execute_correct_command(input(), self):
            pass

    def finish_turn(self, active, message):
        if self == active:
            print(message)


class Bot(Player):
    def __init__(self, silent, name=None):
        if name is None:
            letters = random.sample(string.ascii_lowercase, 5)
            name = "".join(letters).capitalize()
        self.name = name
        self.silent = silent

    def choose_start(self):
        if not self.silent:
            print(self.name + " chose.")

    def finish_turn(self, active, message):
        if not self.silent and self == active:
            print(message)


class RandomBot(Bot):
    def __init__(self, silent, name=None):
        super().__init__(silent, name)
        self.possible_commands = list(DIRECTIONS.keys())

    def choose_start(self, size):
        self.start = [random.randint(0, size - 1) for i in range(2)]
        super().choose_start()
        return self.start

    def turn(self, game):
        game.execute_correct_command(random.choice(self.possible_commands),
                                     self)


class SmartBot(Bot):
    def __init__(self, silent, name=None):
        super().__init__(silent, name)
        self.route = []

    def choose_start(self, size):
        self.maze_size = size
        self.potential_exits = get_potential_exits(size)
        self.start = random.choice(list(self.potential_exits.keys()))
        self.position = self.start
        self.field = Field(size=size)
        super().choose_start()
        return self.start

    def get_route(self, start_node):
        nodes = {(i, j): None for i in range(self.maze_size)
                 for j in range(self.maze_size)}
        priority_queue = RandomPriorityQueue()
        priority_queue.put((0, start_node))
        nodes[start_node] = {'distance': 0, 'ancestor': None}

        while not priority_queue.empty():
            cur_node = priority_queue.get()[1]
            if self.potential_exits.get(cur_node) is not None:
                return build_route(cur_node, nodes)
            else:
                for direction in DIRECTIONS.keys():
                    new_pos = get_new_position(cur_node, direction)
                    if (self.field.can_move(cur_node, direction)['can_move']):
                        if isinstance(self.field[new_pos], Stun):
                            edge = self.field[new_pos].duration + 1
                        else:
                            edge = 1
                        new_distance = nodes[cur_node]['distance'] + edge
                        if (nodes[new_pos] is None or
                                nodes[new_pos]['distance'] > new_distance):
                            nodes[new_pos] = {'distance': new_distance,
                                              'ancestor': cur_node}
                            priority_queue.put((new_distance, new_pos))
        raise NoExitError(self)

    def turn(self, game):
        if len(self.route) == 0:
            if self.potential_exits.get(self.position) is not None:
                self.try_to_exit(game)
                return
            self.route = self.get_route(self.position)
        self.direction = self.route.pop(0)
        game.execute_correct_command(self.direction, self)

    def finish_turn(self, active, message):
        if active == self:
            if message == STUNNED:
                if not check_valid(self.maze_size, self.position,
                                   self.direction):
                    self.potential_exits[self.position].append(self.direction)
                else:
                    self.route.insert(0, self.direction)
                if self.sudden_stun:
                    self.field[self.position].duration += 1
                if isinstance(self.field[self.position], Cell):
                    self.field[self.position] = Stun(1)
                    self.sudden_stun = True
            else:
                self.sudden_stun = False

            if message == WALL:
                if check_valid(self.maze_size, self.position, self.direction):
                    self.route = []
                    set_walls(self.field.horizontal_walls,
                              self.field.vertical_walls,
                              self.position, self.direction)
                else:
                    if len(self.potential_exits[self.position]) == 0:
                        self.potential_exits.pop(self.position)

            if message == MOVE_SUCCESS:
                self.position = get_new_position(self.position, self.direction)
            self.direction = None

        super().finish_turn(active, message)

    def try_to_exit(self, game):
        self.direction = self.potential_exits[self.position].pop()
        game.execute_correct_command(self.direction, self)


def normalize_probabilities_dict(probabilities_dict):
    summary = sum(probabilities_dict.values())
    for key in probabilities_dict.keys():
        probabilities_dict[key] /= summary


def check_field(file_name):
    """
    Verifies the connectivity of the Maze by BFS.
    """
    field = Field(file_name)
    nodes = {(i, j): True for i in range(field.size)
             for j in range(field.size)}
    queue = [(0, 0)]
    nodes[(0, 0)] = False

    while len(queue) != 0:
        cur_node = queue.pop(0)
        for direction in DIRECTIONS.keys():
            new_node = get_new_position(cur_node, direction)
            if (check_valid(field.size, cur_node, direction) and
                    nodes[new_node] and
                    field.can_move(cur_node, direction)['can_move']):
                nodes[new_node] = False
                queue.append(new_node)

    for node in nodes.values():
        if node:
            return False
    return True


def print_wall(file, wall_symbol, wall_prob):
    wall = random.random() < wall_prob
    print(file=file, end=wall_symbol if wall else ' ')


def generate_field(file_name, size, wall_probability, cell_probabilities,
                   exits_number=1):
    normalize_probabilities_dict(cell_probabilities)

    potential_exits = get_potential_exits(size)
    exits = choice(potential_exits.keys(), exits_number)
    exits = {(i, j): random.choice(potential_exits[(i, j)])[0]
             for i, j in exits}

    with open(file_name, 'w') as file:
        print(size, file=file)
        for line in range(size):
            for column in range(size):
                if (line, column) in exits.keys():
                    print(exits[(line, column)], file=file, end='')
                else:
                    print(multinomial_rvs(cell_probabilities),
                          file=file, end='')
                if column != size - 1:
                    print_wall(file, '|', wall_probability)
            print(file=file)
            if line != size - 1:
                for column in range(size):
                    print_wall(file, '-', wall_probability)
                    if column != size - 1:
                        print(file=file, end=' ')
                print(file=file)


def generate_correct_field(tries_nubmer, **kwargs):
    for i in range(tries_nubmer):
        generate_field(**kwargs)
        if check_field(kwargs['file_name']):
            return
    raise DifficultParamsError(**kwargs)


def main():
    games_number = 1
    players = {'random_bots_number': 1,
               'smart_bots_number': 0,
               'alive_players_number': 1}
    field_name = 'field2.txt'
    field_args = {'file_name': field_name,
                  'size': 10,
                  'wall_probability': 0.3,
                  'cell_probabilities': {'.': 0.9, 'S': 0.1},
                  'exits_number': 2}

    smart_wins = 0
    for i in range(games_number):
    #    generate_correct_field(100, **field_args)
        game = Game(field_name, **players)
        if isinstance(game.play_game(), SmartBot):
            smart_wins += 1
    print("Smart won " + str(smart_wins) + "/" + str(games_number))


if __name__ == "__main__":
    main()
