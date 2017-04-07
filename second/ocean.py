import random


creature_marks = {'None': '.', 'Victim': 'v', 'Predator': 'p', 'Obstacle': 'X'}


class OceanException(BaseException):
    def __str__(self):
        return self.descr


class UnexpectedCreatureMark(OceanException):
    def __init__(self, mark):
        marks = "Valid types: " + ", ".join(creature_marks.values()) + "."
        self.descr = marks + " Got {}".format(mark)


class UnexpectedCreatureType(OceanException):
    def __init__(self, creature):
        types = "Valid types: " + ", ".join(creature_marks.keys()) + "."
        self.descr = types + " Got {}".format(type(creature))


class Creature:
    def move(self, neighbors, starting_location):
        return False

    def eat(self, neighbors):
        return False

    def reduce_stamina(self):
        return False


class AliveCreature(Creature):
    def __init__(self, speed):
        self.speed = speed

    def move(self, neighbors, starting_location):
        potential_locations = [cell for cell in neighbors
                               if cell.creature is None and
                               cell.newcomer is None]
        random.shuffle(potential_locations)
        probability = self.speed[len(potential_locations)]

        for location in potential_locations:
            if bernoulli_rvs(probability):
                location.newcomer = self
                starting_location.creature = None
                return True
        return False

    def reproduction(self, neighbors):
        potential_locations = [cell for cell in neighbors
                               if cell.creature is None and
                               cell.newcomer is None]
        if len(potential_locations) > 0:
            random.choice(potential_locations).newcomer = self.child()


class Victim(AliveCreature):
    def child(self):
        return Victim(self.speed)


class Obstacle(Creature):
    pass


class Predator(AliveCreature):
    def __init__(self, speed, eat_rate, stamina):
        super(Predator, self).__init__(speed)
        self.stamina = stamina
        self.max_stamina = stamina
        self.eat_rate = eat_rate

    def child(self):
        child = Predator(self.speed, self.eat_rate, self.max_stamina)
        child.stamina += 1
        return child

    def eat(self, neighbors):
        potential_targets = [cell for cell in neighbors
                             if has_victim(cell)]
        random.shuffle(potential_targets)
        probability = self.eat_rate[len(potential_targets)]

        for cell in potential_targets:
            if bernoulli_rvs(probability):
                if cell.creature is None:
                    cell.newcomer = None
                else:
                    cell.creature = None
                self.stamina = self.max_stamina + 1
                return True
        return False

    def reduce_stamina(self):
        self.stamina -= 1
        return self.stamina == 0


def has_victim(cell):
    return (isinstance(cell.creature, Victim) or
            isinstance(cell.newcomer, Victim))


def get_creature(mark, params):
    if mark == creature_marks['None']:
        return None
    if mark == creature_marks['Predator']:
        return Predator(**params['predator params'])
    if mark == creature_marks['Victim']:
        return Victim(**params['victim params'])
    if mark == creature_marks['Obstacle']:
        return Obstacle()

    raise UnexpectedCreatureMark(mark)


def get_creature_mark(creature):
    if creature is None:
        return creature_marks['None']
    if isinstance(creature, Predator):
        return creature_marks['Predator']
    if isinstance(creature, Victim):
        return creature_marks['Victim']
    if isinstance(creature, Obstacle):
        return creature_marks['Obstacle']

    raise UnexpectedCreatureType(creature)


def probability_array(p_0):
    return [0] + [probability(p_0, n) for n in range(1, 5)]


def probability(p_0, n):
    """
    There are n locations. Want to move/reproduce with probability p_0.
    This function calculates required probabily of action in one location.
    """
    return 1 - (1 - p_0)**(1 / n)


def bernoulli_rvs(p):
    return True if random.random() < p else False


class Cell:
    def __init__(self):
        self.newcomer = None

    def start_turn(self):
        """
        Creature can do only one action at one turn: eat or move.
        Only Predators can eat, of course.
        Firstly he tries to eat. If didn't succeed - tries to move.
        """
        if self.creature is not None:
            if not self.creature.eat(self.neighbors):
                self.creature.move(self.neighbors, self)

    def end_turn(self):
        if self.creature is not None:
            if self.creature.reduce_stamina():
                self.creature = None


