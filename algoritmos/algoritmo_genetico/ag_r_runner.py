from ..algoritmo_genetico.ag_r_alg import AGrAlg


class AGr:
    def __init__(self):
        ...

    def run(self):
        params = {
            'taxa_mutacao': 1,
            'taxa_cruzamento': 1,
            'npop': 25,
            'ngen': 10,
            'dimensao': 6
        }
        ag_b = AGrAlg(**params)
        gen_atual = 0
        alpha = 0.75
        beta = 0.25

        # variaveis p/ os plots
        avg_fitness = []
        gen_fitness = []
        melhor_da_geracao = []

        ag_b.print_argumentos()
        populacao = ag_b.cria_geracao_inicial(gen_atual)
        for indv in populacao:
            indv.fitness = ag_b.func_obj(indv.rep_real)
            gen_fitness.append(indv.fitness)
        melhor_da_geracao.append(min(gen_fitness))
        avg_fitness.append(gen_fitness)
        gen_fitness = []

        gen_atual += 1
        while gen_atual < params['ngen']:
            pais_sorteados_roleta = ag_b.roleta(populacao)
            pop_intermediaria = ag_b.cruzamento(pais_sorteados_roleta, gen_atual, alpha, beta)
            ag_b.mutacao(pop_intermediaria)
            ag_b.elitismo(populacao, pop_intermediaria)
            populacao = pop_intermediaria[:]
            for indv in populacao:
                indv.fitness = ag_b.func_obj(indv.rep_real)
                gen_fitness.append(indv.fitness)
            melhor_da_geracao.append(min(gen_fitness))
            avg_fitness.append(gen_fitness)
            gen_fitness = []
            gen_atual += 1

        ag_b.resultado(melhor_da_geracao, avg_fitness)