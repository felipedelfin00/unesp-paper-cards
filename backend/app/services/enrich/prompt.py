def truncateMiddle(text, maxChars):
    #   Truncates the text from the middle (maitaining start and end),
    #   inserting ellipsis in the center.

    if not text:
        return ""

    if len(text) <= maxChars:
        return text

    ellipsis = "\n...\n"
    half = (maxChars - len(ellipsis)) // 2

    return text[:half] + ellipsis + text[-half:]


def buildPrompt(paper):
    #   Builds the prompt sent to the model to generate, based on the paper's title and abstract,
    #   an accessible-language version of the paper.

    abstract = truncateMiddle(paper.get("abstract", ""), 2000)

    return f"""
        Você é um jornalista muito experiente, especializado em divulgação científica, com domínio na escrita de textos acessíveis.
        Sua tarefa é extrair informações do título e do resumo de um trabalho acadêmico e transformar isso em informações para pessoas sem formação técnica.
        Responda apenas com JSON válido, sem texto antes ou depois.
        
        FORMATO OBRIGATÓRIO:
        {{
            "summary": "...",
            "socialRelevance": "...",
            "knowledgeArea": "...",
            "sdg": [
                {{
                    "number": 1,
                    "reason": "..."
                }}
            ],
            "theme": "..."
        }}
        
        REGRAS:
        - summary: entre 2 e 4 frases curtas, em português. Evite repetir o título, use linguagem acessível, evite jargões. Explique, quando possível, o problema abordado, como foi realizado, e o principal resultado.
        - socialRelevance: explique qual benefício prático o trabalho pode trazer para as pessoas, organizações ou para a sociedade, linguagem simples, máximo de 2 frases.
        - knowledgeArea: apenas uma área principal (ex: "Computação", "Saúde", "Educação"), em português. Não precisa estar na lista de temas.
        - sdg: lista com um ou mais ODS.
            - number: número da ODS relevante (ex: "4", "10"). Incluir apenas se realmente fizer sentido.
            - reason: motivo do por que atribuiu esse ODS ao trabalho.
        - theme: escolha exatamente um dos seguintes temas (não crie novos temas): computing, robotics, data, health, psychology, education, communication, culture, environment, agriculture, climate, biology, food, engineering, industry, energy, mobility, architecture, economics, business, law, public_policy, society, security, accessibility, chemistry, physics, mathematics.
        
        DADOS:
        - Título: {paper.get("title", "")}
        - Resumo: {abstract}  
    """
