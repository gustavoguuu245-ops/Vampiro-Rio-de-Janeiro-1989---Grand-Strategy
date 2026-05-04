import time
import random



def rolar_dados(pool, dificuldade=6):
    """
    Sistema Storyteller D10 - Versão Visual de Luxo
    """
    if pool <= 0:
        pool = 1
        dificuldade += 1

    print(f"\n🎲 [DADOS]: Rolando {pool}d10 (Dificuldade {dificuldade})...")
    
    # Pequeno delay para aumentar a tensão (opcional, mas fica foda)
    time.sleep(0.6)
    
    resultados = [random.randint(1, 10) for _ in range(pool)]
    resultados.sort(reverse=True) # Maior para o menor para facilitar a leitura
    
    sucessos = sum(1 for d in resultados if d >= dificuldade)
    uns = resultados.count(1)
    sucessos_finais = sucessos - uns
    
    # Montando a representação visual dos dados
    dados_visuais = []
    for d in resultados:
        if d == 1:
            dados_visuais.append(f"[{d}]💀") # Falha crítica no dado
        elif d >= dificuldade:
            dados_visuais.append(f"[{d}]✨") # Sucesso no dado
        else:
            dados_visuais.append(f"[{d}]")   # Neutro
            
    print(f" ⊳ RESULTADO: {' '.join(dados_visuais)}")

    # Determinação do rótulo com ícones
    if sucessos_finais < 0:
        res_label = "🔴 FALHA CRÍTICA! (A Besta tomou o controle ou algo terrível ocorreu)"
    elif sucessos_finais == 0:
        res_label = "⚪ FALHA (Ação sem sucesso)"
    elif sucessos_finais == 1:
        res_label = "🟢 SUCESSO MARGINAL (Conseguiu por pouco)"
    elif sucessos_finais == 2:
        res_label = "🟢 SUCESSO MODERADO (Execução completa)"
    elif sucessos_finais == 3:
        res_label = "🔥 SUCESSO COMPLETO (Execução excelente)"
    else:
        res_label = f"🔱 SUCESSO EXCEPCIONAL ({sucessos_finais} sucessos!)"

    print(f" ⊳ STATUS: {res_label}\n")

    return {
        "sucessos": sucessos_finais,
        "label": res_label,
        "dados": resultados,
        "dificuldade": dificuldade
    }

# --- SISTEMA DE DISCIPLINAS E DIFICULDADES ESPECÍFICAS ---

DISCIPLINAS_REGRAS = {
    "Potência": {"tipo": "Passiva", "diff": 0}, # Adiciona sucessos automáticos em Força
    "Dominação": {"tipo": "Ativa", "diff": "Vontade da Vítima"}, # Dificuldade variável
    "Presença": {"tipo": "Ativa", "diff": 7}, # Algumas artes de Presença são diff 7 ou 8
    "Quietus": {"tipo": "Ativa", "diff": 8},
    "Vicissitude": {"tipo": "Ativa", "diff": 7},
    "Tenebrosidade": {"tipo": "Ativa", "diff": 6}
}
TABELA_GERACAO = {
    12: {"max_sangue": 10, "gasto_turno": 1},
    11: {"max_sangue": 10, "gasto_turno": 1},
    10: {"max_sangue": 11, "gasto_turno": 1},
    9:  {"max_sangue": 12, "gasto_turno": 1},
    8:  {"max_sangue": 13, "gasto_turno": 1},
    7:  {"max_sangue": 20, "gasto_turno": 4},
    6:  {"max_sangue": 30, "gasto_turno": 6}
}

def gastar_sangue_para_atributo(personagem, atributo_nome, quantidade):
    geracao_info = TABELA_GERACAO.get(personagem.geracao, TABELA_GERACAO[12])
    
    # Verifica se não excede o limite de gasto por turno
    if quantidade > geracao_info["gasto_turno"]:
        return f"Sua geração ({personagem.geracao}ª) só permite gastar {geracao_info['gasto_turno']} ponto(s) por turno."
    
    if personagem.sangue_atual >= quantidade:
        personagem.sangue_atual -= quantidade
        # O aumento é de 1 para 1 no Atributo Físico
        personagem.atributos["Físicos"][atributo_nome] += quantidade
        return f"Atributo {atributo_nome} aumentado em {quantidade}. Sangue atual: {personagem.sangue_atual}"
    else:
        return "Sangue insuficiente."

def usar_disciplina(personagem, nome_disciplina, alvo=None):
    """
    Puxa a dificuldade da disciplina e realiza o teste.
    """
    info = DISCIPLINAS_REGRAS.get(nome_disciplina, {"diff": 6})
    diff_final = info["diff"]
    
    # Se a dificuldade for dinâmica (como Vontade do Alvo), definimos aqui
    if diff_final == "Vontade da Vítima":
        diff_final = alvo.forca_de_vontade if alvo else 6
        
    # Exemplo de Pool: Atributo do Clã + Nível da Disciplina
    pool = personagem.disciplinas.get(nome_disciplina, 0)
    # Somamos com o atributo mental geralmente para magias
    pool += personagem.atributos["Mentais"]["Inteligência"] 
    
    return rolar_dados(pool, diff_final)

# --- GERADOR DE ALIADOS (Mantendo o que já deu certo) ---

def gerar_aliado_aleatorio(nome_aliado):
    # --- IMPORTS LOCAIS (Evita importação circular e garante que NATUREZAS exista) ---
    import random
    from entities.clans import CLANS_DB
    from entities.player import PersonagemVampiro, NATUREZAS
    
    # 1. Escolha de clã e arquétipos
    clan_nome = random.choice(list(CLANS_DB.keys()))
    natureza = random.choice(NATUREZAS)
    comportamento = random.choice(NATUREZAS)
    genero = random.choice(["Masculino", "Feminino"])
    
    # 2. Instância do aliado
    aliado = PersonagemVampiro(nome_aliado, clan_nome, natureza, comportamento, genero)
    
    # 3. Distribuição de Atributos baseada no foco do Clã
    foco = aliado.clan_info["atributo_foco"]
    categorias = ["Físicos", "Sociais", "Mentais"]
    random.shuffle(categorias)
    
    # Garante que a categoria que contém o atributo de foco do clã seja a prioridade 1 (7 pontos)
    for cat in categorias:
        if foco in aliado.atributos[cat]:
            categorias.remove(cat)
            categorias.insert(0, cat)
            break
            
    prioridades = [7, 5, 3]
    for i, cat in enumerate(categorias):
        pontos = prioridades[i]
        while pontos > 0:
            atrib = random.choice(list(aliado.atributos[cat].keys()))
            if aliado.atributos[cat][atrib] < 5:
                aliado.atributos[cat][atrib] += 1
                pontos -= 1
                
    # 4. Distribuição de Disciplinas (3 pontos iniciais)
    disc_list = list(aliado.disciplinas.keys())
    aliado.disciplinas[disc_list[0]] = 1 # Começa com pelo menos 1 na principal
    pontos_disc = 3
    while pontos_disc > 0:
        d = random.choice(disc_list)
        if aliado.disciplinas[d] < 3:
            aliado.disciplinas[d] += 1
            pontos_disc -= 1
            
    return aliado