# -*- coding: utf-8 -*-
"""
list prompt example
"""
from __future__ import print_function, unicode_literals
from PyInquirer import prompt, Separator, style_from_dict, Token

from pyfiglet import Figlet, figlet_format
from rich import print

from answers_handler import Handler

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


def action_choices(answers):
    choices = ['Nenhuma opção encontrada ):']
    if answers['action'] == 'Executar Algoritmo':
        choices = [
            Separator('= Algoritmos ='),
            'Algoritmo Genetico Rep. Binaria',
            'Algoritmo Genetico Rep. Real',
            'Colônia de Formigas',
            'PSO'
        ]
        return choices
    elif answers['action'] == 'Algoritmo Genetico Interativo':
        choices = [
            # Separator('= Isso irá abrir seu navegador ='),
            # 'Link: ...'
            Separator('= EM BREVE =')
        ]
        return choices
    elif answers['action'] == 'Dicas para Gráficos e Análises':
        message = ''
        choices = [
            Separator('= Links e tutoriais que podem ajudar ='),
            'Link1: ...',
            'Link2: ...'
        ]
        return choices
    elif answers['action'] == 'Sair':
        raise SystemExit
    return choices


question = [
    {
        'type': 'list',
        'name': 'action',
        'message': 'O que deseja fazer?',
        'choices': [
            'Executar Algoritmo',
            Separator('= Extras ='),
            'Algoritmo Genetico Interativo',
            'Dicas para Gráficos e Análises',
            'Sair'
        ]
    },
    {
        'type': 'list',
        'name': 'which',
        'message': 'Escolha uma opção..',
        'choices': action_choices,
    },
]

bioinspirados_text = figlet_format('Bioinspirados', font='slant')
print(f'[bold blue]'
      f'{bioinspirados_text}'
      f'[/bold blue]')
try:
    while True:
        answers = prompt(question, style=style)
        handle_answers = Handler(answers)
        handle_answers.handle_which()
except KeyError:
    print('Ocorreu algum problema...tente executar novamente!')
