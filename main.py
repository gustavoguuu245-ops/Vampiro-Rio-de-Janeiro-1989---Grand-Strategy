import pygame
import sys
import os

# Garantir que o Python encontre as pastas internas
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.mapa import MAPA
from ui.hud import desenhar_interface_completa, desenhar_menu_acoes, desenhar_popup_vampiro, desenhar_popup_evento
from entities.player import PersonagemVampiro
from entities.clans import CLANS_DB
from manager.corte_manager import CorteManager
from manager.turn_manager import TurnManager
from manager.economia_manager import EconomiaGlobal
from manager.npc_manager import NPCManager
from manager.factions import SistemaFaccoes
from actions.conquista import tentar_invasao
from manager.evento_manager import EventManager

# ========================= CONFIGURAÇÕES INICIAIS =========================
pygame.init()
LARGURA, ALTURA = 1200, 800
tela = pygame.display.set_mode((LARGURA, ALTURA)) 
pygame.display.set_caption("VAMPIRO: RIO DE JANEIRO 1989")
relogio = pygame.time.Clock()

fonte = pygame.font.SysFont("Arial", 18)
fonte_titulo = pygame.font.SysFont("Arial", 28, bold=True)

# Assets Globais
imagem_fundo = None
img_coroa = None
img_calice = None
img_sala_trono = None
sala_trono_aberta = False 

try:
    imagem_fundo = pygame.image.load(os.path.join("assets", "maparj.png")).convert_alpha()
    imagem_fundo = pygame.transform.scale(imagem_fundo, (900, 800))
    img_coroa = pygame.image.load(os.path.join("assets", "icone_corte.png")).convert_alpha()
    img_coroa = pygame.transform.scale(img_coroa, (40, 40))
    img_calice = pygame.image.load(os.path.join("assets", "icone_diplomacia.png")).convert_alpha()
    img_calice = pygame.transform.scale(img_calice, (40, 40))
    img_sala_trono = pygame.image.load(os.path.join("assets", "corte.png")).convert_alpha()
    img_sala_trono = pygame.transform.scale(img_sala_trono, (LARGURA, ALTURA))
except Exception as e:
    print(f"⚠️ Erro ao carregar imagens: {e}")

