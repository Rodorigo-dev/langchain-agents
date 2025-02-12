from personagem import Personagem
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

OPCOES_RACAS = ["Humano", "Elfo", "Anão", "Halfling", "Draconato", "Gnomo", "Meio-Orc", "Meio-Elfo", "Tiefling"]
OPCOES_CLASSES = ["Guerreiro", "Mago", "Ladino", "Clérigo", "Bardo", "Paladino", "Druida", "Feiticeiro", "Bruxo", "Monge"]

def obter_info_raca(llm, raca):
    """Obtém informações detalhadas sobre uma raça de D&D usando a IA."""
    raca_info_template = """
    Explique detalhadamente a raça de D&D chamada {raca}. Inclua:
    - Um resumo da raça
    - Principais características e habilidades
    - Quais classes combinam bem com essa raça
    - Um exemplo de personagem famoso dessa raça
    """

    prompt = PromptTemplate(template=raca_info_template, input_variables=["raca"])
    chain = LLMChain(llm=llm, prompt=prompt)

    return chain.invoke({"raca": raca})

def obter_info_classe(llm, classe):
    """Obtém informações detalhadas sobre uma classe de D&D usando a IA."""
    class_info_template = """
    Explique detalhadamente a classe de D&D chamada {classe}. Inclua:
    - Um resumo da classe
    - Principais habilidades e características
    - Estilos de jogo recomendados
    - Raças que combinam bem com essa classe
    - Um exemplo de personagem famoso dessa classe
    """

    prompt = PromptTemplate(template=class_info_template, input_variables=["classe"])
    chain = LLMChain(llm=llm, prompt=prompt)

    return chain.invoke({"classe": classe})

def criar_personagem(llm):
    """Interage com o usuário para criar um personagem de D&D."""
    nome = input("1. Nome do personagem: ").strip()
    
    print("\nOpções de Raça disponíveis:")
    print(", ".join(OPCOES_RACAS))

    while True:
        raca = input("2. Escolha uma raça (ou digite 'info' para saber mais): ").strip()
        if raca.lower() == "info":
            raca_desejada = input("Digite o nome da raça sobre a qual deseja mais informações: ").strip()
            if raca_desejada in OPCOES_RACAS:
                print("\n🔍 Informações sobre a raça:\n")
                print(obter_info_raca(llm, raca_desejada))
            else:
                print("Raça não encontrada. Tente novamente.")
        elif raca in OPCOES_RACAS:
            break
        else:
            print("Raça inválida. Escolha uma das opções listadas.")

    print("\nOpções de Classe disponíveis:")
    print(", ".join(OPCOES_CLASSES))

    while True:
        classe = input("3. Escolha uma classe (ou digite 'info' para saber mais): ").strip()
        if classe.lower() == "info":
            classe_desejada = input("Digite o nome da classe sobre a qual deseja mais informações: ").strip()
            if classe_desejada in OPCOES_CLASSES:
                print("\n🔍 Informações sobre a classe:\n")
                print(obter_info_classe(llm, classe_desejada))
            else:
                print("Classe não encontrada. Tente novamente.")
        elif classe in OPCOES_CLASSES:
            break
        else:
            print("Classe inválida. Escolha uma das opções listadas.")

    antecedente = input("4. Antecedente: ").strip()

    atributos = {}
    for atributo in ["Força", "Destreza", "Constituição", "Inteligência", "Sabedoria", "Carisma"]:
        while True:
            valor = input(f"   - {atributo}: ").strip()
            if valor.isdigit() and 1 <= int(valor) <= 20:
                atributos[atributo] = int(valor)
                break
            else:
                print("Por favor, insira um valor numérico entre 1 e 20.")

    alinhamento = input("\n5. Alinhamento: ").strip()
    
    atributos_formatados = ", ".join(f"{k} {v}" for k, v in atributos.items())

    # Geração da história com IA
    history_template = """Baseado nas seguintes informações do personagem, crie um histórico envolvente:
    Nome: {nome}
    Raça: {raca}
    Classe: {classe}
    Antecedente: {antecedente}
    Atributos: {atributos}
    Alinhamento: {alinhamento}
    """

    prompt = PromptTemplate(template=history_template, input_variables=["nome", "raca", "classe", "antecedente", "atributos", "alinhamento"])
    chain = LLMChain(llm=llm, prompt=prompt)
    
    historia = chain.invoke({
        "nome": nome,
        "raca": raca,
        "classe": classe,
        "antecedente": antecedente,
        "atributos": atributos_formatados,
        "alinhamento": alinhamento
    })

    return Personagem(nome, raca, classe, antecedente, atributos_formatados, alinhamento, historia)
