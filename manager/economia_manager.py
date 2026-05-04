# core/economia_manager.py - O Cérebro Estratégico do Rio de Janeiro
import random
from typing import Dict, List, Optional
from entities.economia import EconomiaBairro, TipoRecurso, CategoriaRebanho

class EconomiaGlobal:
    """
    Gerencia o tesouro central, a redistribuição de recursos e a 
    estabilidade da Mascarada em nível metropolitano.
    """
    def __init__(self, principe_nome: str, cla_principe: str):
        self.principe = principe_nome
        self.cla_principe = cla_principe
        self.bairros: Dict[str, EconomiaBairro] = {}
        self.sistema_corte = None # Será conectado no main.py
        
        # Reserva Central: O "Cofre" do Príncipe
        self.reserva_central: Dict[TipoRecurso, float] = {
            TipoRecurso.SANGUE: 50,
            TipoRecurso.INFLUENCIA: 30,
            TipoRecurso.MASCARADA: 100, # Status da cidade perante a Camarilla
            TipoRecurso.LORE: 10,
            TipoRecurso.MEDO: 0
        }
        
        self.turno_atual = 0
        self.blood_hunt_ativo = False
        self.alvo_blood_hunt = None

    def adicionar_bairro(self, nome: str, populacao: int = 10000):
        """Conecta um domínio do mapa ao sistema global"""
        bairro = EconomiaBairro(nome, populacao)
        self.bairros[nome] = bairro
        return bairro

    def transferir_recurso(self, tipo: TipoRecurso, origem: str, destino: str, quantidade: float) -> bool:
        """Transfere recursos entre bairros ou para o cofre central"""
        # Define os dicionários de estoque envolvidos
        estoque_origem = self.reserva_central if origem == "central" else self.bairros.get(origem).estoque
        estoque_destino = self.reserva_central if destino == "central" else self.bairros.get(destino).estoque

        if not estoque_origem or not estoque_destino or estoque_origem[tipo] < quantidade:
            return False
            
        estoque_origem[tipo] -= quantidade
        estoque_destino[tipo] += quantidade
        return True

    def processar_turno_global(self) -> Dict:
        """O grande motor da noite: Coleta, paga contas e gera crises"""
        self.turno_atual += 1
        
        # --- INICIALIZAÇÃO (O balde começa vazio para somar os bairros) ---
        total_sangue_noite = 0.0
        total_influencia_noite = 0.0
        alertas_globais = []
        
        # 1. PRODUÇÃO DOS BAIRROS
        # Varre todos os bairros que você adicionou ao eco_manager no main.py
        for nome_bairro, bairro in self.bairros.items():
            # O bairro calcula o que os Hospitais/Rebanhos geraram (conforme controlado_por)
            producao = bairro.calcular_producao_passiva()
            
            # Adiciona ao estoque específico do bairro (Microgerenciamento)
            for tipo, valor in producao.items():
                bairro.estoque[tipo] += valor
            
            # Soma ao montante que vai para o Príncipe (Macrogerenciamento)
            total_sangue_noite += producao.get(TipoRecurso.SANGUE, 0.0)
            total_influencia_noite += producao.get(TipoRecurso.INFLUENCIA, 0.0)
            
            # Coleta alertas locais (Investigação policial, etc)
            alertas_globais.extend(bairro.gerar_alertas())

        # 2. MANUTENÇÃO DA CORTE (Usando o SistemaCorte Real)
        custo_sangue = 0
        if self.sistema_corte:
            # Cada membro da corte central consome 2 de sangue por turno
            custo_sangue = len(self.sistema_corte.corte_central) * 2 
            
            # Tenta pagar a conta com o que tem na reserva central
            if self.reserva_central[TipoRecurso.SANGUE] >= custo_sangue:
                self.reserva_central[TipoRecurso.SANGUE] -= custo_sangue
            else:
                alertas_globais.append("🚨 REVOLTA NA CORTE: Falta sangue no tesouro central!")
                # Aqui o jogador começaria a perder lealdade dos NPCs

        # 3. ATUALIZAÇÃO DO COFRE CENTRAL
        # O que sobrou da produção menos o custo da corte vai para o bolso do jogador
        self.reserva_central[TipoRecurso.SANGUE] += total_sangue_noite
        self.reserva_central[TipoRecurso.INFLUENCIA] += total_influencia_noite

        # 4. EVENTOS ALEATÓRIOS (A pimenta do jogo: Rio 1989)
        evento = self._gerar_evento_global()
        if evento: 
            alertas_globais.append(evento)

        # 5. RETORNO PARA O HUD/TERMINAL
        return {
            "turno": self.turno_atual,
            "sangue_gerado": total_sangue_noite,
            "influencia_gerada": total_influencia_noite,
            "custo_manutencao": custo_sangue,
            "alertas": alertas_globais,
            "reserva": {k.value: v for k, v in self.reserva_central.items()}
        }

    def _gerar_evento_global(self) -> Optional[str]:
        if random.random() > 0.15: return None
        eventos = [
            "📰 Reportagem investigativa no 'O Globo' ameaça a Masquerade!",
            "⛪ Inquisição: Rumores de agentes do Vaticano no Galeão.",
            "🌕 Lua Cheia: Gangrels da periferia estão em frenesi.",
            "🦇 Anarquistas: Pichações contra o Príncipe na Lapa."
        ]
        return random.choice(eventos)

    def get_resumo_imperio(self) -> Dict:
        """Visão geral rápida para o HUD"""
        total_pop = sum(b.populacao_total for b in self.bairros.values())
        avg_mascarada = sum(b.estoque[TipoRecurso.MASCARADA] for b in self.bairros.values()) / (len(self.bairros) or 1)
        
        return {
            "bairros_controlados": len(self.bairros),
            "populacao_total": total_pop,
            "masquerade_media": round(avg_mascarada, 1),
            "sangue_central": self.reserva_central[TipoRecurso.SANGUE],
            "risco_inquisicao": "ALTO" if avg_mascarada < 40 else "BAIXO"
        }
    
    def registrar_conquista(self, nome_bairro, jogador):
            if nome_bairro in self.bairros:
                # Muda a lealdade econômica do bairro
                bairro_eco = self.bairros[nome_bairro]
                # Aqui você pode resetar a estabilidade ou mudar o controle dos recursos
                for recurso in bairro_eco.recursos_regionais:
                    recurso.controlado_por = jogador.nome
                print(f"💰 Economia de {nome_bairro} agora sob controle de {jogador.nome}")