class Ocean:
    def __init__(self, start_table, params):
        """
        params: predator_speed, victim_speed, eat_rate,
        predator_reproduction_period, victim_reproduction_period,
        predator_stamina
        """

        creature_params = self.get_creature_params(params)
        self.reproduction_periods = params[-2:]
        self.turns_till_reproduction = params[-2:]
        x_lim = len(start_table[0])
        y_lim = len(start_table)
        self.table = [[Cell() for i in range(x_lim)]
                      for i in range(y_lim)]

        for start_line, line in zip(start_table, self.table):
            for mark, cell in zip(start_line, line):
                cell.creature = get_creature(mark, creature_params)

        for i in range(y_lim):
            for j in range(x_lim):
                potential_neighbors = [self.table[(i + 1) % y_lim][j],
                                       self.table[(i - 1) % y_lim][j],
                                       self.table[i][(j + 1) % x_lim],
                                       self.table[i][(j - 1) % x_lim]]
                self.table[i][j].neighbors = []
                for potential_neighbor in potential_neighbors:
                    if not isinstance(potential_neighbor.creature, Obstacle):
                        self.table[i][j].neighbors.append(potential_neighbor)

    @staticmethod
    def get_creature_params(raw_params):
        eat_rate = probability_array(raw_params[2])
        return {'victim params': {'speed': probability_array(raw_params[1])},
                'predator params': {'speed': probability_array(raw_params[0]),
                                    'eat_rate': eat_rate,
                                    'stamina': raw_params[3]}}

    def end_phase(self):
        for line in self.table:
            for cell in line:
                if cell.newcomer is not None:
                    cell.creature = cell.newcomer
                    cell.newcomer = None

    def make_turn(self):
        """
        Returns True is there are no victims or there are no predators
        in the ocean. If there are both types in the ocean returns None.
        """
        for line in self.table:
            for cell in line:
                cell.start_turn()
        self.end_phase()

        creature_type = [Predator, Victim]
        for i, period_len in enumerate(self.reproduction_periods):
            self.turns_till_reproduction[i] -= 1
            if self.turns_till_reproduction[i] == 0:
                self.turns_till_reproduction[i] = period_len
                for line in self.table:
                    for cell in line:
                        if isinstance(cell.creature, creature_type[i]):
                            cell.creature.reproduction(cell.neighbors)
                self.end_phase()

        for line in self.table:
            for cell in line:
                cell.end_turn()

        if self.creatures_counter():
            return True

    def creatures_counter(self, needstat=False):
        """
        If needstat is False this function checks do the ocean has both
        victims and predators. If not returns True, otherwise returns
        False.
        If needstat is True this function returns number of predators
        and victims in the ocean.
        """
        predators_cnt = 0
        victims_cnt = 0
        for line in self.table:
            for cell in line:
                if isinstance(cell.creature, Predator):
                    predators_cnt += 1
                else:
                    if isinstance(cell.creature, Victim):
                        victims_cnt += 1
                if (not needstat) and victims_cnt and predators_cnt:
                    return False
        if needstat:
            return [predators_cnt, victims_cnt]
        else:
            return True

    def __str__(self):
        result = ""
        for line in self.table:
            for cell in line:
                result += str(get_creature_mark(cell.creature)) + " "
            result += "\n"
        return result

    @staticmethod
    def print_legend():
        print('legend:')
        marks = ['.', 'v', 'p', 'X']
        describtions = ['empty cell', 'victim', 'predator', 'obstacle']
        for mark, describtion in zip(marks, describtions):
            print("{} - {}".format(mark, describtion))
        print()


def init_ocean(file_name):
    with open(file_name) as param_file:
        params = param_file.readline().strip().split()
        params = list(map(float, params[:-3])) + list(map(int, params[-3:]))
        table = [list(map(int, line.strip().split())) for line in param_file]

    ocean = Ocean(table, params)
    return ocean

if __name__ == '__main__':
    params = [0.7, 0.5, 0.6, 4, 5, 6]
    table = [['.', '.', 'v', '.'],
             ['p', '.', '.', 'X'],
             ['p', 'X', '.', 'v'],
             ['X', 'v', '.', '.']]
    ocean = Ocean(table, params)
    Ocean.print_legend()

    for i in range(20):
        print(ocean)
        if ocean.make_turn():
            break
print(ocean)
