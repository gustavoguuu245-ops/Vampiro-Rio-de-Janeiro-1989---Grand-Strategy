
ARQUETIPOS = {
    # === SOCIAIS/POLÍTICOS ===
    "Autocrata": {
        "descricao": "Quer ser o chefe. Busca proeminência e controle.",
        "comportamento": "Ditadores, líderes de quadrilhas, empresários impiedosos",
        "bonus": {"Lideranca": 1, "Intimidacao": 1},
        "penalidade": {"Empatia": -1}  # Dificuldade em ouvir outros
    },
    "Bon Vivant": {
        "descricao": "Vive para se divertir. Hedonista, sibarita.",
        "comportamento": "Filhos únicos, artistas excêntricos, festeiros",
        "bonus": {"Carisma": 1, "Prontidao": 1},  # Festas improvisadas
        "penalidade": {"Autocontrole": -1}  # Excessoos fáceis
    },
    "Celebrante": {
        "descricao": "Encontra alegria na causa. Entusiasmo fanático.",
        "comportamento": "Cruzados, hippies, ativistas, artistas apaixonados",
        "bonus": {"Forca_de_vontade": 1},  # Persistência
        "penalidade": {"Raciocinio": -1}  # Fanatismo cega
    },
    "Competidor": {
        "descricao": "Vive pela vitória. Cada desafio é uma competição.",
        "comportamento": "Atletas, empresários, pesquisadores obsessivos",
        "bonus": {"Destreza": 1, "Esportes": 1},
        "penalidade": {"Empatia": -1}  # Win-at-all-costs
    },
    "Conformista": {
        "descricao": "Segue o grupo. Prefere segurança à responsabilidade.",
        "comportamento": "Puxa-sacos, facções de eleitores, 'as massas'",
        "bonus": {"Etiqueta": 1, "Politica": 1},
        "penalidade": {"Lideranca": -1}  # Não assume comando
    },
    "Diretor": {
        "descricao": "Busca ordem e controle. 'À minha maneira ou de nenhuma'.",
        "comportamento": "Treinadores, professores, figuras políticas rígidas",
        "bonus": {"Organizacao": 1, "Investigacao": 1},
        "penalidade": {"Carisma": -1}  # Rígido demais
    },
    "Esperto": {
        "descricao": "Sempre encontra o caminho mais fácil. Trapaceiro nato.",
        "comportamento": "Criminosos, vendedores, moleques de rua",
        "bonus": {"Labia": 1, "Furtividade": 1},
        "penalidade": {"Coragem": -1}  # Evita confrontos diretos
    },
    "Excêntrico": {
        "descricao": "Fora do normal. Rejeita moralidade tradicional.",
        "comportamento": "Extremistas, celebridades excêntricas, gênios não reconhecidos",
        "bonus": {"Ocultismo": 1, "Ciencia": 1},
        "penalidade": {"Etiqueta": -1}  # Dificuldade social
    },
    "Fanático": {
        "descricao": "Consumido pela causa. O fim justifica os meios.",
        "comportamento": "Revolucionários, crentes fervorosos, incendiários",
        "bonus": {"Briga": 1, "Intimidacao": 1},
        "penalidade": {"Humanidade": -1}  # Perde fácil
    },
    "Filantropo": {
        "descricao": "Protege e nutre outros. Consolação.",
        "comportamento": "Médicos, enfermeiras, psiquiatras, mentores",
        "bonus": {"Medicina": 1, "Empatia": 2},
        "penalidade": {"Forca": -1}  # Dificuldade em ser duro
    },
    "Galante": {
        "descricao": "Busca ser centro das atenções. Sedutor.",
        "comportamento": "Artistas, filhos únicos, pessoas de baixa auto-estima",
        "bonus": {"Aparencia": 1, "Representacao": 1},
        "penalidade": {"Furtividade": -1}  # Não passa despercebido
    },
    "Gozador": {
        "descricao": "Tudo é piada. Alivia tensão com humor.",
        "comportamento": "Comediantes, irônicos, críticos sociais",
        "bonus": {"Labia": 1, "Prontidao": 1},
        "penalidade": {"Seriedade": -1}  # Não leva a sério
    },
    "Juiz": {
        "descricao": "Busca a decisão correta baseada em fatos.",
        "comportamento": "Engenheiros, advogados, médicos diagnósticos",
        "bonus": {"Investigacao": 1, "Raciocinio": 1},
        "penalidade": {"Carisma": -1}  # Frio demais
    },
    "Malandro": {
        "descricao": "Egoísta pragmático. O que é melhor pra mim?",
        "comportamento": "Prostitutas, capitalistas, criminosos calculistas",
        "bonus": {"Dinheiro": 1, "Intimidacao": 1},
        "penalidade": {"Lealdade": -1}  # Difícil confiar
    },
    "Mártir": {
        "descricao": "Sofre pela causa. Sacrifício puro.",
        "comportamento": "Inquisidores, idealistas, desterrados",
        "bonus": {"Coragem": 2, "Forca_de_vontade": 1},
        "penalidade": {"Saude": -1}  # Autossabotagem
    },
    "Masoquista": {
        "descricao": "Busca limites de dor. Testa si mesmo.",
        "comportamento": "Atletas extremistas, depressivos clínicos",
        "bonus": {"Vigor": 1, "Sobrevivencia": 1},
        "penalidade": {"Inteligencia": -1}  # Busca dor irracionalmente
    },
    "Monstro": {
        "descricao": "Sabe que é criatura das trevas. Age como tal.",
        "comportamento": "Sabbat degenerados, anciões insanos",
        "bonus": {"Briga": 2, "Intimidacao": 1},
        "penalidade": {"Humanidade": -2}  # Muito perdido
    },
    "Pedagogo": {
        "descricao": "Sabe de tudo e quer ensinar. Mentor.",
        "comportamento": "Professores, veteranos, 'super-instruídos'",
        "bonus": {"Instrucao": 2, "Sabedoria_popular": 1},
        "penalidade": {"Humildade": -1}  # Sabe demais, irrita
    },
    "Penitente": {
        "descricao": "Busca redenção pelo pecado. Autopunição.",
        "comportamento": "Pecadores arrependidos, criminosos com remorso",
        "bonus": {"Consciencia": 1, "Autocontrole": 1},
        "penalidade": {"Alegria": -1}  # Não se permite feliz
    },
    "Perfeccionista": {
        "descricao": "Exige o melhor. Métodos comprovados.",
        "comportamento": "Prima donnas, artistas, projetistas conceituais",
        "bonus": {"Artesanato": 1, "Ciencia": 1},
        "penalidade": {"Flexibilidade": -1}  # Não adapta
    },
    "Ranzinza": {
        "descricao": "Cínico amargo. Vê defeito em tudo.",
        "comportamento": "Anciões amargurados, adolescentes desiludidos",
        "bonus": {"Percepcao": 1, "Investigacao": 1},  # Ver a merda
        "penalidade": {"Carisma": -2}  # Insuportável
    },
    "Rebelde": {
        "descricao": "Descontente com o status quo. Odeia autoridade.",
        "comportamento": "Adolescentes, insurgentes, não-conformistas",
        "bonus": {"Briga": 1, "Lideranca": 1},
        "penalidade": {"Status": -1}  # Rejeitado pela sociedade
    },
    "Sobrevivente": {
        "descricao": "Persiste contra todas as adversidades.",
        "comportamento": "Desterrados, sem-teto, idealistas teimosos",
        "bonus": {"Sobrevivencia": 2, "Vigor": 1},
        "penalidade": {"Esperanca": -1}  # Pessimista
    },
    "Solitário": {
        "descricao": "Isolado por escolha. Não se encaixa.",
        "comportamento": "Criminosos, radicais, livres pensadores",
        "bonus": {"Furtividade": 1, "Autocontrole": 1},
        "penalidade": {"Carisma": -1}  # Difícil socializar
    },
    "Tradicionalista": {
        "descricao": "Prefere métodos comprovados. Conservador.",
        "comportamento": "Juízes, conservadores, autoridades",
        "bonus": {"Etiqueta": 1, "Tradicao": 1},
        "penalidade": {"Inovacao": -1}  # Resiste mudanças
    },
    "Valentão": {
        "descricao": "Robusto e ameaçador. Poder = direito.",
        "comportamento": "Ladrões, intolerantes, capangas, inseguros",
        "bonus": {"Forca": 1, "Intimidacao": 2},
        "penalidade": {"Inteligencia": -1}  # Brutal demais
    },
    "Visionário": {
        "descricao": "Vê além do óbvio. Sonhador inspirador.",
        "comportamento": "Filósofos, inventores, artistas visionários",
        "bonus": {"Inteligencia": 1, "Percepcao": 1},
        "penalidade": {"Praticidade": -1}  # Impraticável
    }
}