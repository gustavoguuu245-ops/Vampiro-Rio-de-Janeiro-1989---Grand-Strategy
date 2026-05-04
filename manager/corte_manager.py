# corte_manager.py
import random
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from entities.clans import CLANS_DB
from entities.arquetipos import ARQUETIPOS
from entities.qualidades import MERITS, FLAWS


class CargoCorte(Enum):
    PRINCIPE = "principe"
    SENESCAL = "senescal"
    SHERIFF = "sheriff"
    HARPIA = "harpya"
    PRIMOGENITO = "primogenito"
    KEEPER_ELYSIUM = "keeper"
    CHILDE = "childe"
    MEMBRO = "membro"
    NEOFITO = "neofito"


class TipoRelacao(Enum):
    LEALDADE = "lealdade"
    AMBICAO = "ambicao"
    MEDO = "medo"
    RANCOR = "rancor"
    INVEJA = "inveja"
    LAÇO_SANGUE = "laco"

@dataclass
class PersonalidadeVampirica:
    natureza: str
    comportamento: str
    lealdade_base: int = 5
    ambicao_base: int = 5
    merits: List[str] = field(default_factory=list)
    flaws: List[str] = field(default_factory=list)
    nivel_genio: str = "Mediano"
    
    def verificar_traicao_potencial(self, situacao: dict) -> bool:
        """Verifica se o vampiro tem chance de trair baseado na lealdade e ambição"""
        # Se a lealdade for muito baixa e a ambição alta, há risco
        if self.lealdade_base < 3 and self.ambicao_base > 7:
            import random
            return random.randint(1, 10) < self.ambicao_base
        return False

    def calcular_lealdade_efetiva(self, fome: int = 0, humilhado: bool = False) -> int:
        lealdade = self.lealdade_base
        if fome > 5:
            lealdade -= 3
        if humilhado:
            lealdade -= 4
        return max(0, min(10, lealdade))


class MembroCorte:
    _id_counter = 0
    
    def calcular_poder_total(self) -> int:
        """Calcula o poder real somando base e cargo"""
        # Bônus simples por cargo
        bonus = {
            CargoCorte.SENESCAL: 15,
            CargoCorte.SHERIFF: 10,
            CargoCorte.HARPIA: 8,
            CargoCorte.PRIMOGENITO: 12
        }.get(self.cargo, 0)
        
        return self.poder_base + bonus

    def __init__(self, nome: str, cla: str, geracao: int = 12, idade_vampiro: int = 20, cargo: CargoCorte = CargoCorte.MEMBRO):
        MembroCorte._id_counter += 1
        self.id = MembroCorte._id_counter
        self.nome = nome
        self.cla = cla
        self.geracao = geracao
        self.idade_vampiro = idade_vampiro
        self.cargo = cargo

        self.status_social = 3
        self.sangue_atual = 8
        self.sangue_max = 10 + (13 - geracao)

        self.personalidade = self._gerar_personalidade()
        self.atributos = self._gerar_atributos()
        self.disciplinas = self._gerar_disciplinas()

    @property
    def clã(self):
        return self.cla

    @property
    def lealdade(self):
        return self.personalidade.lealdade_base * 10

    @property
    def poder_base(self):
        return sum(self.atributos.values()) + sum(self.disciplinas.values()) * 2 + self.status_social

    def _gerar_personalidade(self):
        # ... (mantive a lógica boa que você tinha, simplificada)
        natureza = random.choice(list(ARQUETIPOS.keys()))
        comportamento = random.choice(list(ARQUETIPOS.keys()))
        return PersonalidadeVampirica(natureza=natureza, comportamento=comportamento)
    
    def _gerar_atributos(self):
        # simplificado mas funcional
        return {"forca": 3, "destreza": 3, "vigor": 3, "carisma": 3, "manipulacao": 3, "inteligencia": 3}

    def _gerar_disciplinas(self):
        disc_cla = CLANS_DB.get(self.cla, {}).get("disciplinas", ["Potência"])
        return {d: random.randint(1, 3) for d in disc_cla[:3]}

    def modificar_status(self, valor: int, motivo: str):
        self.status_social = max(0, min(10, self.status_social + valor))

    def calcular_poder_total(self) -> int:
        """Calcula o poder do vampiro somando a base e o bônus do cargo"""
        bonus_cargos = {
            CargoCorte.SENESCAL: 15,
            CargoCorte.SHERIFF: 10,
            CargoCorte.HARPIA: 8,
            CargoCorte.PRIMOGENITO: 12
        }
        # Pega o bônus do cargo atual ou 0 se for membro comum
        bonus = bonus_cargos.get(self.cargo, 0)
        return self.poder_base + bonus

