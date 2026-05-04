# manager/evento_manager.py
import random
from typing import Optional, List
from manager.economia_manager import TipoRecurso
from entities.evento import (
    EVENTOS_POSSIVEIS, evento_primeira_noite, 
    evento_fome_na_corte, evento_conflito_favela, evento_malkaviano_lapa
)

class EventManager:
    """
    Gerencia o destino do Rio. Responsável por disparar crises de fome,
    conflitos políticos e eventos narrativos estilo CK3.
    """

    def __init__(self, corte_manager, jogador, economia_manager):
        self.corte = corte_manager
        self.jogador = jogador
        self.economia = economia_manager
        self.turno_ultimo_evento = 0
        self.eventos_ja_disparados = set()

    def deve_disparar_evento(self, turno_atual: int) -> bool:
        """Define a chance de um evento acontecer"""
        if turno_atual == 1:
            return True
        
        # Garante um respiro entre eventos narrativos, 
        # mas crises de fome podem ignorar isso se necessário
        if turno_atual - self.turno_ultimo_evento < 2:
            return False
        
        return random.random() < 0.45  # 45% de chance

    def verificar_crises_prioritarias(self):
        """Verifica se existem condições para eventos de urgência (Ex: Fome)"""
        sangue_atual = self.economia.reserva_central.get(TipoRecurso.SANGUE, 0)
        
        # Se o sangue estiver abaixo de 10, a Fome é quase certa
        if sangue_atual < 10:
            return evento_fome_na_corte(self.corte, self.economia)
        return None

    def gerar_evento(self, turno_atual: int):
            """Gera e retorna um evento baseado em prioridade e probabilidade."""
            from manager.economia_manager import TipoRecurso
            
            # 1. EMERGÊNCIA REAL: CRISE DE SANGUE (Prioridade Absoluta)
            # Ela ignora travas de turno e chance aleatória.
            sangue_total = self.economia.reserva_central.get(TipoRecurso.SANGUE, 0)
            if sangue_total < 10:
                print(f"🚨 MOTOR: Sangue crítico ({sangue_total})! Forçando Crise de Fome.")
                self.turno_ultimo_evento = turno_atual
                return evento_fome_na_corte(self.corte, self.economia)

            # 2. EVENTO DE ABERTURA (Apenas Turno 1)
            if turno_atual == 1 and "primeira_noite" not in self.eventos_ja_disparados:
                print("📜 MOTOR: Disparando evento de abertura.")
                self.eventos_ja_disparados.add("primeira_noite")
                self.turno_ultimo_evento = turno_atual
                return evento_primeira_noite(self.corte, self.jogador)

            # 3. TRAVA DE INTERVALO (Evita spam de eventos narrativos)
            if turno_atual - self.turno_ultimo_evento < 2:
                return None

            # 4. SORTEIO DE EVENTOS NARRATIVOS (45% de chance)
            if random.random() < 0.45:
                # Filtramos para não repetir abertura nem a crise (que já tem check próprio acima)
                eventos_disponiveis = [
                    func for func in EVENTOS_POSSIVEIS 
                    if func.__name__ not in ["evento_primeira_noite", "evento_fome_na_corte"]
                ]
                
                if not eventos_disponiveis:
                    return None

                # --- LÓGICA DE PESOS DINÂMICOS ---
                pesos = []
                medo_atual = self.economia.reserva_central.get(TipoRecurso.MEDO, 0)
                
                for func in eventos_disponiveis:
                    peso_base = getattr(func, 'peso', 100)
                    # Exemplo: Se o Medo estiver alto, eventos de conflito aparecem mais
                    if "conflito" in func.__name__ and medo_atual > 50:
                        peso_base += 50
                    pesos.append(peso_base)

                # Sorteia baseado nos pesos
                evento_func = random.choices(eventos_disponiveis, weights=pesos, k=1)[0]
                
                # DEBUG FINAL DO MOTOR
                print(f"🎲 MOTOR: Sorteio realizado! Evento escolhido: {evento_func.__name__}")
                
                self.turno_ultimo_evento = turno_atual
                
                # Tenta disparar com economia ou apenas corte
                try:
                    return evento_func(self.corte, self.economia)
                except:
                    return evento_func(self.corte)

            return None # Caso não passe no random de 45%