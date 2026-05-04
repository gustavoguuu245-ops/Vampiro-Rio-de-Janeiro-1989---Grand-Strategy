# entities/economia.py - Sistema Econômico Otimizado para VtM Grand Strategy
import random
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass, field

# 1. ENUMS E CONSTANTES
class TipoRecurso(Enum):
    SANGUE = "sangue"           # Mana/ações - consumido toda noite
    INFLUENCIA = "influencia"   # Dinheiro/poder político - compra tudo
    MASCARADA = "mascarada"     # Segurança/secreto - se zerar, Inquisição vem
    LORE = "lore"               # Conhecimento oculto - desbloqueia disciplinas
    MEDO = "medo"               # Terror/reputação - controle populacional

class CategoriaRebanho(Enum):
    VINCULADO = "vinculado"     # Laço de sangue - obedece cegamente
    DOMADO = "domado"           # Controlado temporariamente
    IGNORANTE = "ignorante"     # Não sabe de vampiros - caça fácil, risco alto

class ClasseSocial(Enum):
    # (Nome, Multiplicador Sangue, Multiplicador Influência)
    INDIGENTE = ("Indigente", 0.5, 0.1)
    TRABALHADOR = ("Trabalhador", 1.0, 0.3)
    CLASSE_MEDIA = ("Classe Média", 1.2, 0.8)
    ELITE = ("Elite", 0.8, 2.5)
    POLITICO = ("Político", 0.6, 4.0)
    CRIMINOSO = ("Criminoso", 1.5, 0.5)

    def __init__(self, nome, mult_sangue, mult_influencia):
        self.nome_exibicao = nome
        self.mult_sangue = mult_sangue
        self.mult_influencia = mult_influencia

# 2. COMPONENTES REGIONAIS
@dataclass 
class RecursoRegional:
    """Instalações fixas de um bairro (hospitais, bancos de sangue, etc)"""
    nome: str
    tipo: str  # "hospital", "banco_sangue", "midia", "delegacia", "boate", "favela"
    nivel: int = 1
    controlado_por: Optional[str] = None
    
    def get_producao(self) -> Dict[TipoRecurso, float]:
        tabela = {
            "hospital": {TipoRecurso.SANGUE: 3.0 * self.nivel, TipoRecurso.MASCARADA: -0.5},
            "banco_sangue": {TipoRecurso.SANGUE: 5.0 * self.nivel},
            "midia": {TipoRecurso.INFLUENCIA: 4.0 * self.nivel, TipoRecurso.MASCARADA: 1.0},
            "delegacia": {TipoRecurso.INFLUENCIA: 2.0 * self.nivel, TipoRecurso.MEDO: 1.0},
            "boate": {TipoRecurso.SANGUE: 2.0 * self.nivel, TipoRecurso.INFLUENCIA: 1.0, TipoRecurso.MASCARADA: -1.0},
            "favela": {TipoRecurso.SANGUE: 4.0 * self.nivel, TipoRecurso.MASCARADA: -2.0, TipoRecurso.MEDO: 2.0},
        }
        return tabela.get(self.tipo, {})

# 3. O BAIRRO (A ENTIDADE PRINCIPAL)
class EconomiaBairro:
    """
    Gerencia a economia de um bairro usando simulação de massa.
    """
    def __init__(self, nome: str, populacao_total: int = 10000):
        self.nome = nome
        self.populacao_total = populacao_total
        
        # Otimização: Em vez de mil objetos 'Humano', usamos contadores por classe
        self.populacao: Dict[ClasseSocial, int] = {}
        self.rebanho_vinculado: Dict[ClasseSocial, int] = {c: 0 for c in ClasseSocial}
        
        # Estoque local do bairro
        self.estoque: Dict[TipoRecurso, float] = {
            TipoRecurso.SANGUE: 10,
            TipoRecurso.INFLUENCIA: 5,
            TipoRecurso.MASCARADA: 100,
            TipoRecurso.LORE: 0,
            TipoRecurso.MEDO: 0
        }
        
        # Infraestrutura
        self.recursos_regionais: List[RecursoRegional] = []
        self.vampiros_presentes: List[str] = [] # Apenas nomes para evitar imports circulares
        
        # Status
        self.nivel_investigacao = 0  # Inquisição
        self.nivel_criminalidade = 0 # Anarquistas
        
        self._configurar_populacao_inicial()

    def _configurar_populacao_inicial(self):
        """Distribui a população total entre as classes sociais"""
        distribuicao = {
            ClasseSocial.INDIGENTE: 0.10,
            ClasseSocial.TRABALHADOR: 0.50,
            ClasseSocial.CLASSE_MEDIA: 0.25,
            ClasseSocial.ELITE: 0.08,
            ClasseSocial.POLITICO: 0.02,
            ClasseSocial.CRIMINOSO: 0.05
        }
        for classe, percentual in distribuicao.items():
            self.populacao[classe] = int(self.populacao_total * percentual)

    def calcular_producao_passiva(self) -> Dict[TipoRecurso, float]:
        """Calcula quanto o bairro gera sozinho antes de descontar custos"""
        total = {r: 0.0 for r in TipoRecurso}
        
        # 1. Produção do Rebanho Vinculado (Sua fonte estável)
        for classe, qtd in self.rebanho_vinculado.items():
            total[TipoRecurso.SANGUE] += qtd * classe.mult_sangue * 1.5
            total[TipoRecurso.INFLUENCIA] += qtd * classe.mult_influencia * 0.5

        # 2. Produção dos Recursos Regionais
        for recurso in self.recursos_regionais:
            if recurso.controlado_por:
                for tipo, valor in recurso.get_producao().items():
                    total[tipo] += valor

        # 3. Penalidades de Investigação
        if self.nivel_investigacao > 5:
            total[TipoRecurso.MASCARADA] -= 2.0
            
        return total

    def adicionar_recurso(self, nome: str, tipo: str, nivel: int = 1):
        novo = RecursoRegional(nome, tipo, nivel)
        self.recursos_regionais.append(novo)
        return novo

    def gerar_alertas(self) -> List[str]:
        alertas = []
        if self.estoque[TipoRecurso.MASCARADA] < 40:
            alertas.append(f"⚠️ Mascarada instável em {self.nome}!")
        if self.nivel_investigacao > 7:
            alertas.append(f"🔥 INQUISIÇÃO ATIVA em {self.nome}!")
        return alertas

print(f"✅ Entidade EconomiaBairro limpa e otimizada.")