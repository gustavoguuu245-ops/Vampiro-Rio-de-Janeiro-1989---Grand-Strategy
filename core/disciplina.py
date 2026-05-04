import random
from core.engine import rolar_dados



class DisciplinaManager:
    """Gerenciador Mestre de Disciplinas (Nível 1 ao 6) - 16 Disciplinas Féis ao Livro"""

    @staticmethod
    def executar_poder(personagem, nome_disciplina, poder_especifico, alvo=None):
        nivel = personagem.disciplinas.get(nome_disciplina, 0)
        
        # 1. ANIMALISMO
        if nome_disciplina == "Animalismo":
            if poder_especifico == "Linguagem Feral": # 1
                pool = personagem.atributos["Sociais"]["Manipulação"] + personagem.habilidades["Perícias"]["Empatia c/ Animais"]
                return rolar_dados(pool, 6)
            elif poder_especifico == "Chamado de Noé": # 2
                pool = personagem.atributos["Sociais"]["Carisma"] + personagem.habilidades["Perícias"]["Sobrevivência"]
                return rolar_dados(pool, 6)
            elif poder_especifico == "Intimidar a Besta": # 3
                pool = personagem.atributos["Sociais"]["Manipulação"] + personagem.habilidades["Talentos"]["Intimidação"]
                return rolar_dados(pool, 7)
            elif poder_especifico == "Cavalgar a Mente": # 4
                pool = personagem.atributos["Sociais"]["Carisma"] + personagem.habilidades["Perícias"]["Empatia c/ Animais"]
                return rolar_dados(pool, 8)
            elif poder_especifico == "Expulsando a Besta": # 5
                pool = personagem.atributos["Sociais"]["Manipulação"] + personagem.habilidades["Perícias"]["Empatia c/ Animais"]
                return rolar_dados(pool, 8)
            elif poder_especifico == "Unidade Acelerada": # 6
                pool = personagem.atributos["Mentais"]["Percepção"] + personagem.habilidades["Perícias"]["Empatia c/ Animais"]
                return rolar_dados(pool, 6)

        # 2. AUSPÍCIOS
        elif nome_disciplina == "Auspícios":
            if poder_especifico == "Sentidos Aguçados": # 1
                return rolar_dados(nivel, 6)
            elif poder_especifico == "Visão da Alma": # 2
                pool = personagem.atributos["Mentais"]["Percepção"] + personagem.habilidades["Talentos"]["Empatia"]
                return rolar_dados(pool, 8)
            elif poder_especifico == "Toque do Espírito": # 3
                pool = personagem.atributos["Mentais"]["Percepção"] + personagem.habilidades["Talentos"]["Empatia"]
                return rolar_dados(pool, 6)
            elif poder_especifico == "Roubar Segredos": # 4
                pool = personagem.atributos["Mentais"]["Inteligência"] + personagem.habilidades["Talentos"]["Lábia"]
                return rolar_dados(pool, alvo.forca_de_vontade if alvo else 7)
            elif poder_especifico == "Caminhada da Anima": # 5
                personagem.forca_de_vontade -= 1
                pool = personagem.atributos["Mentais"]["Percepção"] + personagem.habilidades["Conhecimentos"]["Ocultismo"]
                return rolar_dados(pool, 7)
            elif poder_especifico == "Visão Longínqua": # 6
                pool = personagem.atributos["Mentais"]["Percepção"] + personagem.habilidades["Talentos"]["Empatia"]
                return rolar_dados(pool, 6)

        # 3. DEMÊNCIA
        elif nome_disciplina == "Demência":
            if poder_especifico == "Paixão do Íncubo": # 1
                pool = personagem.atributos["Sociais"]["Carisma"] + personagem.habilidades["Talentos"]["Empatia"]
                return rolar_dados(pool, alvo.caminho if alvo else 7)
            elif poder_especifico == "Assombrar a Alma": # 2
                pool = personagem.atributos["Sociais"]["Manipulação"] + personagem.habilidades["Talentos"]["Lábia"]
                return rolar_dados(pool, (alvo.atributos["Mentais"]["Percepção"] + 3) if alvo else 7)
            elif poder_especifico == "Visão do Caos": # 3
                return rolar_dados(personagem.atributos["Mentais"]["Percepção"] + personagem.habilidades["Conhecimentos"]["Ocultismo"], 7)
            elif poder_especifico == "Confusão": # 4
                pool = personagem.atributos["Sociais"]["Manipulação"] + personagem.habilidades["Talentos"]["Intimidação"]
                return rolar_dados(pool, alvo.forca_de_vontade if alvo else 7)
            elif poder_especifico == "Loucura Uivante": # 5
                return rolar_dados(personagem.atributos["Sociais"]["Manipulação"] + personagem.habilidades["Talentos"]["Intimidação"], alvo.forca_de_vontade if alvo else 8)
            elif poder_especifico == "Beijo da Lua": # 6
                return rolar_dados(personagem.atributos["Sociais"]["Manipulação"] + personagem.habilidades["Talentos"]["Empatia"], alvo.forca_de_vontade if alvo else 9)

        # 4. DOMINAÇÃO
        elif nome_disciplina == "Dominação":
            diff = alvo.forca_de_vontade if alvo else 7
            if poder_especifico == "Observância": pool = personagem.atributos["Sociais"]["Manipulação"] + personagem.habilidades["Talentos"]["Intimidação"] # 1
            elif poder_especifico == "Murmúrio": pool = personagem.atributos["Sociais"]["Manipulação"] + personagem.habilidades["Talentos"]["Liderança"] # 2
            elif poder_especifico == "Memória do Dissoluto": pool = personagem.atributos["Mentais"]["Raciocínio"] + personagem.habilidades["Talentos"]["Lábia"] # 3
            elif poder_especifico == "Isca": pool = personagem.atributos["Sociais"]["Carisma"] + personagem.habilidades["Talentos"]["Liderança"] # 4
            elif poder_especifico == "Possessão": pool = personagem.atributos["Sociais"]["Carisma"] + personagem.habilidades["Talentos"]["Intimidação"] # 5
            elif poder_especifico == "Fidelidade": pool = personagem.atributos["Sociais"]["Carisma"] + personagem.habilidades["Talentos"]["Liderança"] # 6
            return rolar_dados(pool, diff)

        # 5. METAMORFOSE
        elif nome_disciplina == "Metamorfose":
            if poder_especifico == "Testemunha": return {"sucessos": 1, "label": "Visão Noturna"} # 1
            personagem.sangue_atual -= 1
            if poder_especifico == "Garras": return {"sucessos": 1, "label": "Garras (Agravado)"} # 2
            elif poder_especifico == "Enterrado": return {"sucessos": 1, "label": "Fusão com a Terra"} # 3
            elif poder_especifico == "Forma da Besta": return {"sucessos": 1, "label": "Lobo/Morcego"} # 4
            elif poder_especifico == "Corpo Espiritual": return {"sucessos": 1, "label": "Névoa"} # 5
            elif poder_especifico == "Sono Tranquilo": # 6
                personagem.sangue_atual -= 4
                return {"sucessos": 1, "label": "Sono em Névoa"}

        # 6. TENEBROSIDADE
        elif nome_disciplina == "Tenebrosidade":
            if poder_especifico == "Jogo de Sombras": # 1
                personagem.sangue_atual -= 1
                return {"sucessos": 1, "label": "Sombra Manipulada"}
            elif poder_especifico == "Noturno": # 2
                pool = personagem.atributos["Sociais"]["Manipulação"] + personagem.habilidades["Conhecimentos"]["Ocultismo"]
                return rolar_dados(pool, 7)
            elif poder_especifico == "Braços de Ahriman": # 3
                return rolar_dados(personagem.atributos["Sociais"]["Manipulação"] + personagem.habilidades["Conhecimentos"]["Ocultismo"], 7)
            elif poder_especifico == "Sombras Noturnas": # 4
                return rolar_dados(personagem.atributos["Mentais"]["Raciocínio"] + personagem.habilidades["Conhecimentos"]["Ocultismo"], 7)
            elif poder_especifico == "Forma Tenebrosa": # 5
                personagem.sangue_atual -= 3
                return {"sucessos": 1, "label": "Sombra Viva"}
            elif poder_especifico == "Caminhar no Abismo": # 6
                return rolar_dados(personagem.atributos["Mentais"]["Inteligência"] + personagem.habilidades["Perícias"]["Furtividade"], 6)

        # 7. MORTIS
        elif nome_disciplina == "Mortis":
            if poder_especifico == "Máscara": # 1
                personagem.sangue_atual -= 1
                return rolar_dados(personagem.atributos["Físicos"]["Vigor"] + personagem.habilidades["Conhecimentos"]["Medicina"], 6)
            elif poder_especifico == "Murchar": # 2
                personagem.forca_de_vontade -= 1
                return rolar_dados(personagem.atributos["Sociais"]["Manipulação"] + personagem.habilidades["Conhecimentos"]["Medicina"], alvo.forca_de_vontade if alvo else 7)
            elif poder_especifico == "Despertar": # 3
                personagem.forca_de_vontade -= 2
                return rolar_dados(personagem.forca_de_vontade, 10 - (alvo.caminho if alvo else 7))
            elif poder_especifico == "Sussurros": return {"sucessos": 1, "label": "Estado de Morte"} # 4
            elif poder_especifico == "Morte Negra": # 5
                return rolar_dados(personagem.atributos["Físicos"]["Vigor"] + personagem.habilidades["Conhecimentos"]["Ocultismo"], alvo.forca_de_vontade if alvo else 8)
            elif poder_especifico == "Vigor Mortis": # 6
                personagem.sangue_atual -= 3
                return {"sucessos": 1, "label": "Zumbi Criado"}

        # 8. QUIETUS
        elif nome_disciplina == "Quietus":
            if poder_especifico == "Silêncio": return {"sucessos": 1, "label": "Silêncio Ativo"} # 1
            elif poder_especifico == "Fraqueza": # 2
                # Regra: Força de Vontade vs (Vigor + Fortitude) do alvo
                pool = personagem.forca_de_vontade
                # Busca o Vigor do alvo e soma a Fortitude (se ele tiver), caso contrário usa dificuldade 6
                diff = (alvo.atributos["Físicos"]["Vigor"] + alvo.disciplinas.get("Fortitude", 0)) if alvo else 6
                return rolar_dados(pool, diff)
            elif poder_especifico == "Doença": # 3
                personagem.sangue_atual -= 3
                return rolar_dados(personagem.forca_de_vontade, alvo.forca_de_vontade if alvo else 7)
            elif poder_especifico == "Agonia": # 4
                personagem.sangue_atual -= 1
                return {"sucessos": 1, "label": "Arma Envenenada"}
            elif poder_especifico == "Essência": return {"sucessos": 1, "label": "Diablerie à Distância"} # 5
            elif poder_especifico == "Suor de Sangue": # 6
                return rolar_dados(personagem.forca_de_vontade, (alvo.atributos["Físicos"]["Vigor"] + 3) if alvo else 6)

        # 9. PRESENÇA
        elif nome_disciplina == "Presença":
            if poder_especifico == "Fascínio": pool, diff = (personagem.atributos["Sociais"]["Carisma"] + personagem.habilidades["Talentos"]["Representação"]), 7
            elif poder_especifico == "Olhar": pool, diff = (personagem.atributos["Sociais"]["Carisma"] + personagem.habilidades["Talentos"]["Intimidação"]), (alvo.atributos["Mentais"]["Raciocínio"] + 3 if alvo else 6)
            elif poder_especifico == "Transe": pool, diff = (personagem.atributos["Sociais"]["Aparência"] + personagem.habilidades["Talentos"]["Empatia"]), (alvo.forca_de_vontade if alvo else 6)
            elif poder_especifico == "Convocação": pool, diff = (personagem.atributos["Sociais"]["Carisma"] + personagem.habilidades["Talentos"]["Lábia"]), 5
            elif poder_especifico == "Majestade": return {"sucessos": nivel, "label": "Aura Majestosa"}
            elif poder_especifico == "Paixão": pool, diff = (personagem.atributos["Sociais"]["Manipulação"] + personagem.habilidades["Talentos"]["Lábia"]), (alvo.forca_de_vontade if alvo else 7)
            return rolar_dados(pool, diff)

        # 10. SERPENTIS
        elif nome_disciplina == "Serpentis":
            if poder_especifico == "Olhos": return rolar_dados(personagem.forca_de_vontade, 9) # 1
            elif poder_especifico == "Língua": return rolar_dados(personagem.atributos["Físicos"]["Destreza"] + 3, 6) # 2
            elif poder_especifico == "Pele": return {"sucessos": 1, "label": "Pele Betuminosa"} # 3
            elif poder_especifico == "Forma": return {"sucessos": 1, "label": "Cobra Negra"} # 4
            elif poder_especifico == "Coração": return {"sucessos": 1, "label": "Coração Removido"} # 5
            elif poder_especifico == "Hálito": # 6
                personagem.sangue_atual -= 1
                return rolar_dados(personagem.atributos["Físicos"]["Destreza"] + personagem.habilidades["Talentos"]["Briga"], 6)

        # 11. QUIMERISMO
        elif nome_disciplina == "Quimerismo":
            if poder_especifico == "Ignis Fatuus": personagem.forca_de_vontade -= 1
            elif poder_especifico == "Fata Morgana": personagem.forca_de_vontade -= 2
            elif poder_especifico == "Aparição": personagem.sangue_atual -= 1
            elif poder_especifico == "Cruel Realidade":
                personagem.forca_de_vontade -= 2
                return rolar_dados(personagem.atributos["Sociais"]["Manipulação"] + personagem.habilidades["Talentos"]["Lábia"], (alvo.atributos["Mentais"]["Percepção"] + 3) if alvo else 7)
            return {"sucessos": 1, "label": "Ilusão Criada"}

        # 12. TAUMATURGIA (Trilhas do Sangue Tremere)
        elif nome_disciplina == "Taumaturgia":
            personagem.sangue_atual -= 1 # Custo padrão de ativação
            pool = personagem.forca_de_vontade
            diff = nivel + 3
            
            # --- TRILHA: REGO VITAE (Trilha do Sangue - Padrão) ---
            if poder_especifico == "Um Gosto por Sangue": # N1
                return rolar_dados(pool, diff) # Sucessos determinam precisão das infos
            elif poder_especifico == "Furia do Sangue": # N2
                # Força o alvo a gastar sangue para aumentar atributos ou frenesi
                return rolar_dados(pool, diff)
            elif poder_especifico == "Potencia do Sangue": # N3
                # Executa a rolagem e guarda o dicionário de retorno
                resultado = rolar_dados(pool, diff)
                sucessos = resultado["sucessos"]
                
                if sucessos > 0:
                    # Regra do Livro: Cada sucesso diminui a geração temporariamente
                    personagem.geracao -= sucessos
                    return {
                        "sucessos": sucessos, 
                        "label": f"Geração reduzida para {personagem.geracao}ª por {sucessos} horas."
                    }
                return resultado # Retorna a falha normal
            elif poder_especifico == "Furto de Vitae": # N4
                # Rouba sangue à distância (15 metros)
                return rolar_dados(pool, diff)
            elif poder_especifico == "Caldeirao de Sangue": # N5
                # Ferve o sangue do alvo (1 nível de dano por ponto fervido)
                return rolar_dados(pool, diff)

            # --- TRILHA: CREO IGNEM (Trilha das Chamas) ---
            elif "Chamas" in poder_especifico:
                # N1: Vela, N2: Palma, N3: Fogueira, N4: Execução, N5: Incêndio
                return rolar_dados(pool, diff)

            # --- TRILHA: REGO MOTUS (Trilha do Movimento) ---
            elif "Movimento" in poder_especifico:
                # N1: 0.5kg, N2: 10kg, N3: 100kg/Levitar, N4: 200kg, N5: 1 Tonelada
                return rolar_dados(pool, diff)

            # --- TRILHA: REGO TEMPESTAS (Trilha do Clima) ---
            elif "Clima" in poder_especifico:
                # N1: Neblina, N2: Chuva, N3: Vento, N4: Tempestade, N5: Raio
                return rolar_dados(pool, diff)

            # --- TRILHA: REGO AQUAM (Trilha da Água) ---
            elif poder_especifico == "Jaula de Agua": # N2
                return rolar_dados(pool, diff)
            elif poder_especifico == "Desidratar": # N3
                # Vítima resiste com Vigor + Sobrevivência (Diff 9)
                return rolar_dados(pool, diff)
            elif poder_especifico == "Transformar Sangue em Agua": # N5
                return rolar_dados(pool, diff)
            return rolar_dados(personagem.forca_de_vontade, nivel + 3) # 1-5
            

        # 13. VICISSITUDE (Clã Tzimisce)
        elif nome_disciplina == "Vicissitude":
            # Pool base: Destreza + Medicina (Dificuldade varia conforme a complexidade)
            pool = personagem.atributos["Físicos"]["Destreza"] + personagem.habilidades["Conhecimentos"]["Medicina"]
            
            # Nível 1: Semblante Maleável (Mudar a própria aparência)
            if poder_especifico == "Semblante Maleavel":
                return rolar_dados(pool, 6) # Mais fácil mexer no próprio rosto
            
            # Nível 2: Moldar Carne (Mudar os outros / Criar deformidades)
            elif poder_especifico == "Moldar Carne":
                # Pode aumentar/diminuir Aparência ou causar dano por asfixia/cegueira
                return rolar_dados(pool, 7)
            
            # Nível 3: Moldar Ossos (Armas ósseas ou colapsar costelas)
            elif poder_especifico == "Moldar Ossos":
                # Pode criar garras de osso ou espinhos (Dano Letal/Agravado)
                return rolar_dados(pool, 8)
            
            # Nível 4: Forma de Zulo (A forma de guerra horripilante)
            elif poder_especifico == "Forma de Zulo":
                # Gasta 2 de sangue. Ganha +2 em todos os atributos físicos.
                personagem.sangue_atual -= 2
                return {"sucessos": 1, "label": "Transformado em Monstro Zulo (+2 For/Des/Vig)"}
            
            # Nível 5: Forma de Plasma (Virar sangue vivo)
            elif poder_especifico == "Forma de Plasma":
                # Pode passar por frestas e é imune a dano físico (exceto fogo/sol)
                personagem.sangue_atual -= 2
                return {"sucessos": 1, "label": "Transformado em Plasma Sanguíneo"}
            
            # Nível 6: Sopro do Dragão (Vomitar fogo/ácido) ou Simbiose
            elif poder_especifico == "Sopro do Dragao":
                # Causa 2 dados de dano agravado (fogo místico)
                personagem.sangue_atual -= 1
                return rolar_dados(personagem.atributos["Físicos"]["Vigor"] + 3, 6)

        elif nome_disciplina == "Ofuscação":
            if poder_especifico == "Manto das Sombras": return {"sucessos": 1, "label": "Oculto nas Sombras"} # N1
            elif poder_especifico == "Presenca Invisivel": return rolar_dados(personagem.atributos["Mentais"]["Raciocínio"] + personagem.habilidades["Perícias"]["Furtividade"], 6) # N2
            elif poder_especifico == "Máscara": return rolar_dados(personagem.atributos["Sociais"]["Manipulação"] + personagem.habilidades["Talentos"]["Representação"], 7) # N3
            elif poder_especifico == "Desaparecimento": 
                diff = (alvo.atributos["Físicos"]["Resistência"] + alvo.habilidades["Talentos"]["Prontidão"]) if alvo else 7
                return rolar_dados(personagem.atributos["Sociais"]["Carisma"] + personagem.habilidades["Perícias"]["Furtividade"], diff) # N4
            elif poder_especifico == "Cobrir o Grupo": return {"sucessos": 1, "label": "Grupo Oculto"} # N5
            elif poder_especifico == "Máscara da Alma": return {"sucessos": 1, "label": "Aura Disfarçada"} # N6

        elif nome_disciplina == "Daimoinon":
            if poder_especifico == "Sentir Pecado": # N1
                diff = (alvo.virtudes["Autocontrole"] + 4) if alvo else 7
                return rolar_dados(personagem.atributos["Mentais"]["Percepção"] + 3, diff)
            elif poder_especifico == "Temor do Vazio": # N2
                diff = (alvo.virtudes["Coragem"] + 4) if alvo else 7
                return rolar_dados(personagem.atributos["Mentais"]["Raciocínio"] + 3, diff)
            elif poder_especifico == "Chamas": return rolar_dados(personagem.atributos["Físicos"]["Destreza"] + 3, 6) # N3
            elif poder_especifico == "Invocar a Besta": return rolar_dados(personagem.atributos["Sociais"]["Manipulação"] + 3, 8) # N4
            elif poder_especifico == "Maldição": return rolar_dados(personagem.atributos["Mentais"]["Inteligência"] + 3, alvo.forca_de_vontade if alvo else 8) # N5
            elif poder_especifico == "Ignorar as Chamas": return {"sucessos": 1, "label": "Imune ao Fogo (menos Sol)"} # N6

        # 16. POTÊNCIA / FORTITUDE / RAPIDEZ
        elif nome_disciplina == "Potência": return {"sucessos": nivel, "label": "Força Bruta"}
        elif nome_disciplina == "Fortitude": return {"sucessos": nivel, "label": "Resistência"}
        elif nome_disciplina == "Rapidez":
            personagem.sangue_atual -= nivel
            return {"sucessos": nivel, "label": "Velocidade"}

        return {"sucessos": 0, "label": "Poder não mapeado"}

