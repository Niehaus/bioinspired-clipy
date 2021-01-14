from algoritmos.algoritmo_genetico.ag_b_runner import AGb
from algoritmos.algoritmo_genetico.ag_r_runner import AGr
from algoritmos.colonia_formigas.ant_colony_runner import AntColony
from algoritmos.pso.pso_runner import PSO


class Handler:
    def __init__(self, answers):
        self.action = answers['action'],
        self.which = answers['which']
        self.chosen = {
            'Algoritmo Genetico Rep. Binaria': AGb(),
            'Algoritmo Genetico Rep. Real': AGr(),
            'Colônia de Formigas': AntColony(),
            'PSO': PSO()
        }

        self.action = ''.join(self.action)
        self.which = ''.join(self.which)

    def handle_which(self):
        if self.action == 'Executar Algoritmo':
            executioner = self.chosen[self.which]
            executioner.run()
        elif self.action == 'Acesso ao Código':
            print('')

