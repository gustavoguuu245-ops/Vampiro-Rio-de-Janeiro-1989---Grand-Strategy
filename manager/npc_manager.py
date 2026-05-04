import random
import json
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime


from entities.clans import CLANS_DB
from entities.arquetipos import ARQUETIPOS
from entities.qualidades import MERITS, FLAWS


# ============================================================================
# CONSTANTES E CONFIGURAÇÕES
# ============================================================================

class TierNPC(Enum):
    ELITE = "elite"           # 20 NPCs - Príncipes inimigos, Senescal, Xerife, Harpias
    CORTE = "corte"           # 80 NPCs - Membros do conselho, conspiradores
    NEOFITO = "neofito"       # 180 NPCs - Soldados, jovens, recrutáveis
    ERRANTE = "errante"       # 40 NPCs - Vampiros sem corte, mercenários, recrutáveis

class StatusVampiro(Enum):
    ATIVO = "ativo"
    MORTO = "morto"           # Final death
    DORMINDO = "dormindo"     # Torpor prolongado
    ERRANTE = "errante"       # Sem corte, vagando
    PRISIONEIRO = "prisioneiro"
    BLOOD_HUNT = "blood_hunt" # Sendo caçado

# Distribuição dos 320 NPCs
DISTRIBUICAO_NPCS = {
    TierNPC.ELITE: 20,
    TierNPC.CORTE: 80,
    TierNPC.NEOFITO: 180,
    TierNPC.ERRANTE: 40
}

# Nomes temáticos para Rio 1989
NOMES_MASCULINOS = [
    "Antônio", "Carlos", "Fernando", "João", "José", "Luís", "Marcelo", "Pedro", 
    "Ricardo", "Roberto", "Alexandre", "Bruno", "César", "Daniel", "Eduardo",
    "Felipe", "Gabriel", "Henrique", "Igor", "Juliano", "Lucas", "Mateus",
    "Nicolau", "Otávio", "Paulo", "Rafael", "Samuel", "Tiago", "Vicente",
    "Adriano", "Bernardo", "Caio", "Diego", "Érico", "Fabiano", "Gustavo",
    "Hugo", "Inácio", "Jorge", "Kleber", "Leonardo", "Márcio", "Norberto",
    "Orlando", "Patrick", "Quintino", "Rodrigo", "Sérgio", "Tadeu", "Ulisses"
]

NOMES_FEMININOS = [
    "Ana", "Beatriz", "Carolina", "Daniela", "Elena", "Fernanda", "Gabriela",
    "Helena", "Isabela", "Juliana", "Karina", "Larissa", "Mariana", "Natália",
    "Olívia", "Patrícia", "Quintina", "Raquel", "Sofia", "Tatiana", "Valentina",
    "Amanda", "Bianca", "Camila", "Débora", "Elisa", "Flávia", "Giovanna",
    "Heloísa", "Ingrid", "Jéssica", "Karen", "Lorena", "Melissa", "Nina",
    "Priscila", "Renata", "Sabrina", "Thaís", "Vitória", "Yasmin", "Zara",
    "Adriana", "Bruna", "Cristina", "Diana", "Esther", "Fabiana", "Giselle"
]

SOBRENOMES_TRADICIONAIS = [
    # Famílias tradicionais cariocas
    "Albuquerque", "Andrade", "Azevedo", "Barbosa", "Barros", "Batista", "Borges",
    "Braga", "Campos", "Cardoso", "Carvalho", "Castro", "Coelho", "Costa", "Cruz",
    "Dias", "Duarte", "Fernandes", "Ferreira", "Figueiredo", "Freitas", "Frota",
    "Garcia", "Gomes", "Gonçalves", "Guimarães", "Lima", "Lopes", "Machado",
    "Marques", "Martins", "Mendes", "Monteiro", "Moraes", "Moreira", "Moura",
    "Nascimento", "Neves", "Nogueira", "Oliveira", "Pereira", "Pinto", "Pires",
    "Ramos", "Reis", "Ribeiro", "Rocha", "Rodrigues", "Santana", "Santos",
    "Silva", "Silveira", "Sousa", "Souza", "Teixeira", "Vieira", "Xavier",
    # Sobrenomes aristocráticos/nobres
    "Aguiar", "Alencar", "Almeida", "Alves", "Amaral", "Araújo", "Azevedo",
    "Bittencourt", "Cabral", "Cavalcanti", "Correia", "Coutinho", "Diniz",
    "Fonseca", "Franco", "Leite", "Lobo", "Maia", "Medeiros", "Melo",
    "Mendonça", "Mesquita", "Neto", "Nóbrega", "Novaes", "Peixoto", "Pimentel",
    "Pinto", "Pires", "Porto", "Queiroz", "Ramalho", "Rangel", "Sales",
    "Sampaio", "Siqueira", "Tavares", "Torres", "Vasconcelos", "Viana", "Xavier"
]