class CorteManager:
    def __init__(self, principe_nome: str, principe_cla: str):
        self.principe = principe_nome
        self.principe_cla = principe_cla
        self.turno_atual = 0
        self.corte_central: Dict[int, MembroCorte] = {}
        self.cargos_ocupados: Dict[CargoCorte, Optional[int]] = {}
        self.harpy_id: Optional[int] = None
        # eventos
    def evento_noite_de_caca(self):
        print("🩸 Noite de caça livre declarada!")
        # Aqui depois você bota a lógica de ganhar sangue

    def harpia_abafar_escandalo(self):
        print("🤫 A Harpia espalhou boatos e limpou sua barra.")

    def humilhar_publicamente(self):
        print("⚖️ Você deu um exemplo de autoridade.")

    def fundar_corte_inicial(self, npc_manager):
        """Cria 32 membros + define Primogênitos automaticamente"""
        print("🏛️ Fundando a Corte do Rio de Janeiro...")

        todos_clans = list(CLANS_DB.keys())
        for _ in range(32):
            cla = random.choice(todos_clans)
            idade = random.randint(10, 200)
            vamp = MembroCorte(f"{cla} {random.randint(100,999)}", cla, idade_vampiro=idade)
            self.corte_central[vamp.id] = vamp

        # Primogênitos automáticos (mais forte de cada clã, exceto do Príncipe)
        for cla in todos_clans:
            if cla == self.principe_cla:
                continue
            membros_cla = [v for v in self.corte_central.values() if v.cla == cla]
            if membros_cla:
                primogenito = max(membros_cla, key=lambda v: v.poder_base)
                primogenito.cargo = CargoCorte.PRIMOGENITO
                primogenito.status_social = 7

        print(f"✅ Corte criada com {len(self.corte_central)} vampiros.")


    def nomear_para_cargo(self, vampiro_id: int, novo_cargo: CargoCorte) -> Tuple[bool, str]:
        """Jogador escolhe quem ocupa o cargo (exceto Primogênito)"""
        vamp = self.corte_central.get(vampiro_id)
        if not vamp:
            return False, "Vampiro não encontrado"

        # Demite o anterior se for cargo único
        if novo_cargo in [CargoCorte.SENESCAL, CargoCorte.SHERIFF, CargoCorte.HARPIA, CargoCorte.KEEPER_ELYSIUM]:
            atual_id = self.cargos_ocupados.get(novo_cargo)
            if atual_id and atual_id != vampiro_id:
                antigo = self.corte_central[atual_id]
                antigo.cargo = CargoCorte.MEMBRO
                antigo.personalidade.lealdade_base -= 4  # rancor

        vamp.cargo = novo_cargo
        self.cargos_ocupados[novo_cargo] = vampiro_id

        if novo_cargo == CargoCorte.HARPIA:
            self.harpy_id = vampiro_id

        vamp.personalidade.lealdade_base += 2
        return True, f"{vamp.nome} agora é {novo_cargo.value.upper()}!"
    
    # --- MÉTODOS DE EVENTOS (Respostas às Escolhas) ---
    def evento_noite_de_caca(self):
        print("🩸 ORDEM DO PRÍNCIPE: Caça liberada! A reserva de sangue aumentou.")
        # Aqui você pode acessar o eco_manager futuramente

    def evento_primeiro_elysium(self):
        print("🏛️ ELYSIUM: O encontro foi um sucesso. A corte reconhece sua liderança.")
        # Dá um pequeno bônus de lealdade para todos os membros ativos
        for v in self.corte_central.values():
            v.personalidade.lealdade_base += 1

    def evento_investigar_anarquistas(self):
        # Verifica se o cargo de Sheriff está ocupado
        from manager.corte_manager import CargoCorte
        sheriff_id = self.cargos_ocupados.get(CargoCorte.SHERIFF)
        
        if sheriff_id:
            vamp = self.corte_central[sheriff_id]
            print(f"🕵️ SHERIFF {vamp.nome}: Investigação concluída. Célula anarquista localizada!")
        else:
            print("🕵️ SISTEMA: Como você não tem um Sheriff, seus carrascos pessoais fizeram o trabalho.")

    def harpia_abafar_escandalo(self):
        from manager.corte_manager import CargoCorte
        harpy_id = self.cargos_ocupados.get(CargoCorte.HARPIA)
        
        if harpy_id:
            print("🤫 HARPIA: Os jornais foram silenciados e o escândalo sumiu.")
        else:
            print("🤫 SISTEMA: Você não tem Harpia, mas subornou a mídia com seu próprio sangue.")
    # --- FUNÇÕES DE RESPOSTA À CRISE ---
    def evento_cacada_brutal(self, eco_manager):
        from manager.economia_manager import TipoRecurso
        eco_manager.reserva_central[TipoRecurso.SANGUE] += 20
        eco_manager.reserva_central[TipoRecurso.MASCARADA] -= 15
        print("🩸 Sangue restaurado com violência!")

    def evento_racionamento(self, eco_manager):
        for v in self.corte_central.values():
            v.personalidade.lealdade_base -= 2
        print("📉 Corte insatisfeita com o racionamento.")

    def evento_sacrificio_prisioneiro(self, eco_manager):
        from manager.economia_manager import TipoRecurso
        eco_manager.reserva_central[TipoRecurso.SANGUE] += 10
        eco_manager.reserva_central[TipoRecurso.MEDO] += 5
        print("💀 Medo espalhado na cidade.")

    def humilhar_publicamente(self):
        print("⚖️ AUTORIDADE: Você deu um exemplo de crueldade. Medo na corte +1.")
    
    def promover_ventrue_ao_conselho(self):
        # Lógica que discutimos: Procura um Ventrue aleatório e sobe ele
        print("🤝 DIPLOMACIA: Um novo Primogênito Ventrue foi nomeado. Lealdade do Clã +2.")

    def reforcar_autoridade(self):
        print("👑 PODER: Você ignorou os anciões. Medo +2.")
        
        # Procura qualquer Ventrue que seja apenas "Membro" ou "Neófito"
        vampiro_escolhido = None
        for v in self.corte_central.values():
            if v.cla == "Ventrue" and v.cargo in [CargoCorte.MEMBRO, CargoCorte.NEOFITO]:
                vampiro_escolhido = v
                break
        
        if vampiro_escolhido:
            vampiro_escolhido.cargo = CargoCorte.PRIMOGENITO
            vampiro_escolhido.personalidade.lealdade_base += 5 # Ele vira seu fã
            print(f"🤝 DIPLOMACIA: {vampiro_escolhido.nome} foi elevado a Primogênito Ventrue!")
            print("👑 O Clã Ventrue agora respeita sua sabedoria. Lealdade do Clã +2.")
            
            # Bônus para todos os outros Ventrue da corte
            for v in self.corte_central.values():
                if v.cla == "Ventrue":
                    v.personalidade.lealdade_base += 2
        else:
            print("⚠️ SISTEMA: Não há Ventrues disponíveis para promoção, mas você prometeu favores futuros.")    

    def get_membros_para_hud(self) -> List[Dict]:
        return [
            {
                "id": v.id,
                "nome": v.nome,
                "cla": v.cla,
                "cargo": v.cargo.value, # Pega o valor atual do Enum
                "lealdade": v.personalidade.lealdade_base, # Certifique-se de que o HUD usa essa chave
                "status": v.status_social
            }
            for v in self.corte_central.values()
        ]

    def processar_turno(self, eventos_mundo=None):
        """Processa a manutenção e intrigas da corte"""
        print("🏛️ Corte processando decisões da noite...")
        # Aqui você pode adicionar lógica futura de intrigas
        return [] # Retorna lista vazia de decisões por enquanto