
from ..colonia_formigas.ant_alg import AntSystemAlg, Ant
from rich import print
from rich.panel import Panel

def read_file(filepath):
    global data

    data = {'dist_matrix': {}, 'pheromone_matrix': {}, 'city_number': 0}

    with open(filepath, 'r') as dist_matrix_file:
        for i, line in enumerate(dist_matrix_file, start=0):
            data['dist_matrix'][i] = list(map(int, line.split()))
            data['pheromone_matrix'][i] = [10 ** -16] * len(line.split())
        data['city_number'] = len(data['dist_matrix'])


global data


class AntColony:
    @staticmethod
    def nice_print(num_cidades, optimum, solution):
        print(
            Panel.fit(
                f"Número de Cidades: [bold red]{num_cidades}[/bold red]"
                f" \nValor da Solução: [bold green]{optimum}[/bold green]"
                f" \nCaminho: {solution}",
                title="[bold magenta]Resultados do Ant Colony[/bold magenta]",
                border_style='magenta'
            )
        )

    @staticmethod
    def run():
        read_file('./algoritmos/colonia_formigas/wg22_dist.txt')

        params = {
            'data': data,
            'alpha': 1,
            'beta': 5,
            'q': 100,
            'evaporation_rate': 0.05
        }

        iter_max = 10
        iteration = 0
        ant_system = AntSystemAlg(**params)

        ant_pop = Ant.generate_ant_pop(data['city_number'])
        while iteration < iter_max:
            for ant in ant_pop:
                ant.prepare_for_tour()
                ant_system.move(ant)
                ant_system.update_best_solution(ant.trail)
            ant_system.update_pheromone(ant_pop)
            iteration += 1
        ant_system.clear_pheromone_matrix()
        optimum, solution = ant_system.get_best_solution()


        dados_resultados = {
            'num_cidades': data['city_number'],
            'optimum': optimum,
            'solution': solution
        }
        AntColony.nice_print(**dados_resultados)