SOBRENOMES_CLAN = {
    "Ventrue": ["von Habsburg", "de Bourbon", "Romanov", "von Hohenzollern", "de Bragança"],
    "Toreador": ["de Medici", "Borgia", "Sforza", "Visconti", "d'Este"],
    "Tremere": ["Kreiger", "von Stroheim", "Eichmann", "Schwarz", "Weiss"],
    "Nosferatu": ["das Sombras", "do Esgoto", "debaixo da Ponte", "das Ruínas", "do Breu"],
    "Brujah": ["Marcone", "O'Banion", "Kowalski", "Kowalczyk", "Moretti"],
    "Gangrel": ["Selvagem", "da Mata", "do Lobo", "das Sombras", "Errante"],
    "Malkaviano": ["o Louco", "o Visionário", "o Profeta", "o Caolho", "o Desordeiro"],
    "Lasombra": ["de Castilla", "de Aragón", "de León", "de Navarra", "de Granada"],
    "Tzimisce": ["Varkony", "Dragomir", "Vladescu", "Craioveanu", "Bathory"],
    "Assamita": ["ibn Jibran", "al-Farabi", "al-Rashid", "ibn Sina", "al-Ghazali"],
    "Setita": ["al-Sabbah", "al-Mualim", "al-Hakim", "al-Farouk", "al-Rashid"],
    "Giovanni": ["di Venezia", "di Napoli", "di Milano", "di Roma", "di Firenze"],
    "Ravnos": ["Romani", "Vlach", "Sinti", "Yenish", "Dom"],
    "Capadócio": ["de Montserrat", "de Montalembert", "de Châteaubriand", "de Tocqueville", "de Lamartine"]
}

# ============================================================================
# CLASSE PRINCIPAL: NPC
# ============================================================================

