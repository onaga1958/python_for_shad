from scipy.stats import bernoulli
from random import shuffle


class OceanException(BaseException):
    pass


class UnexpectedCreatureIndex(OceanException):
    pass


class Creature:
    def __init__(self, speed, reprodaction_rate):
        self.speed = speed
        self.reprodaction_rate = reprodaction_rate

    def child(self):
        return Creature(self.speed, self.reprodaction_rate)

    def possible_neighbor(self, cell):
        return not (isinstance(cell.creature, Creature) or
                    isinstance(cell.newcomer, Creature))

    def move(self, neighbors):
        potential_locations = [cell for cell in neighbors 
                               if self.possible_neighbor(cell)]
        shuffle(potential_locations)
        p = self.speed[len(potential_locations)]
 
        for location in potential_locations:
            if bernoulli.rvs(p):
                return location
        return None

    def reproduction(self, neighbors):
        potential_locations = [cell for cell in neighbors 
                               if (cell.creature is None and
                                   cell.newcomer is None)]
        shuffle(potential_locations)
        p = self.reprodaction_rate[len(potential_locations)]
 
        for location in potential_locations:
            if bernoulli.rvs(p):
                return [self.child(), location]
        return [None, None]


class Obstacle:
    pass


class Predator(Creature):
    def __init__(self, speed, reprodaction_rate, stamina):
        super(Predator, self).__init__(speed, reprodaction_rate)
        self.stamina = stamina
        self.max_stamina = stamina

    def child(self):
        child = Predator(self.speed, self.reprodaction_rate, self.max_stamina) 
        child.stamina += 1
        return child

    def possible_neighbor(self, cell):
        return not (isinstance(cell.creature, Predator) or
                    isinstance(cell.newcomer, Predator))
        

def get_creature(creature_index, params):
    if creature_index == 0:
        return None
    if creature_index == 1:
        return Predator(params[0], params[2], params[4])
    if creature_index == 2:
        return Creature(params[1], params[3])
    if creature_index == 3:
        return Obstacle()

    raise UnexpectedCreatureIndex()

def creature_index(creature):
    if creature is None:
        return 0
    if isinstance(creature, Predator):
        return 1
    else:
        if isinstance(creature, Creature):
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

class Ocean:
    class Cell:
        def __init__(self):
            self.newcomer = None

        def start_turn(self):
            """
            Creature can do only one action at one turn: move or reproduce.

            Firstly he tries to move. If didn't succeed - tries to reproduce.
            """
            if self.creature is not None:
                new_cell = self.creature.move(self.neighbors)
                if new_cell is not None:
                    if isinstance(new_cell.newcomer, Creature):
                        self.creature.stamina = self.creature.max_stamina + 1
                    new_cell.newcomer = self.creature
                    self.creature = None
                else:
                    new_creature, new_cell = self.creature.reproduction(self.neighbors)
                    if new_creature is not None:
                        new_cell.newcomer = new_creature

        def end_turn(self):
            # newcomer and creature can be both noNone only in one case:
            # if newcomer is a Predator and creature is a simple Creature
            if isinstance(self.newcomer, Predator):
                if isinstance(self.creature, Creature):
                    self.newcomer.stamina = self.newcomer.max_stamina + 1

            if isinstance(self.newcomer, Creature):
                self.creature = self.newcomer
                self.newcomer = None

            if isinstance(self.creature, Predator):
                self.creature.stamina -= 1
                if self.creature.stamina == 0:
                    self.creature = None
                    

    def __init__(self, start_table, params):
        """
        params: predator_speed, victim_speed, predator_reprodaction_rate,

        victim_reprodaction_rate, predator_stamina
        """
        self.params = list(map(probability_array, params[:-1])) + [params[-1]]
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

    def make_turn(self):
        """
        Returns True is there are no victims or there are no predators

        in the ocean. If there are both types in the ocean returns None.
        """
        for line in self.table:
            for cell in line:
                if not isinstance(cell.creature, Obstacle):
                    cell.start_turn()

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
        params = list(map(float, params[:-1])) + [int(params[-1])]
        table = [list(map(int, line.strip().split())) for line in param_file]

    ocean = Ocean(table, params)
    return ocean

if __name__ == '__main__':
    ocean = init_ocean("ocean_params.txt")
    for i in range(5):
        print(ocean)
        if ocean.make_turn():
            break
    print(ocean)
