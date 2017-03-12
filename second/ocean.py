import random


class OceanException(BaseException):
    pass


class UnexpectedCreatureIndex(OceanException):
    pass


class Creature:
    def __init__(self, speed):
        self.speed = speed

    def move(self, neighbors):
        potential_locations = [cell for cell in neighbors
                               if cell.creature is None and
                               cell.newcomer is None]
        random.shuffle(potential_locations)
        probability = self.speed[len(potential_locations)]

        for location in potential_locations:
            if bernoulli_rvs(probability):
                return location
        return None

    def reproduction(self, neighbors):
        potential_locations = [cell for cell in neighbors
                               if cell.creature is None and
                               cell.newcomer is None]
        if len(potential_locations) > 0:
            random.choice(potential_locations).newcomer = self.child()


class Victim(Creature):
    def child(self):
        return Victim(self.speed)


class Obstacle:
    pass


class Predator(Creature):
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
                             if has_simple_creature(cell)]
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


def has_simple_creature(cell):
    return (isinstance(cell.creature, Victim) or
            isinstance(cell.newcomer, Victim))


def get_creature(creature_index, params):
    if creature_index == 0:
        return None
    if creature_index == 1:
        return Predator(params[0], params[2], params[4])
    if creature_index == 2:
        return Victim(params[1])
    if creature_index == 3:
        return Obstacle()

    raise UnexpectedCreatureIndex()


def creature_index(creature):
    if creature is None:
        return 0
    if isinstance(creature, Predator):
        return 1
    if isinstance(creature, Victim):
        return 2
    return 3


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


class Ocean:
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
                if isinstance(self.creature, Predator):
                    if self.creature.eat(self.neighbors):
                        return None

                new_cell = self.creature.move(self.neighbors)
                if new_cell is not None:
                    new_cell.newcomer = self.creature
                    self.creature = None

        def end_turn(self):
            if isinstance(self.creature, Predator):
                self.creature.stamina -= 1
                if self.creature.stamina == 0:
                    self.creature = None

    def __init__(self, start_table, params):
        """
        params: predator_speed, victim_speed, eat_rate,

        predator_reproduction_period, victim_reproduction_period,

        predator_stamina
        """
        self.params = list(map(probability_array, params[:3])) + params[3:]
        self.turns_till_reproduction = params[-3:-1]
        x_lim = len(start_table[0])
        y_lim = len(start_table)
        self.table = [[Ocean.Cell() for i in range(x_lim)]
                      for i in range(y_lim)]

        for start_line, line in zip(start_table, self.table):
            for creature_index, cell in zip(start_line, line):
                cell.creature = get_creature(creature_index, self.params)

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
                if not isinstance(cell.creature, Obstacle):
                    cell.start_turn()
        self.end_phase()

        params = self.params[-3:-1]
        creature_type = [Predator, Victim]
        for i in range(len(self.turns_till_reproduction)):
            self.turns_till_reproduction[i] -= 1
            if self.turns_till_reproduction[i] == 0:
                self.turns_till_reproduction[i] = params[i]
                for line in self.table:
                    for cell in line:
                        if isinstance(cell.creature, creature_type[i]):
                            cell.creature.reproduction(cell.neighbors)
                self.end_phase()

        for line in self.table:
            for cell in line:
                if not isinstance(cell.creature, Obstacle):
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
                    if isinstance(cell.creature, Creature):
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
                result += str(creature_index(cell.creature)) + " "
            result += "\n"
        return result


def init_ocean(file_name):
    with open(file_name) as param_file:
        params = param_file.readline().strip().split()
        params = list(map(float, params[:-3])) + list(map(int, params[-3:]))
        table = [list(map(int, line.strip().split())) for line in param_file]

    ocean = Ocean(table, params)
    return ocean

if __name__ == '__main__':
    params = [0.7, 0.5, 0.6, 8, 5, 6]
    table = [[0, 0, 1, 0], [2, 0, 0, 3], [2, 3, 0, 1], [3, 2, 0, 0]]
    ocean = Ocean(table, params)
    for i in range(20):
        print(ocean)
        if ocean.make_turn():
            break
    print(ocean)
