from ..pso.pso_alg import PSOAlg
from rich import print
from rich.panel import Panel


class PSO:
    @staticmethod
    def run():
        diversification_factor = 0.729
        cognitive_factor = 1.49445
        social_factor = 1.49445
        dimension = 10
        cloud_size = 100
        max_iteration = 100
        k = 0

        pso = PSOAlg(
            dimension,
            diversification_factor,
            cognitive_factor,
            social_factor,
            [-10, 10]
        )
        cloud_particles = pso.initialize_cloud_particles(cloud_size)
        topology = pso.set_topology(cloud_particles)

        for i, particle in enumerate(cloud_particles, start=0):
            particle.initialize_coordinates(pso.sup_limit, pso.inf_limit)
            particle.neighbors = topology[i]
            pso.best_neighbor(cloud_particles, particle)

        while k < max_iteration:
            for i, particle in enumerate(cloud_particles, start=0):

                if pso.f(particle.x) < pso.f(particle.p_best):
                    particle.p_best = particle.x[:]
                    if pso.f(particle.x) < pso.f(pso.g_best):
                        pso.g_best = particle.x[:]
                for j in range(particle.dimension):
                    pij = particle.p_best[j]
                    gj = pso.g_best[j]
                    xij = particle.x[j]
                    particle.velocity[j] = pso.calculate_velocity(pij, gj, xij)
                particle.update_velocity()
            k += 1
        best_fitness = pso.f(pso.g_best)

        pso_result = {
            'inf_limit': pso.inf_limit,
            'sup_limit': pso.sup_limit,
            'cloud_size': cloud_size,
            'dimension': dimension,
            'best_fitness': best_fitness
        }

        PSO.nice_print(**pso_result)

    @staticmethod
    def nice_print(inf_limit, sup_limit, cloud_size, dimension, best_fitness):
        print('\n')
        print(
            Panel.fit(
                f'f6(x): [bold red]{inf_limit}[/bold red] <= xi <= [bold red]{sup_limit}[/bold red]\n'
                f'The global minimum is located at origin[bold red] x* = (0,. . .,0), f(x*) = 0[/bold red]\n'
                f'Number of particles: [bold red]{cloud_size}[/bold red]\n'
                f'Dimension(s): [bold red]{dimension}[/bold red]\n'
                f'Global Best founded: [bold green]{best_fitness}[/bold green]',
                title="[bold magenta]Resultados do PSO[/bold magenta]",
                border_style='magenta'
            )
        )
