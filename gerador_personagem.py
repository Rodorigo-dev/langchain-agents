from personagem import Personagem
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

def criar_personagem(llm):
    nome = input("1. Nome do personagem: ").strip()
    raca = input("2. Raça: ").strip()
    classe = input("3. Classe: ").strip()
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