# ========================= CRIAÇÃO DO PERSONAGEM =========================
def selecionar_personagem_visual():
    nome_texto = ""
    cla_selecionado = None
    executando_criacao = True
    COR_VINHO = (139, 0, 0)
    
    while executando_criacao:
        tela.fill((10, 10, 10))
        txt_t = fonte_titulo.render("CRIAÇÃO DO PRÍNCIPE", True, COR_VINHO)
        tela.blit(txt_t, (LARGURA//2 - txt_t.get_width()//2, 30))
        
        pygame.draw.rect(tela, (30, 30, 30), (LARGURA//2 - 200, 100, 400, 40))
        txt_n = fonte.render(f"Nome: {nome_texto}", True, (255, 255, 255))
        tela.blit(txt_n, (LARGURA//2 - 190, 110))
        
        botoes_clans = {}
        for i, clan in enumerate(CLANS_DB.keys()):
            col, lin = i // 7, i % 7
            rect = pygame.Rect(200 + (col * 450), 180 + (lin * 50), 350, 40)
            cor_box = COR_VINHO if cla_selecionado == clan else (40, 40, 40)
            pygame.draw.rect(tela, cor_box, rect, border_radius=5)
            tela.blit(fonte.render(clan, True, (255, 255, 255)), (rect.x + 10, rect.y + 10))
            botoes_clans[clan] = rect

        btn_confirmar = pygame.Rect(LARGURA//2 - 100, 650, 200, 60)
        if nome_texto and cla_selecionado:
            pygame.draw.rect(tela, (0, 100, 0), btn_confirmar, border_radius=10)
            txt_f = fonte_titulo.render("DESPERTAR", True, (255, 255, 255))
            tela.blit(txt_f, (btn_confirmar.centerx - txt_f.get_width()//2, 
                              btn_confirmar.centery - txt_f.get_height()//2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE: nome_texto = nome_texto[:-1]
                elif len(nome_texto) < 15 and event.unicode.isprintable(): nome_texto += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                for clan, rect in botoes_clans.items():
                    if rect.collidepoint(event.pos): cla_selecionado = clan
                if btn_confirmar.collidepoint(event.pos) and nome_texto and cla_selecionado:
                    return PersonagemVampiro(nome_texto, cla_selecionado, "Autocrata", "Arquiteto", "M", True)

        pygame.display.flip()
        relogio.tick(60)

# ========================= LOOP PRINCIPAL =========================
def rodar_game():
    global sala_trono_aberta 

    jogador = selecionar_personagem_visual()
    if not jogador: return

    # 1. Gerenciamento de NPCs e População
    npc_manager = NPCManager()
    npc_manager.inicializar_mundo(list(MAPA.keys()))

    # 2. Fundação da Corte (Elite e Cargos)
    corte = CorteManager(jogador.nome, jogador.clan_nome)
    corte.fundar_corte_inicial(npc_manager)

    # 3. Inicialização da Economia Global (PRECISA VIR ANTES DO EVENT MANAGER)
    eco_manager = EconomiaGlobal(jogador.nome, jogador.clan_nome)
    eco_manager.sistema_corte = corte

    # 4. LIGAÇÃO DO EVENT MANAGER (Agora ele já recebe o eco_manager pronto)
    event_manager = EventManager(corte, jogador, eco_manager)
    evento_atual = None  
    botoes_evento = []

    # 5. Outros Managers de Sistemas
    turn_manager = TurnManager(corte)
    gerenciador_faccoes = SistemaFaccoes(MAPA, jogador.clan_nome, npc_manager)

    for nome_bairro, dom in MAPA.items():
        pop_base = getattr(dom, 'populacao', 50000)
        dom.economia = eco_manager.adicionar_bairro(nome_bairro, pop_base)
        if dom.dono == jogador.clan_nome:
            dom.economia.adicionar_recurso("Refúgio do Príncipe", "haven", nivel=1).controlado_por = jogador.nome

    # Variáveis de Controle
    rodando = True
    bairro_foco = None
    menu_acao_aberto = False
    vampiro_foco = None  
    menu_detalhes_aberto = False
    botoes_menu = {}
    botoes_cargos = {}

    # Inicialização dos Rects
    rect_despertar = pygame.Rect(0,0,0,0)
    rect_coroa = pygame.Rect(0,0,0,0)
    rect_calice = pygame.Rect(0,0,0,0)
    rects_membros = []

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

            # --- TECLADO ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if evento_atual: # ESC não fecha evento, precisa escolher!
                        pass
                    elif menu_detalhes_aberto:
                        menu_detalhes_aberto = False
                        vampiro_foco = None
                    elif sala_trono_aberta:
                        sala_trono_aberta = False

            # --- TRATAMENTO DE MOUSE ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                
                # PRIORIDADE 1: SE TEM EVENTO, SÓ PROCESSA O EVENTO
                if evento_atual:
                    for rect, escolha in botoes_evento:
                        if rect.collidepoint(pos):
                            escolha.efeito()  
                            evento_atual = None 
                            botoes_evento = []
                            break
                    continue 

                # PRIORIDADE 2: Clique em Cargos (Sala do Trono)
                if menu_detalhes_aberto and 'botoes_cargos' in locals() and botoes_cargos:
                    clicou_cargo = False
                    for cargo_id, rect in botoes_cargos.items():
                        if rect.collidepoint(pos):
                            v_id = vampiro_foco['id'] if isinstance(vampiro_foco, dict) else vampiro_foco.id
                            from manager.corte_manager import CargoCorte
                            mapeamento = {
                                "senescal": CargoCorte.SENESCAL, "sheriff": CargoCorte.SHERIFF,
                                "harpya": CargoCorte.HARPIA, "keeper": CargoCorte.KEEPER_ELYSIUM
                            }
                            cargo_enum = mapeamento.get(cargo_id)
                            if cargo_enum:
                                sucesso, msg = corte.nomear_para_cargo(v_id, cargo_enum)
                                print(f"👑 SISTEMA: {msg}")
                                menu_detalhes_aberto = False
                                clicou_cargo = True
                                break
                    if clicou_cargo: 
                        continue

                # B. Clique no ícone da Coroa
                if rect_coroa.collidepoint(pos):
                    sala_trono_aberta = not sala_trono_aberta
                    menu_acao_aberto = False
                    continue

                # C. Selecionar membro na Sala do Trono
                if sala_trono_aberta and not menu_detalhes_aberto:
                    clicou_membro = False
                    for rect, v_info in rects_membros:
                        if rect.collidepoint(pos):
                            vampiro_foco = v_info
                            menu_detalhes_aberto = True
                            clicou_membro = True
                            break
                    if clicou_membro: 
                        continue

                # D. Cliques no Mapa (Apenas se a Sala do Trono estiver fechada)
                if not sala_trono_aberta:
                    # 1. Botão Despertar (Turno + Geração de Evento)
                    if rect_despertar and rect_despertar.collidepoint(pos):
                        if not evento_atual: # Só gera se não tiver um evento travando a tela
                            print("🌙 O sol se põe...")
                                
                            # 1. Processa a economia primeiro
                            turn_manager.processar_turno_completo([], eco_manager, corte)
                                
                            # 2. Captura o novo evento (A crise de sangue será checada aqui)
                            novo_evento = event_manager.gerar_evento(turn_manager.turno_atual)
                                
                            if novo_evento:
                                evento_atual = novo_evento
                                botoes_evento = [] 
                                print(f"✅ EVENTO DISPARADO: {evento_atual.titulo}")
                                    
                            # 3. Atualiza recursos e facções
                            jogador.sangue_atual = min(jogador.sangue_max, jogador.sangue_atual + 1)
                            gerenciador_faccoes.processar_turno_todas_faccoes(MAPA)
                        continue

                    # 2. Menu de Ações (Ex: Guerra)
                    if menu_acao_aberto and bairro_foco:
                        if "guerra" in botoes_menu and botoes_menu["guerra"].collidepoint(pos):
                            from actions.conquista import tentar_invasao
                            resultado = tentar_invasao(jogador, bairro_foco)
                            if resultado.get("sucesso"):
                                eco_manager.registrar_conquista(bairro_foco.nome, jogador)
                            menu_acao_aberto = False
                            continue

                    # 3. Seleção de Bairros
                    for nome, dom in MAPA.items():
                        if hasattr(dom, 'pos_mapa'):
                            bx, by = dom.pos_mapa
                            rect_clique = pygame.Rect(bx + 300 - 15, by - 15, 30, 30)
                            if rect_clique.collidepoint(pos):
                                bairro_foco = dom
                                menu_acao_aberto = True
                                break

        # ====================== DESENHO ======================
        tela.fill((0, 0, 0))

        if sala_trono_aberta:
            if img_sala_trono: tela.blit(img_sala_trono, (0, 0))
            else: tela.fill((30, 0, 0))
            
            _, rect_coroa, rect_calice, rects_membros = desenhar_interface_completa(
                tela, None, jogador, bairro_foco, MAPA, fonte, fonte_titulo, ALTURA, img_coroa, img_calice, corte
            )
            
            if menu_detalhes_aberto and vampiro_foco:
                botoes_cargos = desenhar_popup_vampiro(tela, vampiro_foco, fonte, fonte_titulo, LARGURA, ALTURA)
        else:
            rect_despertar, rect_coroa, rect_calice, _ = desenhar_interface_completa(
                tela, imagem_fundo, jogador, bairro_foco, MAPA, fonte, fonte_titulo, ALTURA, img_coroa, img_calice, corte
            )
            if menu_acao_aberto and bairro_foco:
                botoes_menu = desenhar_menu_acoes(tela, bairro_foco, fonte_titulo)
        
        # O EVENTO É DESENHADO POR CIMA DE TUDO (Mapa ou Sala do Trono)
        if evento_atual:
            botoes_evento = desenhar_popup_evento(tela, evento_atual, fonte, fonte_titulo, LARGURA, ALTURA) 

        pygame.display.flip()
        relogio.tick(60)

if __name__ == "__main__":
    try: rodar_game()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("\nPressione ENTER para sair...")
    finally: pygame.quit()