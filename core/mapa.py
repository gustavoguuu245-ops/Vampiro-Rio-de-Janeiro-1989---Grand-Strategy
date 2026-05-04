# entities/mapa.py
from entities.clans import CLANS_DB

class Dominio:
    def __init__(self, nome, zona, clan_nome, recurso, vizinhos, pos_mapa):
        self.nome = nome
        self.zona = zona
        self.dono = clan_nome
        self.recurso_foco = recurso
        self.vizinhos = vizinhos 
        self.pos_mapa = pos_mapa  # (x, y) relativo ao PNG do mapa
        self.nivel_influencia = 3
        self.estabilidade = 100
        
        # Pega info extra do seu clans.py automaticamente
        self.perfil_defesa = CLANS_DB[clan_nome]["atributo_foco"]

# O "Banco de Dados" do seu mapa - ADICIONEI AS COORDENADAS (X, Y)
# Nota: Estes números são chutes iniciais. Tu vais calibrar clicando no jogo!
MAPA = {
    "Campo Grande": Dominio("Campo Grande", "Zona Oeste", "Setita", "Efetivo", ["Bangu", "Santa Cruz"], (252, 509)),
    "Bangu": Dominio("Bangu", "Zona Oeste", "Brujah", "Força", ["Campo Grande", "Madureira"], (369, 445)),
    "Santa Cruz": Dominio("Santa Cruz", "Zona Oeste", "Gangrel", "Sobrevivência", ["Campo Grande"], (134, 511)),
    "Tijuca": Dominio("Tijuca", "Zona Norte", "Nosferatu", "Informação", ["Centro", "Méier"], (504, 250)),
    "Madureira": Dominio("Madureira", "Zona Norte", "Malkaviano", "Caos", ["Bangu", "Méier"], (355, 296)),
    "Méier": Dominio("Méier", "Zona Norte", "Capadócio", "Morte", ["Tijuca", "Madureira"], (390, 231)),
    "Copacabana": Dominio("Copacabana", "Zona Sul", "Toreador", "Social", ["Ipanema", "Botafogo"], (471, 624)),
    "Ipanema": Dominio("Ipanema", "Zona Sul", "Ventrue", "Dinheiro", ["Copacabana"], (558, 575)),
    "Botafogo": Dominio("Botafogo", "Zona Sul", "Tremere", "Ocultismo", ["Copacabana", "Centro"], (620, 528)),
    "Centro": Dominio("Centro", "Centro", "Lasombra", "Política", ["Tijuca", "Botafogo"], (570, 403)),
    "Lapa": Dominio("Lapa", "Centro", "Ravnos", "Ilusão", ["Centro", "Santa Teresa"], (470, 368)),
    "Santa Teresa": Dominio("Santa Teresa", "Centro", "Assamita", "Assassinato", ["Lapa", "Centro", "Tijuca"], (561, 468)),
    "Castelo": Dominio("Castelo", "Centro", "Giovanni", "Finanças", ["Centro", "Lapa"], (530, 444)),
    "Ilha do Governador": Dominio("Ilha do Governador", "Zona Norte", "Tzimisce", "Experimentos", ["Centro", "Méier"], (547, 153))
}
