import random
from actions.conquista import tentar_invasao
from entities.player import PersonagemVampiro
from manager.npc_manager import TierNPC

class FactionAI:
    def __init__(self, clan_nome, npc_manager):
        # O seu bloco exatamente como você mandou:
        self.clan_nome = clan_nome
        
        elites = [npc_manager.npcs[id_id] for id_id in npc_manager.por_clan.get(clan_nome, set()) 
                  if npc_manager.npcs[id_id].tier == TierNPC.ELITE]
        
        if elites:
            self.lider = elites[0]
        else:
            self.lider = PersonagemVampiro(f"Líder {clan_nome}", clan_nome, "Tirano", "Competidor", "Indefinido", eh_jogador=False)

        nome_lider = f"Líder {clan_nome}"
        self.lider = PersonagemVampiro(nome_lider, clan_nome, "Tirano", "Competidor", "Indefinido", eh_jogador=False)
        
        # Buff básico para os líderes de IA para darem trabalho
        self.lider.atributos["Físicos"]["Força"] = random.randint(3, 5)
        self.lider.habilidades["Militar"] = random.randint(2, 4)
        self.lider.sangue_atual = 10
        self.lider.sangue_max = 20

        # Personalidade da IA afeta a chance de ataque
        self.agressividade = self._definir_agressividade()

    def _definir_agressividade(self):
        # Brujah e Setitas atacam mais. Ventrue e Tremere são mais defensivos.
        agressivos = ["Brujah", "Setita", "Assamita", "Gangrel"]
        if self.clan_nome in agressivos:
            return 0.7  # 70% de chance de focar em guerra
        return 0.3      # 30% de chance (preferem acumular recursos)

    def turno_ai(self, mapa):
        relatorio_acoes = []
        
        # 1. Recupera um pouco de sangue passivamente por turno
        self.lider.sangue_atual = min(self.lider.sangue_max, self.lider.sangue_atual + 2)

        # 2. Descobre quais bairros a IA controla e quais são as fronteiras (vizinhos)
        meus_bairros = []
        alvos_potenciais = []

        for nome, dominio in mapa.items():
            if dominio.dono == self.clan_nome: # Se o clã é o dono, adiciona à lista
                meus_bairros.append(dominio)
            else:
                # Verifica se algum bairro não é meu, mas faz fronteira com algum que é meu
                for meu in meus_bairros:
                    if dominio.nome in meu.vizinhos and dominio not in alvos_potenciais:
                        alvos_potenciais.append(dominio)

        # Se a IA não tem bairros (foi destruída), ela não faz nada
        if not meus_bairros:
            return relatorio_acoes

        # 3. DECISÃO DE IA: Atacar ou Esperar?
        if alvos_potenciais and self.lider.sangue_atual >= 4:
            if random.random() < self.agressividade:
                # Escolhe um alvo aleatório das fronteiras
                alvo = random.choice(alvos_potenciais)
                
                # Executa o mesmo ataque que o jogador usaria (reaproveitando código!)
                resultado = tentar_invasao(self.lider, alvo)
                
                if resultado["sucesso"]:
                    # A IA agora é a dona real do bairro no mapa
                    alvo.dono = self.clan_nome
                    relatorio_acoes.append(f"⚠️ AVISO: O clã {self.clan_nome} conquistou {alvo.nome}!")
                else:
                    relatorio_acoes.append(f"⚔️ O clã {self.clan_nome} falhou ao tentar invadir {alvo.nome}.")

        return relatorio_acoes

class SistemaFaccoes:
    """Gerencia todas as IAs do jogo de uma vez"""
    def __init__(self, mapa_inicial, clan_jogador, npc_manager):
        self.faccoes = {}
        
        # Vasculha o mapa para descobrir quais clãs existem além do jogador
        for nome_bairro, dominio in mapa_inicial.items():
            dono = dominio.dono
            # Se não é o jogador e a facção ainda não foi criada, cria a IA
            if dono != clan_jogador and dono not in self.faccoes:
                self.faccoes[dono] = FactionAI(dono, npc_manager)

    def processar_turno_todas_faccoes(self, mapa):
        eventos_mundo = []
        for nome_clan, faccao in self.faccoes.items():
            acoes = faccao.turno_ai(mapa)
            eventos_mundo.extend(acoes)
        return eventos_mundo