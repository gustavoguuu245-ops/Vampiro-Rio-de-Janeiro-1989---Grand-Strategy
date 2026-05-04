# events.py
from dataclasses import dataclass
from typing import List, Callable

@dataclass
class Escolha:
    texto: str
    efeito: Callable
    descricao_consequencia: str

@dataclass
class Evento:
    titulo: str
    descricao: str
    escolhas: List[Escolha]
    peso: int = 100


# ====================== EVENTO INICIAL - PRIMEIRA NOITE ======================

def evento_primeira_noite(corte_manager, jogador):
    """Evento de abertura - Estilo CKIII clássico"""
    return Evento(
        titulo="Boa Noite, Príncipe",
        descricao=(
            "Boas-vindas à sua ascensão como governante do Rio de Janeiro, 1989.\n\n"
            " reconhecemos o seu direito de sangue. Seu poder agora cresce... "
            "mas junto com ele, os planos para sua queda já começam a ser tramados nas sombras.\n\n"
            "A corte está reunida pela primeira vez. Todos esperam sua primeira grande decisão."
        ),
        escolhas=[
            Escolha(
                texto="1. Declarar uma noite de caça livre (aumentar sangue da corte)",
                efeito=lambda: corte_manager.evento_noite_de_caca(),
                descricao_consequencia="A corte ganhou +3 sangue geral, mas a Mascarada enfraqueceu (-1)."
            ),
            Escolha(
                texto="2. Convocar o primeiro Elysium imediatamente",
                efeito=lambda: corte_manager.evento_primeiro_elysium(),
                descricao_consequencia="Ganhou +2 lealdade dos Primogênitos e da Harpia. A corte se sente mais organizada."
            ),
            Escolha(
                texto="3. Enviar o Sheriff atrás de rumores de Anarquistas",
                efeito=lambda: corte_manager.evento_investigar_anarquistas(),
                descricao_consequencia="O Sheriff ganhou +1 poder. Descobriu uma pequena célula anarquista na Lapa."
            )
        ]
    )


# ====================== OUTROS EVENTOS (para expansão futura) ======================


def evento_escandalo_harpia(corte_manager):
    return Evento(
        titulo="Escândalo na Copacabana",
        descricao="Um Toreador foi flagrado se alimentando de forma imprudente em uma festa na praia.",
        escolhas=[
            Escolha("Mandar a Harpia abafar o caso", 
                    lambda: corte_manager.harpia_abafar_escandalo(), 
                    "Harpia ganha +2 Status. Mascarada preservada."),
            Escolha("Humilhar publicamente o responsável", 
                    lambda: corte_manager.humilhar_publicamente(), 
                    "Ganha +1 Medo na corte, mas perde influência com os Toreador."),
        ]
    )


def evento_inveja_primogenito(corte_manager):
    return Evento(
        titulo="Inveja no Conselho",
        descricao="O Clã Ventrue acusa você de favorecer neófitos em detrimento dos anciões.",
        escolhas=[
            Escolha(
                texto="Elevar um Ventrue ao Conselho de Primogênitos", 
                efeito=lambda: corte_manager.promover_ventrue_ao_conselho(), 
                descricao_consequencia="+2 lealdade com TODOS os Ventrue da corte."
            ),
            Escolha(
                texto="Ignorar e reforçar sua autoridade", 
                efeito=lambda: corte_manager.reforcar_autoridade(), 
                descricao_consequencia="+2 Medo, mas perde influência com os Ventrue."
            ),
        ]
    )
# ====================== EVENTOS DE CRISE (ECONOMIA/SANGUE) ======================

def evento_fome_na_corte(corte_manager, eco_manager):
    """Dispara quando a reserva de sangue está crítica"""
    return Evento(
        titulo="🚨 CRISE: A Fome da Besta",
        descricao=(
            "A reserva de sangue atingiu níveis críticos. Os vampiros da sua corte\n"
            "olham para os mortais — e uns para os outros — com olhos famintos.\n\n"
            "Se nada for feito, o caos e o frenesi tomarão conta das ruas."
        ),
        escolhas=[
            Escolha(
                texto="1. Autorizar caçada brutal no Centro",
                efeito=lambda: corte_manager.evento_cacada_brutal(eco_manager),
                descricao_consequencia="+20 Sangue, mas a Mascarada sofre um golpe duro (-15)."
            ),
            Escolha(
                texto="2. Racionar sangue (Exigir sacrifício)",
                efeito=lambda: corte_manager.evento_racionamento(eco_manager),
                descricao_consequencia="-10 Lealdade geral. A elite está furiosa."
            ),
            Escolha(
                texto="3. Drenar um prisioneiro importante",
                efeito=lambda: corte_manager.evento_sacrificio_prisioneiro(eco_manager),
                descricao_consequencia="+10 Sangue e +5 Medo. Você governa pelo terror."
            )
        ],
        peso=500 # Peso altíssimo para priorizar em crises
    )

# ====================== EVENTOS NARRATIVOS (EXPANSÃO) ======================

def evento_conflito_favela(corte_manager):
    """Conflito entre clãs territoriais e o crime organizado"""
    return Evento(
        titulo="Sombras na Rocinha",
        descricao=(
            "Um grupo de Gangrels territoriais entrou em conflito com traficantes locais.\n"
            "Tiros foram trocados e a polícia está subindo o morro.\n\n"
            "Isso ameaça o silêncio da nossa espécie na Zona Sul."
        ),
        escolhas=[
            Escolha(
                texto="Apoiar os vampiros com o Sheriff",
                efeito=lambda: corte_manager.evento_investigar_anarquistas(), # Reutiliza a lógica de combate
                descricao_consequencia="+5 Lealdade com clãs combatentes. Risco de exposição."
            ),
            Escolha(
                texto="Deixar a polícia resolver (Preservar Mascarada)",
                efeito=lambda: corte_manager.humilhar_publicamente(), # Reutiliza lógica de autoridade
                descricao_consequencia="Mascarada protegida, mas os Gangrels se sentirão traídos."
            )
        ],
        peso=80
    )

def evento_malkaviano_lapa(corte_manager):
    """Evento aleatório de loucura Malkaviana"""
    return Evento(
        titulo="O Beijo do Arcos",
        descricao=(
            "Um Malkaviano influente está 'pregando' segredos da Gehenna embaixo dos Arcos da Lapa.\n"
            "Uma multidão de mortais curiosos está se reunindo."
        ),
        escolhas=[
            Escolha(
                texto="Mandar a Harpia espalhar que é performance artística",
                efeito=lambda: corte_manager.harpia_abafar_escandalo(),
                descricao_consequencia="Crise evitada. Harpia ganha prestígio."
            ),
            Escolha(
                texto="Silenciar o profeta à força",
                efeito=lambda: corte_manager.humilhar_publicamente(),
                descricao_consequencia="Gera medo. O segredo morre com ele."
            )
        ],
        peso=70
    )

# ====================== LISTA CENTRAL ATUALIZADA ======================

EVENTOS_POSSIVEIS = [
    evento_primeira_noite,
    evento_fome_na_corte,
    evento_conflito_favela,
    evento_malkaviano_lapa,
    evento_escandalo_harpia,
    evento_inveja_primogenito,
    evento_primeira_noite,
    evento_escandalo_harpia,
    evento_inveja_primogenito
]
