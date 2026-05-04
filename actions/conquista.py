# actions/conquista.py
from core.engine import rolar_dados

def tentar_invasao(jogador, bairro_alvo):
    """Executa a lógica de guerra usando Militar + Força"""
    if jogador.sangue_atual < 2:
        return {"sucesso": False, "msg": "🩸 Sangue insuficiente para mobilizar um ataque!"}

    # Definição do Pool
    forca = jogador.atributos["Físicos"]["Força"]
    militar = jogador.habilidades["Militar"]
    pool = forca + militar
    
    # Dificuldade baseada na influência
    dificuldade = 6 + (bairro_alvo.nivel_influencia // 2)

    # ROLAGEM (Ajustado para ler o dicionário do engine)
    resultado_dados = rolar_dados(pool, dificuldade)
    sucessos = resultado_dados.get('sucessos', 0) 

    jogador.sangue_atual -= 2 
    
    if sucessos > 0:
        bairro_alvo.dono = jogador.nome 
        return {
            "sucesso": True, 
            "msg": f"🚩 VITÓRIA! {bairro_alvo.nome} foi conquistado!",
            "sucessos": sucessos
        }
    else:
        return {
            "sucesso": False, 
            "msg": f"💀 DERROTA! A resistência em {bairro_alvo.nome} foi muito forte.",
            "sucessos": sucessos
        }