# --- DICIONÁRIO NARRATIVO PARA A IA ---
DISCIPLINAS_LORE = {
    "Animalismo": "Domínio sobre feras e a Besta. Pode comandar animais e até entrar em seus corpos.",
    "Auspícios": "Sentidos divinos. Vê auras, lê objetos e projeta a consciência pelo cordão de prata.",
    "Demência": "A loucura mística dos Malkavianos. Incendeia paixões e cria visões de pesadelo.",
    "Dominação": "Escravidão mental pelo olhar. Comandos de uma palavra ou reescrita de memórias.",
    "Fortitude": "Resistência de pedra. Permite ignorar golpes e resistir ao Sol e ao Fogo.",
    "Metamorfose": "Transformação em predadores, névoa ou fusão com o solo sagrado.",
    "Mortis": "Alquimia da morte. Pode mumificar inimigos, murchar membros e animar cadáveres (zumbis).",
    "Ofuscação": "Ocultismo visual. Permite sumir das mentes alheias e assumir mil faces.",
    "Potência": "Vigor físico sobrenatural. Cada nível garante força para esmagar aço e ossos.",
    "Presença": "Magnetismo aterrador. Atrai multidões, causa transe de amor ou pânico paralisante.",
    "Quietus": "O silêncio do assassino. Sangue vira veneno e armas causam feridas que não fecham.",
    "Quimerismo": "Maestria das ilusões. Cria imagens, sons e realidades que podem até ferir.",
    "Rapidez": "Velocidade da luz. Permite realizar múltiplas ações antes que o alvo pisque.",
    "Taumaturgia": "Feitiçaria de sangue Tremere. Controla fogo, elementos e rouba o vitae à distância.",
    "Tenebrosidade": "Manipulação do Abismo. Sombras vivas, tentáculos e escuridão absoluta.",
    "Vicissitude": "Escultura de carne e osso. Transforma o corpo em armas ou o inimigo em uma massa informe."
}