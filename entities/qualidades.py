MERITS = {
    # === FÍSICAS ===
    "Sentido Aguçado": {"custo": 1, "efeito": "Reduz dificuldade em 2 pts para testes com um sentido específico"},
    "Ambidestro": {"custo": 1, "efeito": "Sem penalidade para usar mão inábil"},
    "Ingerir Comida": {"custo": 1, "efeito": "Pode ingerir comida (mantém Máscara, mas precisa 'devolver' depois)"},
    "Equilíbrio Perfeito": {"custo": 1, "efeito": "Reduz dificuldade em 2 pts para testes de equilíbrio"},
    "Rubor de Saúde": {"custo": 2, "efeito": "Aparência +1 (parece mortal). Reduz dificuldade Social em 2 pts"},
    "Voz Encantadora": {"custo": 2, "efeito": "Reduz dificuldade em 2 pts para testes de persuasão/comando"},
    "Temerário": {"custo": 3, "efeito": "Adiciona 3 dados em ações arriscadas (dif 8+). Ignora 1 falha crítica no dado"},
    "Digestão Eficiente": {"custo": 3, "efeito": "Ganha 1 ponto de sangue extra a cada 2 consumidos (máx não excede reserva)"},
    "Corpo Grande": {"custo": 4, "efeito": "Tamanho aumentado. Vitalidade +1 nível. Força bruta"},
    
    # === MENTAIS ===
    "Bom Senso": {"custo": 1, "efeito": "Narrador pode dar dicas quando jogador vai fazer besteira"},
    "Concentração": {"custo": 1, "efeito": "Imune a distrações (ruídos, luzes estroboscópicas)"},
    "Noção Exata do Tempo": {"custo": 1, "efeito": "Sabe hora exata sem relógio"},
    "Código de Honra": {"custo": 2, "efeito": "Ganha 2 dados extras quando segue código, +1 dado em Força de Vontade/Virtude"},
    "Memória Eidética": {"custo": 2, "efeito": "Lembra-se de tudo visto/ouvido com perfeição"},
    "Sono Leve": {"custo": 2, "efeito": "Acorda instantaneamente ao menor sinal de perigo"},
    "Linguista Nato": {"custo": 2, "efeito": "Adiciona 3 dados em testes de linguagem"},
    "Temperamento Calmo": {"custo": 3, "efeito": "Adiciona 2 dados para resistir ao frenesi"},
    "Vontade de Ferro": {"custo": 3, "efeito": "Gasta 1 ponto de Força de Vontade para cancelar Dominação. +3 dados vs magia mental"},
    
    # === SOCIAIS ===
    "Senhor de Prestígio": {"custo": 1, "efeito": "Status +1 devido à ancestralidade (mesmo que o senhor não goste mais)"},
    "Líder Nato": {"custo": 1, "efeito": "Adiciona 2 dados em testes de Liderança (mínimo Carisma 3)"},
    "Dívida de Gratidão": {"custo": "1-3", "efeito": "Um ancião deve um favor (1=pouco, 3=vida)"},
    
    # === SOBRENATURAIS ===
    "Médium": {"custo": 2, "efeito": "Sente/fala com espíritos (preço: sangue ou favores aos espíritos)"},
    "Resistência à Magia": {"custo": 2, "efeito": "Dificuldade +2 para magias direcionadas a ele (exceto Taumaturgia)"},
    "Habilidade Oracular": {"custo": 3, "efeito": "Vê presságios (teste Percepção+Ocultismo). Interpretar: Inteligência+Ocultismo"},
    "Mentor Espiritual": {"custo": 3, "efeito": "Tem guia espiritual (Narrador define poderes/acesso)"},
    "Imunidade ao Laço de Sangue": {"custo": 3, "efeito": "Imune a laços de sangue (mas não a Vinculum)"},
    "Sorte": {"custo": 3, "efeito": "Pode repetir 3 testes fracassados por sessão (1x cada)"},
    "Amor Verdadeiro": {"custo": 4, "efeito": "Sucesso automático em Força de Vontade (só anulado por falha crítica)"},
    "Nove Vidas": {"custo": 6, "efeito": "Quando 'morrer', refaz o teste. Se passar, sobrevive (máx 9x)"},
    "Fé Verdadeira": {"custo": 7, "efeito": "Começa com 1 ponto de Fé. +1 dado por ponto em Força de Vontade/Virtude (máx 10)"},
}

                      #começo dos Defeitos#
