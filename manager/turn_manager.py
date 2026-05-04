import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class FaseTurno(Enum):
    COLETA_SANGUE = "coleta"      # Recursos do rebanho
    MANUTENCAO = "manutencao"      # Pagar custos da corte
    ACOES_JOGADOR = "acoes"        # Jogador move peças
    DECISOES_CORTE = "corte"       # AI dos vampiros
    EVENTOS = "eventos"            # Eventos aleatórios
    RESOLUCAO = "resolucao"        # Combate/conspirações

@dataclass
class RelatorioTurno:
    """Tudo que aconteceu em um turno"""
    numero: int
    fases_executadas: List[FaseTurno]
    
    # Economia
    producao_sangue: float = 0
    producao_influencia: float = 0
    custo_corte: Dict[str, float] = None
    
    # Corte
    decisoes_vampiros: List[dict] = None
    traidores_detectados: List[str] = None
    promocoes: List[dict] = None
    
    # Eventos
    eventos_aleatorios: List[dict] = None
    crises: List[str] = None
    
    # Alertas para o jogador
    alertas_urgentes: List[str] = None
    
    def __post_init__(self):
        if self.custo_corte is None:
            self.custo_custo_corte = {}
        if self.decisoes_vampiros is None:
            self.decisoes_vampiros = []
        if self.traidores_detectados is None:
            self.traidores_detectados = []
        if self.eventos_aleatorios is None:
            self.eventos_aleatorios = []
        if self.crises is None:
            self.crises = []
        if self.alertas_urgentes is None:
            self.alertas_urgentes = []

