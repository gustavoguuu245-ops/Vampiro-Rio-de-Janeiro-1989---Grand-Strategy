# entities/player.py
from entities.clans import CLANS_DB
from entities.arquetipos import ARQUETIPOS

class PersonagemVampiro:
    def __init__(self, nome, clan_nome, natureza, comportamento, genero, eh_jogador=False):
        self.nome = nome
        self.eh_jogador = eh_jogador
        self.clan_nome = clan_nome
        self.clan_info = CLANS_DB[clan_nome]
        self.natureza = ARQUETIPOS
        self.comportamento = ARQUETIPOS
        self.genero = genero  # "Masculino", "Feminino" ou "Indefinido"
        
        # --- ATRIBUTOS (Base 1) ---
        # Prioridades na criação: 7/5/3 pontos a distribuir
        self.atributos = {
            "Físicos": {"Força": 1, "Destreza": 1, "Vigor": 1},
            "Sociais": {"Carisma": 1, "Manipulação": 1, "Aparência": 1},
            "Mentais": {"Percepção": 1, "Inteligência": 1, "Raciocínio": 1}
        }
        
        # --- HABILIDADES (Base 0) ---
        
        self.habilidades = {
            "Militar": 0,
            "Intriga": 0,
            "Diplomacia": 0,
            "Finanças": 0,
            "Ocultismo": 0,
            "Política": 0
        }
        
        # --- VANTAGENS (Baseadas no Manual) ---
        self.disciplinas = {d: 0 for d in self.clan_info["disciplinas"]}
        self.antecedentes = {} # Ex: Rebanho, Recursos, Aliados (5 pontos na criação)
        self.virtudes = {"Consciência": 1, "Autocontrole": 1, "Coragem": 1} # (7 pontos na criação)
        
        # --- STATUS VITAIS ---
        self.vitalidade = 7  # Níveis: OK até Incapacitado
        self.forca_de_vontade = 5
        self.sangue_max = 10
        self.sangue_atual = 10
        self.caminho = 7     # Humanidade ou Caminho específico
        self.pontos_bonus = 15 if eh_jogador else 0

    def gerar_prompt_ia(self):
        """Gera o perfil para o NarradorIA (Gemini) entender o personagem"""
        artigo = "um" if self.genero == "Masculino" else "uma" if self.genero == "Feminino" else "um ser"
        return (f"{self.nome} é {artigo} cainita do clã {self.clan_info['perfil']}. "
                f"Sua natureza é {self.natureza}, seu comportamento é {self.comportamento} "
                f"e seu gênero é {self.genero}.")
