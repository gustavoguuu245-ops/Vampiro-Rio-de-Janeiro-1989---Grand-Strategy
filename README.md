# Vampiro-Rio-de-Janeiro-1989---Grand-Strategy
Um Grand Strategy e RPG  desenvolvido inteiramente em Python e Pygame. Inspirado em mecânicas de jogos clássicos de simulação e intriga política (como Crusader Kings 3), o jogador assume o papel de um Príncipe recém-empossado no Rio de Janeiro do final dos anos 80, precisando gerenciar recursos, alianças, territórios e a sobrevivência da sua corte.

Nota sobre os Assets:
Para otimizar o repositório, os arquivos de imagem (mapas pesados em alta resolução e artes de interface) não foram incluídos. O foco deste repositório é demonstrar a arquitetura robusta de software e as lógicas complexas de simulação de estratégia em Python.

Principais Sistemas e Arquitetura
Ecossistema Vivo e IA (320 NPCs): O motor do jogo (npc_manager.py) simula simultaneamente 320 vampiros independentes. Cada NPC possui arquétipos de personalidade próprios, alianças de clã, nível de ambição e status social.

Sistema de Intriga e Traição: A Corte não é estática. Os NPCs calculam constantemente suas lealdades (corte_manager.py). Decisões impopulares do jogador ativam um sistema dinâmico de traição e motim, onde "aliados" podem conspirar e atacar o Príncipe pelas costas.

Motor de RPG Personalizado: Implementação completa do sistema de rolagem de dados (d10 pool), atributos, habilidades, vantagens e disciplinas (engine.py e disciplina.py).

Arquitetura MVC/Modular: Separação estrita de responsabilidades entre Dados (entities), Lógica de Turnos/Eventos (manager), Ações (actions) e Interface (main.py).

Simulação Econômica e Política: Gerenciamento de domínios no mapa do Rio de Janeiro (mapa.py), controle de rebanho, Mascarada, Influência e Sangue (economia_manager.py).

Motor de Eventos Procedurais: Sistema de eventos dinâmicos que avaliam o estado do jogo (medo da população, nível da Mascarada) para gerar crises, investigações ou oportunidades narrativas (evento_manager.py).

Tecnologias e Padrões
Python (OOP): Uso massivo de Programação Orientada a Objetos, Dataclasses, Enums e Type Hinting.

Pygame: Renderização do mapa estratégico e da interface de gerenciamento (HUD).

Design Patterns: Aplicação prática de conceitos de Managers, Game Loop e State Management.