@dataclass
class NPC:
    """
    Ficha completa de um vampiro NPC no sistema de 320.
    Cada NPC tem Natureza + Comportamento (2 arquétipos), Clã, Qualidades e Defeitos.
    """
    id: int
    nome: str
    genero: str  # "M" ou "F"
    clan_nome: str
    
    # Arquétipos duplos (obrigatório)
    natureza: str      # Quem ele é de verdade
    comportamento: str # Como ele age
    
    # Tier e Status
    tier: TierNPC
    status: StatusVampiro = StatusVampiro.ATIVO
    
    # Localização
    bairro_atual: Optional[str] = None
    corte_vinculada: Optional[str] = None  # Nome da corte/príncipe
    
    # Atributos (simplificados para performance em massa)
    atributos: Dict[str, int] = field(default_factory=dict)
    
    # Disciplinas do clã
    disciplinas: Dict[str, int] = field(default_factory=dict)
    
    # Qualidades e Defeitos (Merits/Flaws)
    merits: List[str] = field(default_factory=list)
    flaws: List[str] = field(default_factory=list)
    
    # Vida útil
    geracao: int = 12
    idade_vampiro: int = 5
    sangue_atual: int = 5
    sangue_max: int = 10
    
    # Metadados
    data_criacao: str = field(default_factory=lambda: datetime.now().isoformat())
    historia: List[str] = field(default_factory=list)
    
    # Relacionamentos (cache para performance)
    lealdade_base: int = 5
    ambicao_base: int = 5
    
    def __post_init__(self):
        """Inicializa atributos derivados após criação"""
        if not self.atributos:
            self._gerar_atributos()
        if not self.disciplinas:
            self._gerar_disciplinas()
        self._calcular_personalidade()
    
    def _gerar_atributos(self):
        """Distribui atributos baseado nos arquétipos"""
        # Base 1 em tudo
        self.atributos = {
            "forca": 1, "destreza": 1, "vigor": 1,
            "carisma": 1, "manipulacao": 1, "aparencia": 1,
            "percepcao": 1, "inteligencia": 1, "raciocinio": 1
        }
        
        # Distribui pontos baseado nos arquétipos (7/5/3 simplificado)
        pontos_por_tier = {
            TierNPC.ELITE: 15,
            TierNPC.CORTE: 10,
            TierNPC.NEOFITO: 6,
            TierNPC.ERRANTE: 5
        }
        
        pontos = pontos_por_tier.get(self.tier, 5)
        
        # Natureza define prioridade de categoria
        natureza_info = ARQUETIPOS.get(self.natureza, {})
        bonus = natureza_info.get("bonus", {})
        
        # Determina categoria prioritária baseada na natureza
        categorias_prioridade = self._determinar_categorias_prioridade()
        
        # Distribui pontos
        for _ in range(pontos):
            cat = random.choice(categorias_prioridade)
            atributos_cat = self._get_atributos_da_categoria(cat)
            attr = random.choice(atributos_cat)
            if self.atributos[attr] < 5:
                self.atributos[attr] += 1
        
        # Aplica bônus dos arquétipos
        for attr, val in bonus.items():
            attr_lower = attr.lower().replace("_", "")
            if attr_lower in self.atributos:
                self.atributos[attr_lower] = min(5, self.atributos[attr_lower] + val)
    
    def _determinar_categorias_prioridade(self) -> List[str]:
        """Determina quais categorias de atributos priorizar baseado nos arquétipos"""
        # Mapeamento de arquétipos para categorias
        mapa_arquetipo_categoria = {
            # Físicos
            "Valentão": "fisicos", "Competidor": "fisicos", "Sobrevivente": "fisicos",
            "Mártir": "fisicos", "Monstro": "fisicos", "Masoquista": "fisicos",
            # Sociais
            "Autocrata": "sociais", "Bon Vivant": "sociais", "Celebrante": "sociais",
            "Galante": "sociais", "Gozador": "sociais", "Malandro": "sociais",
            "Filantropo": "sociais", "Pedagogo": "sociais", "Penitente": "sociais",
            # Mentais
            "Juiz": "mentais", "Perfeccionista": "mentais", "Visionário": "mentais",
            "Excêntrico": "mentais", "Cientista": "mentais", "Inovador": "mentais",
            "Tradicionalista": "mentais", "Ranzinza": "mentais", "Solitário": "mentais",
            # Misto
            "Fanático": "sociais", "Rebelde": "fisicos", "Conformista": "sociais",
            "Diretor": "mentais", "Esperto": "mentais", "Tradicionalista": "mentais"
        }
        
        cat_natureza = mapa_arquetipo_categoria.get(self.natureza, "sociais")
        cat_comportamento = mapa_arquetipo_categoria.get(self.comportamento, "sociais")
        
        # Cria lista ponderada
        categorias = [cat_natureza] * 3 + [cat_comportamento] * 2 + ["fisicos", "sociais", "mentais"]
        return categorias
    
    def _get_atributos_da_categoria(self, categoria: str) -> List[str]:
        """Retorna atributos de uma categoria"""
        mapa = {
            "fisicos": ["forca", "destreza", "vigor"],
            "sociais": ["carisma", "manipulacao", "aparencia"],
            "mentais": ["percepcao", "inteligencia", "raciocinio"]
        }
        return mapa.get(categoria, ["forca", "carisma", "inteligencia"])
    
    def _gerar_disciplinas(self):
        """Gera disciplinas do clã"""
        info_cla = CLANS_DB.get(self.clan_nome, {})
        disc_cla = info_cla.get("disciplinas", ["Potência"])
        
        # Nível base por tier
        nivel_base = {
            TierNPC.ELITE: 3,
            TierNPC.CORTE: 2,
            TierNPC.NEOFITO: 1,
            TierNPC.ERRANTE: 1
        }.get(self.tier, 1)
        
        self.disciplinas = {}
        for d in disc_cla:
            # Variação de nível
            variacao = random.randint(-1, 2)
            nivel = max(0, min(5, nivel_base + variacao))
            self.disciplinas[d] = nivel
    
    def _calcular_personalidade(self):
        """Calcula lealdade e ambição baseado nos arquétipos"""
        natureza_info = ARQUETIPOS.get(self.natureza, {})
        
        # Base
        self.lealdade_base = 5
        self.ambicao_base = 5
        
        # Modificadores por natureza
        naturezas_leais = ["Defensor", "Penitente", "Filantropo", "Mártir", "Fanático", "Tradicionalista"]
        naturezas_ambiciosas = ["Tirano", "Monstro", "Autocrata", "Malandro", "Competidor", "Rebelde"]
        
        if self.natureza in naturezas_leais:
            self.lealdade_base += random.randint(1, 3)
        elif self.natureza in naturezas_ambiciosas:
            self.ambicao_base += random.randint(1, 3)
        
        # Qualidades e defeitos afetam
        for merit in self.merits:
            if "Lealdade" in merit or "Honra" in merit:
                self.lealdade_base += 1
            if "Ambição" in merit or "Liderança" in merit:
                self.ambicao_base += 1
        
        for flaw in self.flaws:
            if "Vontade Fraca" in flaw:
                self.lealdade_base -= 2
            if "Vingança" in flaw:
                self.ambicao_base += 2
        
        # Limita ranges
        self.lealdade_base = max(1, min(10, self.lealdade_base))
        self.ambicao_base = max(1, min(10, self.ambicao_base))
    
    def calcular_poder_total(self) -> int:
        """Calcula poder político/combático total"""
        poder_attr = sum(self.atributos.values())
        poder_disc = sum(self.disciplinas.values()) * 2
        poder_tier = {
            TierNPC.ELITE: 10,
            TierNPC.CORTE: 5,
            TierNPC.NEOFITO: 2,
            TierNPC.ERRANTE: 1
        }.get(self.tier, 0)
        
        return poder_attr + poder_disc + poder_tier
    
    def get_descricao_personalidade(self) -> str:
        """Retorna descrição narrativa da personalidade"""
        return f"{self.nome} é {self.natureza.lower()} por natureza, mas age como {self.comportamento.lower()}."
    
    def to_dict(self) -> dict:
        """Serializa para dicionário"""
        return {
            "id": self.id,
            "nome": self.nome,
            "genero": self.genero,
            "clan": self.clan_nome,
            "natureza": self.natureza,
            "comportamento": self.comportamento,
            "tier": self.tier.value,
            "status": self.status.value,
            "bairro": self.bairro_atual,
            "atributos": self.atributos,
            "disciplinas": self.disciplinas,
            "merits": self.merits,
            "flaws": self.flaws,
            "lealdade": self.lealdade_base,
            "ambicao": self.ambicao_base,
            "poder": self.calcular_poder_total()
        }

# ============================================================================
# GERENCIADOR GLOBAL DE NPCs
# ============================================================================