FLAWS = {
    # === FÍSICOS ===
    "Cheiro do Túmulo": {"pontos": 1, "efeito": "Exala odor de terra revolvida. Dificuldade Social +1 com mortais"},
    "Estatatura Baixa": {"pontos": 1, "efeito": "Altura < 1,50m. Metade velocidade. Dificuldade manipular objetos de adulto"},
    "Deficiência Auditiva": {"pontos": 1, "efeito": "Dificuldade +2 para testes de audição"},
    "Caolho": {"pontos": 2, "efeito": "Um olho só. Dificuldade Percepção +2 (profundidade). Dano à distância -1 dado"},
    "Desfigurado": {"pontos": 2, "efeito": "Aparência = 0 máximo. Dificuldade Social +2"},
    "Criança": {"pontos": 3, "efeito": "Abraçado com 5-10 anos. Força/Vigor máx 2 (exceto com sangue). Dificuldade controlar/conduzir adultos +2"},
    "Deformidade": {"pontos": 3, "efeito": "Definido pelo Narrador (ex: corcunda, membro mal-formado). Penalidade física"},
    "Aleijado": {"pontos": 3, "efeito": "Velocidade 1/4. Precisa de muletas/bengala. Impossibilitado de correr"},
    "Monstruoso": {"pontos": 3, "efeito": "Aparência = 0 (monstro selvagem). Dificuldade Social extrema"},
    "Ferimento Permanente": {"pontos": 3, "efeito": "Acorda Ferido cada noite. Cicatrizes visíveis permanecem"},
    "Cura Demorada": {"pontos": 3, "efeito": "Cura 1 nível de dano a cada 5 dias (exceto com gasto de sangue/Força de Vontade)"},
    "Vício": {"pontos": 3, "efeito": "Dependente de substância (álcool, drogas, adrenalina). Enfraquecido sem acesso"},
    "Mudo": {"pontos": 4, "efeito": "Incapaz de falar. Comunicação: escrita ou linguagem de sinais"},
    "Sangue Fraco": {"pontos": 4, "efeito": "Custo de sangue dobrado para curar/ativar Disciplinas. Máx 8 pontos usáveis (exceto com aumento)"},
    "Portador de Doença Contagiosa": {"pontos": 4, "efeito": "10% de chance de infectar quem beber seu sangue. Gasto extra de sangue para 'limpar' o sangue"},
    "Surdez": {"pontos": 4, "efeito": "Incapaz de ouvir sons. Dificuldade +3 para ações que exigem audição"},
    "Pele Cadavérica": {"pontos": 5, "efeito": "Pele não regenera naturalmente. Cortes/arranhões permanecem visíveis"},
    "Cegueira": {"pontos": 6, "efeito": "Incapaz de enxergar. Dificuldade +2 para ações manuais (coordenação)"},
    
    # === MENTAIS ===
    "Sono Pesado": {"pontos": 1, "efeito": "Dificuldade +2 para acordar durante o dia. Teste Força de Vontade 7 ou perde dados"},
    "Pesadelos": {"pontos": 1, "efeito": "Pesadelos horríveis. Teste Força de Vontade 7 ao acordar ou -1 dado na noite"},
    "Fobia": {"pontos": 2, "efeito": "Medo irracional (aranhas, multidões, alturas). Teste de Coragem para enfrentar"},
    "Exclusão de Presa": {"pontos": 1, "efeito": "Recusa-se a alimentar de certo tipo (policiais, traficantes, ricos). Frenesi se violar"},
    "Timidez": {"pontos": 1, "efeito": "Dificuldade +2 para interação social com estranhos. +3 se centro de atenções"},
    "Coração Mole": {"pontos": 1, "efeito": "Não suporta ver outros Sofrerem. Teste Força de Vontade 8 ou evita Situação"},
    "Dificuldade de Fala": {"pontos": 1, "efeito": "Gago ou outro problema. Dificuldade +2 em testes relevantes"},
    "Bairrismo": {"pontos": 2, "efeito": "Territorial obsessivo. Teste de frenesi se outro vampiro entrar sem convite. Ataca intruso"},
    "Cabeça Quente": {"pontos": 2, "efeito": "Irrita-se facilmente. Dificuldade +2 para evitar frenesi"},
    "Vingança": {"pontos": 2, "efeito": "Obcecado em se vingar. Gasta 1 ponto de Força de Vontade para resistir compulsão"},
    "Amnésia": {"pontos": 1, "efeito": "Incapaz de recordar passado/própria família. Origem determinada pelo Narrador"},
    "Lunático": {"pontos": 2, "efeito": "Afetado pelas fases da lua. Dificuldade +1 (crescente), +2 (minguante), +3 (cheia) para frenesi"},
    "Vontade Fraca": {"pontos": 3, "efeito": "Dominação funciona automaticamente. Dificuldade +2 para resistir magia/Intimidação/Liderança"},
    "Consumo Conspícuo": {"pontos": 4, "efeito": "Precisa consumir órgãos (coração, fígado). Vítima morre. Sangue extra para 'limpar'"},
    
    # === SOCIAIS ===
    "Senhor Indigno": {"pontos": 1, "efeito": "Senhor o detesta. Aliados do senhor trabalham contra você"},
    "Segredo Sombrio": {"pontos": 1, "efeito": "Tem segredo embaraçoso (assassinato, traição, ser Sabá)"},
    "Identidade Trocada": {"pontos": 1, "efeito": "Parece com outro membro. Confusão de identidade constante"},
    "Ressentimento do Senhor": {"pontos": 1, "efeito": "Senhor não gosta de você. Procura prejudicar"},
    "Inimigo": {"pontos": "1-5", "efeito": "Quantos pontos gastar = poder do inimigo (1=rival, 5=arquimago/Matusalém)"},
    "Caçado": {"pontos": 4, "efeito": "Perseguido por caçador de bruxas. Aliados também podem ser caçados"},
    "Membro de Seita Sob Observação": {"pontos": 4, "efeito": "Desertor de seita. Desconfiança/hostilidade de todos"},
    
    # === SOBRENATURAIS ===
    "Toque de Congelamento": {"pontos": 1, "efeito": "Plantas murcham à aproximação. Retira calor de seres vivos"},
    "Repulsa ao Alho": {"pontos": 1, "efeito": "Não tolera cheiro de alho. Teste Força de Vontade ou sai do recinto"},
    "Presença Sinistra": {"pontos": 2, "efeito": "Mortais sentem desconforto. Dificuldade Social +2 com mortais"},
    "Repulsa a Cruzes": {"pontos": 3, "efeito": "Não tolera cruzes. Teste Força de Vontade 9 ou foge. Falha crítica = dano agravado"},
    "Incapacidade de Atravessar Água Corrente": {"pontos": 3, "efeito": "Incapaz de atravessar água corrente (>0,5m largura) sem ponte/elevado 15m"},
    "Assombrado": {"pontos": 3, "efeito": "Espírito zangado o atormenta (principalmente ao se alimentar). Narrador define"},
    "Aperto dos Amaldiçoados": {"pontos": 4, "efeito": "Vítimas lutam/gritam durante a alimentação. Mantém agarrado. Teste Humanidade"},
    "Futuro Negro": {"pontos": 5, "efeito": "Amaldiçoado com morte/sofrimento eterno. Visões terríveis. Gasta 1 Força de Vontade para ignorar ou -1 dado"},
    "Sensibilidade à Luz": {"pontos": 5, "efeito": "Luz do sol causa dobro do dano. Até o luar pode causar dano letal"},
}                     