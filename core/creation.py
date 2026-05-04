# core/creation.py
import time
import random
import json
import os
import sys


# BLINDAGEM DE IMPORT: Faz o script achar a pasta 'entities' mesmo rodando do 'core'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entities.clans import CLANS_DB
from entities.player import PersonagemVampiro, NATUREZAS
from core.engine import rolar_dados

# --- MOTOR DE REGRAS (DADOS, SANGUE E GERAÇÃO) ---

def resolver_invasao(atacante, defensor_bairro):
    """
    Calcula quem ganha a disputa por um bairro no mapa.
    """
    print(f"⚔️ {atacante.nome} está invadindo {defensor_bairro.nome}!")
    
    pool_ataque = atacante.atributos["Físicos"]["Força"] + atacante.disciplinas.get("Potência", 0)
    diff = 6 
    
    resultado = rolar_dados(pool_ataque, diff)
    
    if resultado["sucessos"] > 0:
        return True 
    return False 

TABELA_GERACAO = {
    12: {"max_sangue": 10, "gasto_turno": 1},
    11: {"max_sangue": 10, "gasto_turno": 1},
    10: {"max_sangue": 11, "gasto_turno": 1},
    9:  {"max_sangue": 12, "gasto_turno": 1},
    8:  {"max_sangue": 13, "gasto_turno": 1},
    7:  {"max_sangue": 20, "gasto_turno": 4},
    6:  {"max_sangue": 30, "gasto_turno": 6}
}

CUSTOS_BONUS = {
    "Atributo": 5, "Habilidade": 2, "Disciplina": 7,
    "Antecedente": 1, "Virtude": 2, "Humanidade": 1, "Força de Vontade": 1
}

# --- CLASSE DE CRIAÇÃO ---

class CriadorPersonagem:
    def __init__(self):
        self.etapa = "ESCOLHA_CLÃ"
        self.pontos_atributos = {"Físicos": 0, "Sociais": 0, "Mentais": 0}
        self.pontos_habilidades = {"Talentos": 0, "Perícias": 0, "Conhecimentos": 0}
        
    def listar_clans(self):
        print("\n--- ESCOLHA SEU CLÃ ---")
        for i, clan in enumerate(CLANS_DB.keys(), 1):
            print(f"{i}. {clan} - {CLANS_DB[clan]['perfil']}")
            
    def configurar_prioridades_atributos(self, p1, p2, p3):
        self.pontos_atributos[p1] = 7
        self.pontos_atributos[p2] = 5
        self.pontos_atributos[p3] = 3

    def configurar_prioridades_habilidades(self, p1, p2, p3):
        self.pontos_habilidades[p1] = 13
        self.pontos_habilidades[p2] = 9
        self.pontos_habilidades[p3] = 5

    def validar_ponto_atributo(self, personagem, categoria, atributo):
        if self.pontos_atributos[categoria] > 0:
            valor_atual = personagem.atributos[categoria][atributo]
            if valor_atual < 5: 
                personagem.atributos[categoria][atributo] += 1
                self.pontos_atributos[categoria] -= 1
                return True
        return False

    def validar_ponto_habilidade(self, personagem, categoria, habilidade):
        if self.pontos_habilidades[categoria] > 0:
            valor_atual = personagem.habilidades[categoria][habilidade]
            if valor_atual < 3: 
                personagem.habilidades[categoria][habilidade] += 1
                self.pontos_habilidades[categoria] -= 1
                return True
        return False

    def gastar_pontos_bonus(self, personagem, tipo, categoria=None, item=None):
        custo = CUSTOS_BONUS.get(tipo)
        if personagem.pontos_bonus >= custo:
            if tipo == "Atributo":
                personagem.atributos[categoria][item] += 1
            elif tipo == "Habilidade":
                personagem.habilidades[categoria][item] += 1
            elif tipo == "Disciplina":
                personagem.disciplinas[item] += 1
            elif tipo == "Força de Vontade":
                personagem.forca_de_vontade += 1
            
            personagem.pontos_bonus -= custo
            return True
        return False

# --- FUNÇÕES DE SUPORTE E GERADOR DE ALIADOS ---

def gerar_aliado_aleatorio(nome_aliado):
    clan_nome = random.choice(list(CLANS_DB.keys()))
    natureza = random.choice(NATUREZAS)
    comportamento = random.choice(NATUREZAS)
    genero = random.choice(["Masculino", "Feminino"])
    
    # Ajuste para bater com o player.py
    aliado = PersonagemVampiro(nome_aliado, clan_nome, natureza, comportamento, genero)
    foco = aliado.clan_info["atributo_foco"]
    categorias = ["Físicos", "Sociais", "Mentais"]
    random.shuffle(categorias)
    
    for cat in categorias:
        if foco in aliado.atributos[cat]:
            categorias.remove(cat)
            categorias.insert(0, cat)
            break
            
    prioridades = [7, 5, 3]
    for i, cat in enumerate(categorias):
        pontos = prioridades[i]
        while pontos > 0:
            atrib = random.choice(list(aliado.atributos[cat].keys()))
            if aliado.atributos[cat][atrib] < 5:
                aliado.atributos[cat][atrib] += 1
                pontos -= 1
                
    disc_list = list(aliado.disciplinas.keys())
    aliado.disciplinas[disc_list[0]] = 1
    pontos_disc = 3
    while pontos_disc > 0:
        d = random.choice(disc_list)
        if aliado.disciplinas[d] < 3:
            aliado.disciplinas[d] += 1
            pontos_disc -= 1
    return aliado

def menu_criacao_completo():
    """
    Função mestra chamada pelo main.py
    """
    print("\n" + "="*40)
    print("🕯️   INICIANDO CRIAÇÃO DE PERSONAGEM - RIO 1989   🕯️")
    print("="*40)
    
    nome_input = input("Digite o nome do seu Príncipe: ")
    
    menu = CriadorPersonagem()
    menu.listar_clans()
    
    clans_disponiveis = list(CLANS_DB.keys())
    while True:
        try:
            escolha = int(input("\nEscolha o número do seu Clã: "))
            if 1 <= escolha <= len(clans_disponiveis):
                clan_escolhido = clans_disponiveis[escolha - 1]
                break
        except ValueError:
            pass
        print("❌ Opção inválida!")

    natureza = random.choice(NATUREZAS)
    comportamento = random.choice(NATUREZAS)
    
    # CRIANDO O PERSONAGEM REAL (Usando clan_nome para bater com player.py)
    jogador_real = PersonagemVampiro(
        nome=nome_input, 
        clan_nome=clan_escolhido, 
        natureza=natureza, 
        comportamento=comportamento, 
        genero="Masculino",
        eh_jogador=True
    )
    
    # DISTRIBUIÇÃO INICIAL DE PONTOS (Para o jogador não começar com tudo 1)
    prioridades = [7, 5, 3]
    categorias = ["Físicos", "Sociais", "Mentais"]
    random.shuffle(categorias)
    for i, cat in enumerate(categorias):
        pts = prioridades[i]
        while pts > 0:
            at = random.choice(list(jogador_real.atributos[cat].keys()))
            if jogador_real.atributos[cat][at] < 5:
                jogador_real.atributos[cat][at] += 1
                pts -= 1

    print(f"\n✅ Príncipe {jogador_real.nome} do Clã {clan_escolhido} despertou!")
    time.sleep(1)
    
    return jogador_real