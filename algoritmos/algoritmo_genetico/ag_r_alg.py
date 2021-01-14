import math
import random
from rich import print
from rich.panel import Panel

import numpy as np


class AGrAlg:
    def __init__(self, taxa_mutacao, taxa_cruzamento, npop, ngen, dimensao):
        self.taxa_mutacao = taxa_mutacao
        self.taxa_cruzamento = taxa_cruzamento
        self.npop = npop
        self.ngen = ngen
        self.dimensao = dimensao

    @staticmethod
    def func_obj(x):

        n = float(len(x))
        f_exp = -0.2 * math.sqrt(1 / n * sum(np.power(x, 2)))

        t = 0
        for i in range(0, len(x)):
            t += np.cos(2 * math.pi * x[i])

        s_exp = 1 / n * t
        f = -20 * math.exp(f_exp) - math.exp(s_exp) + 20 + math.exp(1)

        return f

    def gerador_individuo(self):
        """Gera individuo random de tamanho n, setar igual ao do tutorial1"""
        individuos_tmp = []
        for index in range(self.dimensao):
            individuos_tmp.append(random.uniform(-2, 2))
        # print(individuos_tmp)
        return individuos_tmp

    def cria_geracao_inicial(self, gen_atual):
        """Inicializa cada individuo e sua representacao binaria"""
        populacao = []
        for i in range(self.npop):
            populacao.append(Individuo(i, gen_atual))
            populacao[-1].rep_real = self.gerador_individuo()
        return populacao

    @staticmethod
    def cria_roleta(populacao, roleta, fitness_total):
        """Cria roleta a partir dos fitness invertidos, pois
            trata-se de uma função de minimização, normalizar pelo rank"""
        fit = []
        for indv in populacao:
            if indv.fitness > 0:
                fit.append(1 / indv.fitness)
            elif indv.fitness == 0:
                fit.append(1)
            fitness_total += fit[-1]

        for i in range(len(fit)):
            roleta.append(fit[i] / fitness_total)

    def roleta(self, populacao):
        """Considerando uma função de minimização, método de seleção
        de pais escolhido:"""
        fitness_total = 0
        roleta = []
        limite_sorteado = 0
        acumulador_roleta = 0
        num_pais_sorteados = 0
        lista_pais_sorteados = []
        self.cria_roleta(populacao, roleta, fitness_total)
        while num_pais_sorteados < round(self.npop):
            limite_sorteado = random.random()
            for index in range(len(roleta)):
                acumulador_roleta += roleta[index]
                if acumulador_roleta >= limite_sorteado:
                    acumulador_roleta = 0
                    num_pais_sorteados += 1
                    lista_pais_sorteados.append(populacao[index])
                    break
        return lista_pais_sorteados

    @staticmethod
    def organiza_pares(pais_sorteados):
        mv_indv = Individuo(0, 0)
        for i in range(0, len(pais_sorteados), 2):
            if i == len(pais_sorteados) - 1: break
            if pais_sorteados[i].id == pais_sorteados[i + 1].id:
                prox_pai = i + 2
                for j in range(prox_pai, len(pais_sorteados)):
                    if pais_sorteados[i].id != pais_sorteados[j].id:
                        mv_indv = pais_sorteados[j]
                        pais_sorteados[j] = pais_sorteados[i + 1]
                        pais_sorteados[i + 1] = mv_indv
                        break

    def cruzamento(self, pais_sorteados, gen_atual, alpha, beta):
        """Cruzamento utilizando blend-alphaBeta """
        pop_intermediaria = []
        d = []
        rep_real_aleatoria_x = []
        rep_real_aleatoria_y = []
        self.organiza_pares(pais_sorteados)
        for i in range(0, len(pais_sorteados), 2):
            if i == len(pais_sorteados) - 1:
                break
            chance_cruzamento = random.random()
            if chance_cruzamento <= self.taxa_cruzamento:  # Houve cruzamento
                for dim in range(self.dimensao):
                    X = pais_sorteados[i].rep_real[dim]
                    Y = pais_sorteados[i + 1].rep_real[dim]
                    d.append(abs(X - Y))
                    if X <= Y:
                        rep_real_aleatoria_x.append(random.uniform(X - alpha * d[dim], Y + beta * d[dim]))
                        rep_real_aleatoria_y.append(random.uniform(X - alpha * d[dim], Y + beta * d[dim]))
                    else:
                        rep_real_aleatoria_x.append(random.uniform(Y - beta * d[dim], X + alpha * d[dim]))
                        rep_real_aleatoria_y.append(random.uniform(Y - beta * d[dim], X + alpha * d[dim]))
                # Cria filho X'
                pop_intermediaria.append(Individuo(i, gen_atual))
                pop_intermediaria[-1].rep_real = rep_real_aleatoria_x

                # Cria filho Y'
                pop_intermediaria.append(Individuo(i + 1, gen_atual))
                pop_intermediaria[-1].rep_real = rep_real_aleatoria_y
                d = []
                rep_real_aleatoria_x = []
                rep_real_aleatoria_y = []
            else:  # Não houve cruzamento
                pop_intermediaria.append(pais_sorteados[i])
                pop_intermediaria.append(pais_sorteados[i + 1])

        return pop_intermediaria

    def mutacao(self, pop_intermediaria):
        """Mutar a rep_real de uma dimensão sorteada"""
        for indv in pop_intermediaria:
            chance_mutacao = random.random()
            if chance_mutacao <= self.taxa_mutacao:  # Se vai haver mutação ou não
                index_mutacao = random.randint(0, self.dimensao - 1)
                indv.rep_real[index_mutacao] = random.random()

    @staticmethod
    def elitismo(populacao, pop_intermediaria):
        menor_fitness = 1000
        menorf_index = 0
        for index in range(len(populacao)):
            if populacao[index].fitness < menor_fitness:
                menor_fitness = populacao[index].fitness
                menorf_index = index
        indiv_aleatorio = random.randint(0, len(pop_intermediaria) - 1)
        pop_intermediaria[indiv_aleatorio] = populacao[menorf_index]

    def print_argumentos(self):
        print('\n')
        print(
            Panel.fit(
                f'Taxa de Mutação = {str(self.taxa_mutacao)}'
                f'\nTaxa de Cruzamento = {str(self.taxa_cruzamento)}'
                f'\nTamanho da População = {str(self.npop)}'
                f'\nNúmero de Gerações = {str(self.ngen)}',
                title="[bold magenta]Argumentos do AG[/bold magenta]",
                border_style='magenta'
            )
        )

    @staticmethod
    def resultado(melhor_da_geracao, avg_fitness):
        print(
            Panel.fit(
                f'Fitness Médio [bold red][Última Geração][/bold red]: '
                f'{round(float(np.mean(avg_fitness[-1])), 2)}'
                f'\nMelhor fitness: {round(min(melhor_da_geracao), 2)}',
                title="[bold green]Resultados do AG[/bold green]",
                border_style='green'
            )
        )


class Individuo:
    """Def do individuo de dimensao x"""

    def __init__(self, id, geracao):
        self.id = id
        self.geracao = geracao
        self.rep_real = []
        self.fitness = 0
