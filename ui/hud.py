import pygame
from core.constants import CORES_CLANS, COR_VINHO, COR_FUNDO
import os

def desenhar_dots(tela, posicao_x, posicao_y, valor_atual, maximo_possivel=5):
    RAIO = 5
    ESPACO = 13
    for i in range(maximo_possivel):
        cor = (139, 0, 0) if i < valor_atual else (50, 50, 50)
        pos_x = posicao_x + (i * ESPACO)
        pygame.draw.circle(tela, cor, (pos_x, posicao_y), RAIO)
        pygame.draw.circle(tela, (200, 200, 200), (pos_x, posicao_y), RAIO, 1)

def desenhar_interface_completa(tela, imagem_fundo, jogador, selecionado, MAPA, fonte, fonte_titulo, ALTURA, img_coroa, img_calice, corte,):
    rects_membros = [] 
    rect_despertar = None
    
    # 1. FUNDO DO MAPA OU ÁREA DE VISUALIZAÇÃO
    if imagem_fundo:
        tela.blit(imagem_fundo, (300, 0))
    elif selecionado is not None:
        pygame.draw.rect(tela, (40, 40, 40), (300, 0, 900, ALTURA))

    # 2. HUD LATERAL FIXO (STATUS DO JOGADOR)
    pygame.draw.rect(tela, (20, 20, 20), (0, 0, 300, ALTURA))
    pygame.draw.line(tela, (139, 0, 0), (300, 0), (300, ALTURA), 3)

    # NOME E CLÃ
    txt_nome = fonte_titulo.render(jogador.nome, True, (255, 255, 255))
    tela.blit(txt_nome, (20, 30))
    
    nome_cla = getattr(jogador, 'clan_nome', "Ventrue")
    cor_c = CORES_CLANS.get(nome_cla, (200, 200, 200))
    txt_cla = fonte.render(f"Clã: {nome_cla}", True, cor_c)
    tela.blit(txt_cla, (20, 65))

    # ATRIBUTOS FÍSICOS
    y_atrib = 130
    txt_titulo_at = fonte.render("--- FÍSICOS ---", True, (100, 100, 100))
    tela.blit(txt_titulo_at, (20, y_atrib))
    y_atrib += 30

    for atrib, valor in jogador.atributos["Físicos"].items():
        txt_at = fonte.render(atrib[:3].upper(), True, (180, 180, 180))
        tela.blit(txt_at, (20, y_atrib))
        desenhar_dots(tela, 75, y_atrib + 10, valor)
        y_atrib += 25

    # 3. CONTEÚDO CENTRAL: MAPA OU SALA DO TRONO
    if imagem_fundo:  
        for nome, dom in MAPA.items():
            if hasattr(dom, 'pos_mapa'):
                x, y = dom.pos_mapa
                cor_ponto = CORES_CLANS.get(dom.dono, (150, 150, 150))
                pygame.draw.circle(tela, cor_ponto, (x + 300, y), 10)
                
                if dom.dono == jogador.clan_nome:
                    fonte_coroa_simbolo = pygame.font.SysFont("Segoe UI Symbol", 20)
                    txt_coroa_mapa = fonte_coroa_simbolo.render("👑", True, (255, 215, 0))
                    tela.blit(txt_coroa_mapa, (x + 300 - 10, y - 25))
                
                txt_bairro = fonte.render(nome, True, (200, 200, 200))
                tela.blit(txt_bairro, (x + 315, y - 10))

        if selecionado:
            pygame.draw.rect(tela, (40, 10, 10), (10, 500, 280, 120), border_radius=5)
            txt_b = fonte_titulo.render(selecionado.nome, True, (255, 255, 255))
            tela.blit(txt_b, (20, 510))
            txt_d = fonte.render(f"Dono: {selecionado.dono}", True, (200, 200, 200))
            tela.blit(txt_d, (20, 545))

    else:
        # --- ESTADO: SALA DO TRONO ---
        txt_titulo_corte = fonte_titulo.render("A CORTE DE JANEIRO", True, (255, 215, 0))
        tela.blit(txt_titulo_corte, (750 - txt_titulo_corte.get_width()//2, 40))

        y_lista = 100
        
        # Resgate de membros (Prioridade para a função nova do Manager 3)
        membros_da_lista = []
        if hasattr(corte, 'get_membros_para_hud'):
            membros_da_lista = corte.get_membros_para_hud()
        elif hasattr(corte, 'membros'):
            membros_da_lista = corte.membros

        for i, v in enumerate(membros_da_lista[:32]): 
            coluna = 400 if i < 16 else 820
            linha = i if i < 16 else i - 16
            pos_x, pos_y = coluna, y_lista + (linha * 35)

            # Extração de dados (suporta dicionário ou objeto)
            v_nome = v['nome'] if isinstance(v, dict) else v.nome
            v_cargo = v['cargo'] if isinstance(v, dict) else v.cargo.value
            v_cla = v['cla'] if isinstance(v, dict) else v.cla
            v_lealdade = v.get('lealdade', 50) if isinstance(v, dict) else getattr(v, 'lealdade', 50)
            v_poder = v.get('poder', 0) if isinstance(v, dict) else getattr(v, 'poder_base', 0)

            # Cores por lealdade
            cor_nome = (220, 220, 220)
            if v_lealdade > 80: cor_nome = (100, 255, 100)
            elif v_lealdade < 40: cor_nome = (255, 80, 80)

            # Texto: Nome - CARGO (Clã)
            txt_vampiro = fonte.render(f"{v_nome} - {v_cargo.upper()} ({v_cla})", True, cor_nome)
            tela.blit(txt_vampiro, (pos_x, pos_y))

            # Bolinha de Poder
            cor_poder = (150, 150, 150)
            if v_poder > 100: cor_poder = (255, 215, 0)
            pygame.draw.circle(tela, cor_poder, (pos_x - 15, pos_y + 12), 4)

            # Retângulo de clique
            rect_clique = pygame.Rect(pos_x - 25, pos_y, 380, 30)
            rects_membros.append((rect_clique, v))

    # 4. BOTÕES DO HUD (Coroa, Cálice e Despertar)
    x_coluna = 42 
    y_botoes = 662
    rect_coroa = pygame.Rect(x_coluna, y_botoes, 50, 50)
    rect_calice = pygame.Rect(x_coluna + 60, y_botoes, 50, 50)
    
    # Desenho dos botões com feedback de hover
    mouse_pos = pygame.mouse.get_pos()
    
    cor_c = (139, 0, 0) if rect_coroa.collidepoint(mouse_pos) else (50, 0, 0)
    pygame.draw.rect(tela, cor_c, rect_coroa, border_radius=5)
    if img_coroa: tela.blit(img_coroa, (rect_coroa.x + 5, rect_coroa.y + 5))

    cor_ca = (0, 0, 139) if rect_calice.collidepoint(mouse_pos) else (0, 0, 50)
    pygame.draw.rect(tela, cor_ca, rect_calice, border_radius=5)
    if img_calice: tela.blit(img_calice, (rect_calice.x + 5, rect_calice.y + 5))

    # Botão DESPERTAR
    rect_despertar = pygame.Rect(10, ALTURA - 70, 280, 50)
    pygame.draw.rect(tela, (60, 0, 0), rect_despertar, border_radius=10)
    pygame.draw.rect(tela, (139, 0, 0), rect_despertar, 2, border_radius=10)
    
    txt_btn = fonte_titulo.render("DESPERTAR", True, (255, 255, 255))
    tela.blit(txt_btn, (rect_despertar.centerx - txt_btn.get_width()//2, 
                        rect_despertar.centery - txt_btn.get_height()//2))

    return rect_despertar, rect_coroa, rect_calice, rects_membros

def desenhar_menu_acoes(tela, bairro, fonte_titulo):
    painel_rect = pygame.Rect(450, 250, 300, 300)
    pygame.draw.rect(tela, (20, 20, 20), painel_rect, border_radius=15)
    pygame.draw.rect(tela, (139, 0, 0), painel_rect, 2, border_radius=15)

    txt_bairro = fonte_titulo.render(f"ALVO: {bairro.nome}", True, (255, 255, 255))
    tela.blit(txt_bairro, (painel_rect.centerx - txt_bairro.get_width()//2, painel_rect.y + 20))

    acoes = [
        ("⚔️ GUERRA", (100, 0, 0), 80, "guerra"),
        ("🤝 DIPLOMACIA", (0, 0, 100), 140, "diplomacia"),
        ("🕵️ INTRIGA", (0, 100, 0), 200, "intriga")
    ]

    rects_botoes = {}
    for texto, cor, offset_y, chave in acoes:
        btn_rect = pygame.Rect(painel_rect.x + 25, painel_rect.y + offset_y, 250, 40)
        pygame.draw.rect(tela, cor, btn_rect, border_radius=5)
        txt_btn = pygame.font.SysFont("Arial", 16, bold=True).render(texto, True, (255, 255, 255))
        tela.blit(txt_btn, (btn_rect.centerx - txt_btn.get_width()//2, btn_rect.centery - txt_btn.get_height()//2))
        rects_botoes[chave] = btn_rect
        
    return rects_botoes

def desenhar_popup_vampiro(tela, v, fonte, fonte_titulo, LARGURA, ALTURA):
    # 1. Overlay escuro
    overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 220), (0, 0, LARGURA, ALTURA))
    tela.blit(overlay, (0, 0))

    # 2. Janela Principal (aumentei um pouco a altura para a idade)
    largura_p, altura_p = 500, 450 
    x_p = LARGURA // 2 - largura_p // 2
    y_p = ALTURA // 2 - altura_p // 2
    rect_fundo = pygame.Rect(x_p, y_p, largura_p, altura_p)
    
    pygame.draw.rect(tela, (20, 20, 20), rect_fundo, border_radius=15)
    pygame.draw.rect(tela, (139, 0, 0), rect_fundo, 3, border_radius=15)

    # 3. Extração de Dados
    nome = v.nome if hasattr(v, 'nome') else v.get('nome', 'N/A')
    cla = v.cla if hasattr(v, 'cla') else v.get('cla', 'N/A')
    # Pegando a IDADE
    idade = getattr(v, 'idade_vampiro', 0) if hasattr(v, 'idade_vampiro') else v.get('poder', 0)
    
    cargo_obj = v.cargo if hasattr(v, 'cargo') else v.get('cargo', 'membro')
    cargo_atual = cargo_obj.value if hasattr(cargo_obj, 'value') else str(cargo_obj)
    lealdade = getattr(v, 'lealdade', 50) if hasattr(v, 'lealdade') else v.get('lealdade', 50)

    # 4. Título e Info (Agora com Idade)
    txt_n = fonte_titulo.render(nome.upper(), True, (255, 255, 255))
    tela.blit(txt_n, (x_p + 30, y_p + 30))
    
    # Linha de Clã e Idade
    txt_s = fonte.render(f"Clã: {cla} | Idade: {idade} anos", True, (200, 200, 200))
    tela.blit(txt_s, (x_p + 30, y_p + 70))
    
    txt_c = fonte.render(f"Cargo Atual: {cargo_atual.upper()}", True, (139, 0, 0))
    tela.blit(txt_c, (x_p + 30, y_p + 95))

    # 5. Barra de Lealdade
    pygame.draw.rect(tela, (50, 50, 50), (x_p + 30, y_p + 140, 200, 10))
    cor_barra = (0, 200, 0) if lealdade > 50 else (200, 0, 0)
    pygame.draw.rect(tela, cor_barra, (x_p + 30, y_p + 140, lealdade * 2, 10))
    tela.blit(fonte.render(f"Lealdade: {lealdade}%", True, (255, 255, 255)), (x_p + 30, y_p + 120))

    # 6. LISTA DE CARGOS
    tela.blit(fonte.render("NOMEAR PARA CARGO:", True, (255, 255, 255)), (x_p + 30, y_p + 170))
    
    cargos_opcoes = ["SENESCAL", "SHERIFF", "HARPYA", "KEEPER"]
    botoes_cargos = {}

    for i, cargo_nome in enumerate(cargos_opcoes):
        bx, by = x_p + 30, y_p + 200 + (i * 45)
        rect_btn = pygame.Rect(bx, by, 440, 40)
        
        cor_btn = (50, 50, 50)
        if rect_btn.collidepoint(pygame.mouse.get_pos()):
            cor_btn = (80, 20, 20)
            
        pygame.draw.rect(tela, cor_btn, rect_btn, border_radius=5)
        pygame.draw.rect(tela, (100, 100, 100), rect_btn, 1, border_radius=5)
        
        txt_cargo = fonte.render(f"Definir como {cargo_nome}", True, (255, 255, 255))
        tela.blit(txt_cargo, (bx + 20, by + 10))
        
        botoes_cargos[cargo_nome.lower()] = rect_btn

    txt_esc = fonte.render("[ESC] PARA VOLTAR", True, (100, 100, 100))
    tela.blit(txt_esc, (x_p + largura_p // 2 - txt_esc.get_width() // 2, y_p + altura_p - 30))

    return botoes_cargos
def desenhar_popup_evento(tela, evento, fonte, fonte_titulo, LARGURA, ALTURA):
    # Overlay escuro para focar no evento
    fundo_escuro = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    fundo_escuro.fill((0, 0, 0, 180))
    tela.blit(fundo_escuro, (0, 0))

    # Caixa do Evento
    larg, alt = 650, 450
    x, y = (LARGURA - larg) // 2, (ALTURA - alt) // 2
    rect_box = pygame.Rect(x, y, larg, alt)
    
    pygame.draw.rect(tela, (25, 25, 25), rect_box, border_radius=12)
    pygame.draw.rect(tela, (139, 0, 0), rect_box, 3, border_radius=12) # Borda Vinho

    # Título
    txt_t = fonte_titulo.render(evento.titulo, True, (255, 255, 255))
    tela.blit(txt_t, (x + 30, y + 30))

    # Descrição (Quebra de linha simples)
    palavras = evento.descricao.split(' ')
    linha_atual = ""
    y_texto = y + 80
    for palavra in palavras:
        test_line = linha_atual + palavra + " "
        if fonte.size(test_line)[0] < larg - 60:
            linha_atual = test_line
        else:
            tela.blit(fonte.render(linha_atual, True, (200, 200, 200)), (x + 30, y_texto))
            linha_atual = palavra + " "
            y_texto += 22
    tela.blit(fonte.render(linha_atual, True, (200, 200, 200)), (x + 30, y_texto))

    # Botões de Escolha
    lista_botoes = []
    for i, escolha in enumerate(evento.escolhas):
        btn_rect = pygame.Rect(x + 30, y + 250 + (i * 60), larg - 60, 45)
        
        # Hover effect
        cor = (50, 50, 50)
        if btn_rect.collidepoint(pygame.mouse.get_pos()):
            cor = (80, 0, 0)
            # Tooltip da consequência
            txt_cons = fonte.render(f"Efeito: {escolha.descricao_consequencia}", True, (255, 215, 0))
            tela.blit(txt_cons, (x + 30, y + alt - 40))

        pygame.draw.rect(tela, cor, btn_rect, border_radius=5)
        pygame.draw.rect(tela, (139, 0, 0), btn_rect, 1, border_radius=5)
        
        txt_e = fonte.render(escolha.texto, True, (255, 255, 255))
        tela.blit(txt_e, (btn_rect.x + 15, btn_rect.y + 12))
        
        lista_botoes.append((btn_rect, escolha))
    
    return lista_botoes