class TurnManager:
    """
    Orquestra um turno completo (noite) no jogo.
    """
    
    def __init__(self, sistema_corte, economia_global=None):
        self.corte = sistema_corte
        self.economia = economia_global
        self.turno_atual = 0
        self.historico = []  # Lista de RelatorioTurno
        
        # Configurações de balanceamento
        self.config = {
            "custo_sangue_por_vampiro": 1.0,
            "chance_evento_aleatorio": 0.25,
            "limite_alertas": 5,
            "fome_threshold": 3  # Sangue < 3 = vampiro desesperado
        }
    
    def processar_turno_completo(self, acoes_jogador: List[dict], eco_manager, sistema_corte) -> RelatorioTurno:
        """
        Executa TODAS as fases de um turno.
        """
        self.turno_atual += 1
        relatorio = RelatorioTurno(
            numero=self.turno_atual,
            fases_executadas=[]
        )
        
        print(f"\n🌙=== NOITE {self.turno_atual} ===🌙")
        
        # FASE 1: Coleta de Sangue (Integrada com o Eco Manager)
        if eco_manager:
            resultado_turno = eco_manager.processar_turno_global()
            relatorio.producao_sangue = resultado_turno["sangue_gerado"]
        
        # FASE 2: Outras fases (Protegidas para não dar erro se não existirem)
        fases = [
            ("_fase_manutencao", [relatorio]),
            ("_fase_acoes_jogador", [acoes_jogador, relatorio]),
            ("_fase_decisoes_corte", [relatorio]),
            ("_fase_eventos", [relatorio]),
            ("_fase_resolucao", [relatorio]),
            ("_fase_verificacao_crise", [relatorio])
        ]

        for nome_fase, args in fases:
            metodo = getattr(self, nome_fase, None)
            if metodo:
                metodo(*args)

        # Salvar histórico
        self.historico.append(relatorio)
        self._print_resumo(relatorio)
        
        return relatorio
    
    def _fase_coleta_sangue(self, rel: RelatorioTurno):
        """Calcula produção de sangue e influência"""
        rel.fases_executadas.append(FaseTurno.COLETA_SANGUE)
        
        if self.economia:
            # Usa sistema econômico existente
            resultado = self.economia.processar_turno_global()
            rel.producao_sangue = resultado.get("reserva_central", {}).get("sangue", 0)
            rel.producao_influencia = resultado.get("reserva_central", {}).get("influencia", 0)
        else:
            # Fallback simples
            rel.producao_sangue = len(self.corte.corte_central) * 2
            rel.producao_influencia = 5
            
        print(f"   💉 Sangue coletado: {rel.producao_sangue}")
        print(f"   💰 Influência gerada: {rel.producao_influencia}")
    
    def _fase_manutencao(self, rel: RelatorioTurno):
        """Paga custos da corte, verifica fome"""
        rel.fases_executadas.append(FaseTurno.MANUTENCAO)
        
        custo_total = {"sangue": 0, "influencia": 0}
        vampiros_famintos = []
        
        for vid, vamp in self.corte.corte_central.items():
            # Custo base por vampiro
            custo = self.config["custo_sangue_por_vampiro"]
            
            # Anciões comem mais
            if vamp.geracao <= 8:
                custo += 1
                
            # Pagar
            vamp.sangue_atual -= custo
            custo_total["sangue"] += custo
            
            # Verificar fome
            if vamp.sangue_atual < self.config["fome_threshold"]:
                vampiros_famintos.append(vamp.nome)
                # Fome reduz lealdade
                vamp.personalidade.lealdade_base -= 1
                
        rel.custo_corte = custo_total
        
        if vampiros_famintos:
            rel.alertas_urgentes.append(f"🚨 Vampiros famintos: {', '.join(vampiros_famintos[:3])}")
            
        print(f"   💸 Custo da corte: {custo_total}")
    
    def _fase_acoes_jogador(self, acoes: List[dict], rel: RelatorioTurno):
        """Processa o que o jogador fez neste turno"""
        rel.fases_executadas.append(FaseTurno.ACOES_JOGADOR)
        
        for acao in acoes:
            tipo = acao.get("tipo")
            
            if tipo == "promover":
                vid = acao.get("vampiro_id")
                cargo = acao.get("cargo")
                sucesso, msg = self.corte.nomear_para_cargo(vid, cargo)
                if sucesso:
                    rel.promocoes.append({"vampiro": vid, "cargo": cargo.value})
                    
            elif tipo == "criar_childe":
                nome = acao.get("nome")
                cla = acao.get("cla")
                invest = acao.get("investimento", 3)
                childe = self.corte.criar_childe(nome, cla, invest)
                rel.alertas_urgentes.append(f"✨ Nova cria: {childe.nome}")
                
            elif tipo == "mover":
                # Implementar movimentação entre bairros
                pass
                
        print(f"   🎮 Ações do jogador: {len(acoes)}")
    
    def _fase_decisoes_corte(self, rel: RelatorioTurno):
        """Cada vampiro decide: obedecer, conspirar, trair?"""
        rel.fases_executadas.append(FaseTurno.DECISOES_CORTE)
        
        # Prepara contexto para decisões
        contexto = {
            "turno": self.turno_atual,
            "principe_forte": rel.producao_sangue > 10,
            "crise_mascarada": False  # TODO: verificar
        }
        
        # Processa via sistema de corte
        eventos_mundo = []  # Pode adicionar eventos externos
        decisoes = self.corte.processar_turno(eventos_mundo)
        
        rel.decisoes_vampiros = decisoes
        
        # Verifica traidores
        for vid, vamp in self.corte.corte_central.items():
            if vid == 0:  # Pula jogador
                continue
                
            # Verifica se vai trair
            situacao = {
                "fome": self.config["fome_threshold"] - vamp.sangue_atual,
                "oportunidade": vamp.calcular_poder_total() > 15
            }
            
            if vamp.personalidade.verificar_traicao_potencial(situacao):
                rel.traidores_detectados.append(vamp.nome)
                
        if rel.traidores_detectados:
            rel.alertas_urgentes.append(f"⚠️ Conspiração detectada: {len(rel.traidores_detectados)} vampiros")
            
        print(f"   🧛 Decisões da corte: {len(decisoes)}")
    
    def _fase_eventos(self, rel: RelatorioTurno):
        """Eventos aleatórios do mundo"""
        rel.fases_executadas.append(FaseTurno.EVENTOS)
        
        if random.random() > self.config["chance_evento_aleatorio"]:
            return
            
        eventos_possiveis = [
            {
                "tipo": "anciao_desperta",
                "titulo": "Ancião Desperta",
                "descricao": "Um vampiro de 500 anos despertou em Copacabana",
                "impacto": {"sangue": -5, "medo": +10}
            },
            {
                "tipo": "inquisicao",
                "titulo": "Inquisição",
                "descricao": "Caçadores avistados no Centro",
                "impacto": {"mascarada": -10, "influencia": -3}
            },
            {
                "tipo": "anarquistas",
                "titulo": "Rebelião Anarquista",
                "descricao": "Brujahs tomaram controle de Bangu",
                "impacto": {"territorio": "Bangu", "sangue": -3}
            },
            {
                "tipo": "festa_elysium",
                "titulo": "Elysium Convocado",
                "descricao": "Grande reunião social - todos devem comparecer",
                "impacto": {"influencia": +5, "sangue": -2}
            },
            {
                "tipo": "escandalo_midia",
                "titulo": "Escândalo na Mídia",
                "descricao": "Jornal investiga desaparecimentos",
                "impacto": {"mascarada": -15}
            }
        ]
        
        evento = random.choice(eventos_possiveis)
        rel.eventos_aleatorios.append(evento)
        
        print(f"   📰 Evento: {evento['titulo']}")
    
    def _fase_resolucao(self, rel: RelatorioTurno):
        """Resolve combates, conspirações, etc"""
        rel.fases_executadas.append(FaseTurno.RESOLUCAO)
        
        # TODO: Implementar resolução de conflitos
        # - Blood Hunts ativos
        # - Invasões de território
        # - Conspirações descobertas
        
        pass
    
    def _fase_verificacao_crise(self, rel: RelatorioTurno):
        """Verifica condições de vitória/derrota"""
        # Mudança cirúrgica: Usamos RESOLUCAO porque VERIFICACAO não existe no Enum FaseTurno
        rel.fases_executadas.append(FaseTurno.RESOLUCAO)
        
        crises = []
        
        # Exemplo de lógica de crise (podes expandir depois)
        if rel.producao_sangue < 0:
            crises.append("Fome generalizada nos teus domínios!")
            rel.alertas_urgentes.append("⚠️ CRISE: A produção de sangue está negativa!")
            
        rel.crises = crises
        
        # Crise de lealdade: muitos traidores
        if len(rel.traidores_detectados) > len(self.corte.corte_central) * 0.3:
            crises.append("CRISE: Conspiração em massa!")
            
        # Crise de recursos: sem sangue
        if rel.producao_sangue < rel.custo_corte.get("sangue", 0):
            crises.append("CRISE: Corte faminta!")
            
        # Crise de Masquerade
        # TODO: Implementar sistema de Masquerade
        
        rel.crises = crises
        
        if crises:
            for c in crises:
                rel.alertas_urgentes.append(f"🔴 {c}")
                
    def _print_resumo(self, rel: RelatorioTurno):
        """Printa resumo no console (para debugging)"""
        print(f"\\n📊 RESUMO DO TURNO {rel.numero}:")
        print(f"   Recursos: +{rel.producao_sangue:.0f} sangue, +{rel.producao_influencia:.0f} influência")
        print(f"   Eventos: {len(rel.eventos_aleatorios)}")
        print(f"   Alertas: {len(rel.alertas_urgentes)}")
        if rel.alertas_urgentes:
            for alerta in rel.alertas_urgentes[:3]:
                print(f"      {alerta}")
    
    # ============ MÉTODOS DE CONSULTA ============
    
    def get_estatisticas(self) -> dict:
        """Retorna estatísticas da partida"""
        if not self.historico:
            return {}
            
        total_sangue = sum(r.producao_sangue for r in self.historico)
        total_eventos = sum(len(r.eventos_aleatorios) for r in self.historico)
        
        return {
            "turnos_jogados": self.turno_atual,
            "sangue_total_acumulado": total_sangue,
            "eventos_ocorridos": total_eventos,
            "media_sangue_por_turno": total_sangue / self.turno_atual if self.turno_atual > 0 else 0
        }
    
    def simular_turnos(self, n: int) -> List[RelatorioTurno]:
        """
        Simula N turnos rapidamente (para balanceamento/testes).
        NÃO renderiza nada - útil para testar economia.
        """
        relatorios = []
        for _ in range(n):
            rel = self.processar_turno_completo([])
            relatorios.append(rel)
        return relatorios
