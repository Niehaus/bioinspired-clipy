import random
import math


class AntSystemAlg:
    def __init__(self, data, alpha, beta, q, evaporation_rate):
        self.pheromone = data['pheromone_matrix']
        self.dist = data['dist_matrix']
        self.city_number = data['city_number']
        self.alpha = alpha
        self.beta = beta
        self.probability = [0] * self.city_number
        self.Q = q
        self.evaporation_rate = evaporation_rate
        self.best_solution = {
            'best_fo': math.inf,
            'best_solution': [] * self.city_number
        }

    def calculate_distance(self, x):
        circuit_dist = 0
        for i in range(len(x) - 1):
            circuit_dist += self.dist[x[i]][x[i + 1]]
        circuit_dist += int(self.dist[x[len(x) - 1]][x[0]])

        return circuit_dist

    def move(self, ant):
        """ Ants use the probability function to move between cities"""
        while len(ant.trail) < self.city_number:
            last_city = ant.trail[-1]

            self.probability_of_move(ant)

            total_probability = 0
            for i in range(0, self.city_number):
                total_probability += self.probability[i]

            lucky_number = random.uniform(0, total_probability)
            selected_city = 0
            for i in range(0, self.city_number):
                selected_city += self.probability[i]
                if selected_city >= lucky_number and self.dist[last_city][i] != 0 and not ant.ant_has_visited(i):
                    ant.make_visit(i)
                    break

    def probability_of_move(self, ant):
        i = ant.trail[-1]
        pheromone = 0

        for j in range(0, self.city_number):
            if not ant.ant_has_visited(j) and self.dist[i][j] != 0:
                pheromone += pow(self.pheromone[i][j], self.alpha) * pow(1 / self.dist[i][j], self.beta)

        for j in range(0, self.city_number):
            if self.dist != 0:
                if ant.ant_has_visited(j):
                    self.probability[j] = 0
                else:
                    n = pow(self.pheromone[i][j], self.alpha) * pow(1 / self.dist[i][j], self.beta)
                    self.probability[j] = n / pheromone

    def update_pheromone(self, ant_pop):
        for i in range(0, self.city_number):
            for j in range(0, self.city_number):
                if self.dist[i][j] != 0:
                    self.pheromone[i][j] *= self.evaporation_rate

        for ant in ant_pop:
            if len(ant.trail) > 1:
                ant_contribution = self.Q / self.calculate_distance(ant.trail)
            else:
                ant_contribution = 0

            for i in range(0, len(ant.trail) - 1):
                self.pheromone[ant.trail[i]][ant.trail[i + 1]] += ant_contribution
            self.pheromone[ant.trail[-1]][ant.trail[0]] += ant_contribution

    def update_best_solution(self, candidate_solution):
        candidate_distance = self.calculate_distance(candidate_solution)
        if candidate_distance < self.best_solution['best_fo']:
            self.best_solution['best_fo'] = candidate_distance
            self.best_solution['best_solution'] = candidate_solution[:]

    def get_best_solution(self):
        return self.best_solution['best_fo'], self.best_solution['best_solution']

    def clear_pheromone_matrix(self):
        for i in range(0, self.city_number):
            self.pheromone[i] = [10 ** -16] * self.city_number


class Ant:
    def __init__(self, cities_number):
        self.trail = []
        self.cities_number = cities_number

    def ant_initial_position(self, edges_number):
        initial_city = random.randint(1, edges_number)
        self.trail.append(initial_city)

    @staticmethod
    def generate_ant_pop(ants_number):
        """ Initial position of ant set randomly """
        ant_pop = []
        for _ in range(ants_number):
            ant_pop.append(Ant(ants_number))
        return ant_pop

    def make_visit(self, city_to_visit):
        self.trail.append(city_to_visit)

    def forget_tour(self):
        self.trail = []

    def prepare_for_tour(self):
        self.forget_tour()
        self.make_visit(random.randint(0, self.cities_number - 1))

    def ant_has_visited(self, city):
        if city in self.trail:
            return True
        else:
            return False