class NPCManager:
    """
    Gerencia os 320 NPCs do jogo.
    Responsável por criação, recrutamento, morte e reposição.
    """
    
    def __init__(self):
        self.npcs: Dict[int, NPC] = {}
        self.id_counter = 0
        
        # Índices para busca rápida
        self.por_clan: Dict[str, Set[int]] = {clan: set() for clan in CLANS_DB.keys()}
        self.por_tier: Dict[TierNPC, Set[int]] = {tier: set() for tier in TierNPC}
        self.por_bairro: Dict[str, Set[int]] = {}
        self.por_corte: Dict[str, Set[int]] = {}
        self.errantes: Set[int] = set()
        
        # Contadores para manter o equilíbrio
        self.meta_populacao = DISTRIBUICAO_NPCS.copy()
        self.mortos_historico: List[int] = []
        
    # ===================================================================
    # MÉTODOS DE INICIALIZAÇÃO
    # ===================================================================
    
    def inicializar_mundo(self, bairros: List[str]):
        """Cria os 320 NPCs iniciais do mundo"""
        print("🌎 Inicializando mundo com 320 vampiros...")
        
        # 1. CRIA ELITE (20 NPCs)
        # Príncipes inimigos, Senescal, Xerife, Harpias importantes
        self._criar_elite(bairros)
        
        # 2. CRIA CORTE (80 NPCs)
        # Membros de cortes, primogênitos, conselheiros
        self._criar_corte(bairros)
        
        # 3. CRIA NEÓFITOS (180 NPCs)
        # Soldados, jovens, recrutáveis
        self._criar_neofitos(bairros)
        
        # 4. CRIA ERRANTES (40 NPCs)
        # Sem corte, disponíveis para recrutamento
        self._criar_errantes(bairros)
        
        print(f"✅ Mundo criado: {len(self.npcs)} vampiros ativos")
        self._print_resumo()
    
    def _criar_elite(self, bairros: List[str]):
        """Cria 20 NPCs de elite (Príncipes inimigos, cargos importantes)"""
        clans_list = list(CLANS_DB.keys())
        
        for i in range(DISTRIBUICAO_NPCS[TierNPC.ELITE]):
            # Elite tem clãs variados
            clan = random.choice(clans_list)
            
            # Naturezas mais fortes para elite
            naturezas_fortes = ["Autocrata", "Tirano", "Visionário", "Juiz", 
                              "Competidor", "Tradicionalista", "Fanático"]
            natureza = random.choice(naturezas_fortes)
            comportamento = random.choice(list(ARQUETIPOS.keys()))
            
            npc = self._criar_npc(
                tier=TierNPC.ELITE,
                clan=clan,
                natureza=natureza,
                comportamento=comportamento,
                bairro=random.choice(bairros) if bairros else None
            )
            
            # Elite tem mais qualidades
            npc.merits = self._sortear_merits(2, 4)
            npc.flaws = self._sortear_flaws(0, 2)
            
            # Geração mais baixa (mais poderosa)
            npc.geracao = random.choice([8, 9, 10, 11])
            npc.idade_vampiro = random.randint(50, 300)
    
    def _criar_corte(self, bairros: List[str]):
        """Cria 80 NPCs de corte (membros políticos)"""
        for i in range(DISTRIBUICAO_NPCS[TierNPC.CORTE]):
            clan = random.choice(list(CLANS_DB.keys()))
            
            # Naturezas políticas
            naturezas_politicas = ["Autocrata", "Conformista", "Diretor", "Malandro",
                                 "Juiz", "Tradicionalista", "Conspirador"]
            natureza = random.choice(naturezas_politicas + list(ARQUETIPOS.keys()))
            comportamento = random.choice(list(ARQUETIPOS.keys()))
            
            npc = self._criar_npc(
                tier=TierNPC.CORTE,
                clan=clan,
                natureza=natureza,
                comportamento=comportamento,
                bairro=random.choice(bairros) if bairros else None
            )
            
            npc.merits = self._sortear_merits(1, 3)
            npc.flaws = self._sortear_flaws(1, 2)
            npc.geracao = random.choice([10, 11, 12])
            npc.idade_vampiro = random.randint(10, 100)
    
    def _criar_neofitos(self, bairros: List[str]):
        """Cria 180 NPCs neófitos (massa, soldados)"""
        for i in range(DISTRIBUICAO_NPCS[TierNPC.NEOFITO]):
            clan = random.choice(list(CLANS_DB.keys()))
            
            natureza = random.choice(list(ARQUETIPOS.keys()))
            comportamento = random.choice(list(ARQUETIPOS.keys()))
            
            npc = self._criar_npc(
                tier=TierNPC.NEOFITO,
                clan=clan,
                natureza=natureza,
                comportamento=comportamento,
                bairro=random.choice(bairros) if bairros else None
            )
            
            npc.merits = self._sortear_merits(0, 2)
            npc.flaws = self._sortear_flaws(1, 3)
            npc.geracao = random.choice([12, 13])
            npc.idade_vampiro = random.randint(1, 20)
    
    def _criar_errantes(self, bairros: List[str]):
        """Cria 40 NPCs errantes (sem corte, recrutáveis)"""
        for i in range(DISTRIBUICAO_NPCS[TierNPC.ERRANTE]):
            clan = random.choice(list(CLANS_DB.keys()))
            
            # Errantes tendem a naturezas solitárias
            naturezas_sol = ["Sobrevivente", "Solitário", "Rebelde", "Esperto", 
                           "Sobrevivente", "Excêntrico"]
            natureza = random.choice(naturezas_sol + list(ARQUETIPOS.keys()))
            comportamento = random.choice(list(ARQUETIPOS.keys()))
            
            npc = self._criar_npc(
                tier=TierNPC.ERRANTE,
                clan=clan,
                natureza=natureza,
                comportamento=comportamento,
                bairro=random.choice(bairros) if bairros else None
            )
            
            npc.status = StatusVampiro.ERRANTE
            npc.merits = self._sortear_merits(0, 2)
            npc.flaws = self._sortear_flaws(1, 3)
            npc.geracao = random.choice([11, 12, 13])
            npc.idade_vampiro = random.randint(1, 50)
            
            self.errantes.add(npc.id)
    
    def _criar_npc(self, tier: TierNPC, clan: str, natureza: str, 
                   comportamento: str, bairro: Optional[str] = None) -> NPC:
        """Factory method para criar um NPC"""
        self.id_counter += 1
        
        # Gera nome
        genero = random.choice(["M", "F"])
        nome = self._gerar_nome(clan, genero)
        
        # Cria NPC
        npc = NPC(
            id=self.id_counter,
            nome=nome,
            genero=genero,
            clan_nome=clan,
            natureza=natureza,
            comportamento=comportamento,
            tier=tier,
            bairro_atual=bairro
        )
        
        # Indexa
        self.npcs[npc.id] = npc
        self.por_clan[clan].add(npc.id)
        self.por_tier[tier].add(npc.id)
        
        if bairro:
            if bairro not in self.por_bairro:
                self.por_bairro[bairro] = set()
            self.por_bairro[bairro].add(npc.id)
        
        return npc
    
    # ===================================================================
    # MÉTODOS DE GERAÇÃO ALEATÓRIA
    # ===================================================================
    
    def _gerar_nome(self, clan: str, genero: str) -> str:
        """Gera nome temático baseado no clã"""
        nomes = NOMES_MASCULINOS if genero == "M" else NOMES_FEMININOS
        nome = random.choice(nomes)
        
        # 30% de chance de usar sobrenome do clã
        if random.random() < 0.3 and clan in SOBRENOMES_CLAN:
            sobrenome = random.choice(SOBRENOMES_CLAN[clan])
        else:
            sobrenome = random.choice(SOBRENOMES_TRADICIONAIS)
        
        return f"{nome} {sobrenome}"
    
    def _sortear_merits(self, min_qtd: int, max_qtd: int) -> List[str]:
        """Sorteia qualidades (Merits)"""
        qtd = random.randint(min_qtd, max_qtd)
        disponiveis = list(MERITS.keys())
        if qtd >= len(disponiveis):
            return disponiveis
        return random.sample(disponiveis, qtd)
    
    def _sortear_flaws(self, min_qtd: int, max_qtd: int) -> List[str]:
        """Sorteia defeitos (Flaws)"""
        qtd = random.randint(min_qtd, max_qtd)
        disponiveis = list(FLAWS.keys())
        if qtd >= len(disponiveis):
            return disponiveis
        return random.sample(disponiveis, qtd)
    
    # ===================================================================
    # SISTEMA DE RECRUTAMENTO (A "FILA DE ESPERA")
    # ===================================================================
    
    def buscar_errantes_para_recutamento(self, 
                                         bairro: str, 
                                         filtro_clan: Optional[str] = None,
                                         min_poder: int = 0) -> List[NPC]:
        """
        Busca vampiros errantes disponíveis para recrutamento em um bairro.
        Usado quando o jogador quer contratar um novo membro para a corte.
        """
        disponiveis = []
        
        for npc_id in self.errantes:
            npc = self.npcs[npc_id]
            
            # Filtros
            if filtro_clan and npc.clan_nome != filtro_clan:
                continue
            if npc.calcular_poder_total() < min_poder:
                continue
            if npc.bairro_atual != bairro:
                continue
            
            disponiveis.append(npc)
        
        # Ordena por poder (mais fortes primeiro)
        disponiveis.sort(key=lambda x: x.calcular_poder_total(), reverse=True)
        return disponiveis
    
    def recrutar_errante(self, npc_id: int, corte_nome: str, 
                        novo_tier: TierNPC = TierNPC.NEOFITO) -> Optional[NPC]:
        """
        Recruta um errante para uma corte.
        Retorna o NPC atualizado ou None se falhar.
        """
        if npc_id not in self.npcs:
            return None
        
        npc = self.npcs[npc_id]
        
        if npc.status != StatusVampiro.ERRANTE:
            print(f"❌ {npc.nome} não está disponível para recrutamento")
            return None
        
        # Atualiza status
        npc.status = StatusVampiro.ATIVO
        npc.corte_vinculada = corte_nome
        npc.tier = novo_tier
        
        # Remove de errantes
        self.errantes.discard(npc_id)
        
        # Adiciona à corte
        if corte_nome not in self.por_corte:
            self.por_corte[corte_nome] = set()
        self.por_corte[corte_nome].add(npc_id)
        
        # Recalcula personalidade (agora tem lealdade à corte)
        npc.lealdade_base += random.randint(1, 3)
        npc.historia.append(f"Recrutado por {corte_nome} em {datetime.now().year}")
        
        print(f"✅ {npc.nome} ({npc.clan_nome}) recrutado para {corte_nome}")
        return npc
    
    def gerar_errante_aleatorio(self, bairro: str) -> NPC:
        """
        Gera um novo errante aleatório (para reposição).
        Usado quando a população de errantes cai muito.
        """
        clan = random.choice(list(CLANS_DB.keys()))
        natureza = random.choice(list(ARQUETIPOS.keys()))
        comportamento = random.choice(list(ARQUETIPOS.keys()))
        
        npc = self._criar_npc(
            tier=TierNPC.ERRANTE,
            clan=clan,
            natureza=natureza,
            comportamento=comportamento,
            bairro=bairro
        )
        
        npc.status = StatusVampiro.ERRANTE
        self.errantes.add(npc.id)
        
        print(f"🆕 Novo errante surgido: {npc.nome} ({npc.clan_nome}) em {bairro}")
        return npc
    
    # ===================================================================
    # SISTEMA DE MORTE E REPOSIÇÃO
    # ===================================================================
    
    def matar_npc(self, npc_id: int, motivo: str = "Morte em combate") -> bool:
        """
        Marca um NPC como morto (Final Death).
        Aciona reposição automática se necessário.
        """
        if npc_id not in self.npcs:
            return False
        
        npc = self.npcs[npc_id]
        tier_anterior = npc.tier
        
        # Atualiza status
        npc.status = StatusVampiro.MORTO
        npc.historia.append(f"Morte: {motivo}")
        
        # Remove dos índices
        self.por_clan[npc.clan_nome].discard(npc_id)
        self.por_tier[tier_anterior].discard(npc_id)
        if npc.bairro_atual and npc.bairro_atual in self.por_bairro:
            self.por_bairro[npc.bairro_atual].discard(npc_id)
        if npc.corte_vinculada and npc.corte_vinculada in self.por_corte:
            self.por_corte[npc.corte_vinculada].discard(npc_id)
        self.errantes.discard(npc_id)
        
        self.mortos_historico.append(npc_id)
        
        print(f"☠️ {npc.nome} ({npc.clan_nome}) - {motivo}")
        
        # Verifica necessidade de reposição
        self._verificar_reposicao(tier_anterior)
        
        return True
    
    def _verificar_reposicao(self, tier: TierNPC):
        """Verifica se precisa criar novo NPC para manter equilíbrio"""
        atual = len(self.por_tier[tier])
        meta = self.meta_populacao[tier]
        
        if atual < meta:
            # Cria reposição
            if tier == TierNPC.ERRANTE:
                bairros_disponiveis = list(self.por_bairro.keys()) or ["Centro"]
                self.gerar_errante_aleatorio(random.choice(bairros_disponiveis))
            else:
                # Para outros tiers, cria neófito
                bairros_disponiveis = list(self.por_bairro.keys()) or ["Centro"]
                clan = random.choice(list(CLANS_DB.keys()))
                natureza = random.choice(list(ARQUETIPOS.keys()))
                comportamento = random.choice(list(ARQUETIPOS.keys()))
                
                novo = self._criar_npc(
                    tier=tier,
                    clan=clan,
                    natureza=natureza,
                    comportamento=comportamento,
                    bairro=random.choice(bairros_disponiveis)
                )
                print(f"🆕 Reposição: {novo.nome} ({novo.clan_nome}) - Tier {tier.value}")
    
    def transformar_em_errante(self, npc_id: int, motivo: str = "Corte destruída") -> bool:
        """
        Transforma um NPC em errante (quando perde a corte).
        """
        if npc_id not in self.npcs:
            return False
        
        npc = self.npcs[npc_id]
        
        # Remove da corte anterior
        if npc.corte_vinculada and npc.corte_vinculada in self.por_corte:
            self.por_corte[npc.corte_vinculada].discard(npc_id)
        
        npc.corte_vinculada = None
        npc.status = StatusVampiro.ERRANTE
        npc.tier = TierNPC.ERRANTE
        npc.lealdade_base = max(1, npc.lealdade_base - 3)  # Perde lealdade
        npc.historia.append(f"Tornou-se errante: {motivo}")
        
        self.errantes.add(npc_id)
        
        print(f"🏃 {npc.nome} agora é um errante ({motivo})")
        return True
    
    # ===================================================================
    # MÉTODOS DE CONSULTA E BUSCA
    # ===================================================================
    
    def get_npc(self, npc_id: int) -> Optional[NPC]:
        """Retorna NPC por ID"""
        return self.npcs.get(npc_id)
    
    def get_por_clan(self, clan: str, apenas_ativos: bool = True) -> List[NPC]:
        """Retorna todos os NPCs de um clã"""
        resultado = []
        for npc_id in self.por_clan.get(clan, []):
            npc = self.npcs[npc_id]
            if not apenas_ativos or npc.status == StatusVampiro.ATIVO:
                resultado.append(npc)
        return resultado
    
    def get_por_bairro(self, bairro: str, apenas_ativos: bool = True) -> List[NPC]:
        """Retorna todos os NPCs em um bairro"""
        resultado = []
        for npc_id in self.por_bairro.get(bairro, []):
            npc = self.npcs[npc_id]
            if not apenas_ativos or npc.status == StatusVampiro.ATIVO:
                resultado.append(npc)
        return resultado
    
    def get_elite_disponivel(self) -> List[NPC]:
        """Retorna NPCs de elite para serem Príncipes inimigos"""
        elite = []
        for npc_id in self.por_tier[TierNPC.ELITE]:
            npc = self.npcs[npc_id]
            if npc.status == StatusVampiro.ATIVO and not npc.corte_vinculada:
                elite.append(npc)
        return elite
    
    def buscar_por_arquetipo(self, arquetipo: str) -> List[NPC]:
        """Busca NPCs por natureza ou comportamento"""
        resultado = []
        for npc in self.npcs.values():
            if npc.natureza == arquetipo or npc.comportamento == arquetipo:
                resultado.append(npc)
        return resultado
    
    def buscar_traidores_potenciais(self, corte_nome: str) -> List[NPC]:
        """
        Identifica NPCs em uma corte que podem trair.
        Baseado em: ambição > lealdade, natureza ambiciosa, etc.
        """
        traidores = []
        for npc_id in self.por_corte.get(corte_nome, []):
            npc = self.npcs[npc_id]
            
            # Critérios de traição
            if npc.ambicao_base > npc.lealdade_base + 2:
                traidores.append((npc, "Ambição supera lealdade"))
            elif npc.natureza in ["Tirano", "Monstro", "Malandro"] and npc.lealdade_base < 4:
                traidores.append((npc, f"Natureza {npc.natureza} com baixa lealdade"))
            elif "Vingança" in npc.flaws:
                traidores.append((npc, "Obsessão vingativa"))
        
        return traidores
    
    # ===================================================================
    # MÉTODOS DE PERSISTÊNCIA
    # ===================================================================
    
    def salvar(self, filepath: str = "saves/npcs.json"):
        """Salva estado atual em JSON"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        data = {
            "contador_id": self.id_counter,
            "npcs": {str(k): v.to_dict() for k, v in self.npcs.items()},
            "mortos": self.mortos_historico
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Estado salvo em {filepath}")
    
    def carregar(self, filepath: str = "saves/npcs.json"):
        """Carrega estado de JSON"""
        import os
        if not os.path.exists(filepath):
            print(f"⚠️ Arquivo {filepath} não encontrado")
            return False
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.id_counter = data.get("contador_id", 0)
        self.mortos_historico = data.get("mortos", [])
        
        # Reconstrói NPCs
        for npc_id, npc_data in data.get("npcs", {}).items():
            npc = NPC(
                id=int(npc_id),
                nome=npc_data["nome"],
                genero=npc_data["genero"],
                clan_nome=npc_data["clan"],
                natureza=npc_data["natureza"],
                comportamento=npc_data["comportamento"],
                tier=TierNPC(npc_data["tier"]),
                status=StatusVampiro(npc_data["status"]),
                bairro_atual=npc_data.get("bairro"),
                atributos=npc_data.get("atributos", {}),
                disciplinas=npc_data.get("disciplinas", {}),
                merits=npc_data.get("merits", []),
                flaws=npc_data.get("flaws", []),
                lealdade_base=npc_data.get("lealdade", 5),
                ambicao_base=npc_data.get("ambicao", 5)
            )
            self.npcs[int(npc_id)] = npc
        
        # Reconstrói índices
        self._reconstruir_indices()
        
        print(f"📂 Estado carregado: {len(self.npcs)} NPCs")
        return True
    
    def _reconstruir_indices(self):
        """Reconstrói índices após carregamento"""
        self.por_clan = {clan: set() for clan in CLANS_DB.keys()}
        self.por_tier = {tier: set() for tier in TierNPC}
        self.por_bairro = {}
        self.por_corte = {}
        self.errantes = set()
        
        for npc in self.npcs.values():
            self.por_clan[npc.clan_nome].add(npc.id)
            self.por_tier[npc.tier].add(npc.id)
            
            if npc.bairro_atual:
                if npc.bairro_atual not in self.por_bairro:
                    self.por_bairro[npc.bairro_atual] = set()
                self.por_bairro[npc.bairro_atual].add(npc.id)
            
            if npc.corte_vinculada:
                if npc.corte_vinculada not in self.por_corte:
                    self.por_corte[npc.corte_vinculada] = set()
                self.por_corte[npc.corte_vinculada].add(npc.id)
            
            if npc.status == StatusVampiro.ERRANTE:
                self.errantes.add(npc.id)
    
    # ===================================================================
    # MÉTODOS DE DEBUG E RELATÓRIOS
    # ===================================================================
    
    def _print_resumo(self):
        """Printa resumo da população"""
        print("\n📊 RESUMO DA POPULAÇÃO:")
        for tier in TierNPC:
            count = len(self.por_tier[tier])
            meta = self.meta_populacao[tier]
            status = "✅" if count >= meta else "⚠️"
            print(f"   {status} {tier.value.upper()}: {count}/{meta}")
        
        print(f"\n   Total ativos: {len([n for n in self.npcs.values() if n.status != StatusVampiro.MORTO])}")
        print(f"   Total mortos: {len(self.mortos_historico)}")
        print(f"   Errantes disponíveis: {len(self.errantes)}")
    
    def gerar_relatorio_demografico(self) -> dict:
        """Gera relatório completo da população vampírica"""
        relatorio = {
            "total_npcs": len(self.npcs),
            "por_tier": {},
            "por_clan": {},
            "por_arquetipo": {},
            "media_poder": 0,
            "naturezas_comuns": [],
            "comportamentos_comuns": []
        }
        
        # Por tier
        for tier in TierNPC:
            ativos = [self.npcs[i] for i in self.por_tier[tier] 
                     if self.npcs[i].status != StatusVampiro.MORTO]
            relatorio["por_tier"][tier.value] = len(ativos)
        
        # Por clã
        for clan in CLANS_DB.keys():
            relatorio["por_clan"][clan] = len(self.por_clan[clan])
        
        # Naturezas e comportamentos
        naturezas = {}
        comportamentos = {}
        poder_total = 0
        
        for npc in self.npcs.values():
            if npc.status != StatusVampiro.MORTO:
                naturezas[npc.natureza] = naturezas.get(npc.natureza, 0) + 1
                comportamentos[npc.comportamento] = comportamentos.get(npc.comportamento, 0) + 1
                poder_total += npc.calcular_poder_total()
        
        relatorio["naturezas_comuns"] = sorted(naturezas.items(), key=lambda x: x[1], reverse=True)[:5]
        relatorio["comportamentos_comuns"] = sorted(comportamentos.items(), key=lambda x: x[1], reverse=True)[:5]
        relatorio["media_poder"] = poder_total / max(len(self.npcs), 1)
        
        return relatorio
    
    def print_exemplos(self, quantidade: int = 5):
        """Printa exemplos de NPCs gerados"""
        print(f"\n🧛 EXEMPLOS DE NPCs GERADOS:")
        print("=" * 80)
        
        amostra = random.sample(list(self.npcs.values()), min(quantidade, len(self.npcs)))
        
        for npc in amostra:
            print(f"\n🎭 {npc.nome} ({npc.clan_nome}) - {npc.tier.value.upper()}")
            print(f"   Gênero: {'♂' if npc.genero == 'M' else '♀'} | Geração: {npc.geracao}ª | Idade: {npc.idade_vampiro} anos")
            print(f"   Natureza: {npc.natureza} | Comportamento: {npc.comportamento}")
            print(f"   Lealdade: {npc.lealdade_base}/10 | Ambição: {npc.ambicao_base}/10")
            print(f"   Poder Total: {npc.calcular_poder_total()}")
            print(f"   Qualidades: {', '.join(npc.merits[:3]) if npc.merits else 'Nenhuma'}")
            print(f"   Defeitos: {', '.join(npc.flaws[:3]) if npc.flaws else 'Nenhum'}")
            print(f"   Disciplinas: {', '.join([f'{k}({v})' for k, v in list(npc.disciplinas.items())[:3]])}")
            print(f"   {npc.get_descricao_personalidade()}")

# ============================================================================
# FUNÇÃO DE TESTE
# ============================================================================

if __name__ == "__main__":
    print("🧛=== TESTE DO NPC MANAGER (320 Vampiros) ===🧛\\n")
    
    # Cria manager
    manager = NPCManager()
    
    # Inicializa com bairros do Rio
    bairros = [
        "Copacabana", "Ipanema", "Botafogo", "Centro", "Tijuca",
        "Madureira", "Bangu", "Campo Grande", "Santa Cruz", "Lapa",
        "Santa Teresa", "Castelo", "Ilha do Governador", "Méier"
    ]
    
    manager.initializar_mundo(bairros)
    
    # Mostra exemplos
    manager.print_exemplos(8)
    
    # Testa recrutamento
    print("\\n\\n🎯 TESTE DE RECRUTAMENTO:")
    errantes_copa = manager.buscar_errantes_para_recutamento("Copacabana")
    print(f"   Errantes em Copacabana: {len(errantes_copa)}")
    
    if errantes_copa:
        escolhido = errantes_copa[0]
        print(f"   Recrutando: {escolhido.nome} ({escolhido.clan_nome})")
        manager.recrutar_errante(escolhido.id, "Corte do Príncipe Jogador")
    
    # Relatório demográfico
    print("\\n📊 RELATÓRIO DEMOGRÁFICO:")
    rel = manager.gerar_relatorio_demografico()
    print(f"   Naturezas mais comuns: {rel['naturezas_comuns'][:3]}")
    print(f"   Comportamentos mais comuns: {rel['comportamentos_comuns'][:3]}")
    print(f"   Poder médio: {rel['media_poder']:.1f}")
    
    # Salva estado
    manager.salvar("saves/teste_npc_manager.json")
