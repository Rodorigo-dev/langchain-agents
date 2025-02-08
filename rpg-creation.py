from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração do modelo
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

# Template para gerar informações sobre as classes
class_info_template = """
Explique detalhadamente a classe de D&D chamada {classe}. Inclua:
- Um resumo da classe
- Principais habilidades e características
- Estilos de jogo recomendados
- Raças que combinam bem com essa classe
- Um exemplo de personagem famoso dessa classe
"""

# Função para obter informações sobre a classe
def get_class_info(classe):
    prompt = PromptTemplate(template=class_info_template, input_variables=["classe"])
    chain = LLMChain(llm=llm, prompt=prompt)
    
    return chain.invoke({"classe": classe})

# Função para criar o personagem com interação passo a passo
def create_character():
    print("\nVamos criar seu personagem de D&D! Responda as perguntas abaixo.\n")
    
    nome = input("1. Nome do personagem: ")
    raca = input("2. Raça (Humano, Elfo, Anão, etc.): ")
    
    # Permite que o usuário peça informações sobre classes antes de escolher
    while True:
        classe = input("3. Classe (Guerreiro, Mago, Clérigo, etc.) [Digite 'info' para saber mais]: ")
        if classe.lower() == "info":
            classe_desejada = input("Digite o nome da classe sobre a qual deseja mais informações: ")
            print(get_class_info(classe_desejada))
        else:
            break
    
    antecedente = input("4. Antecedente (Nobre, Forasteiro, etc.): ")
    
    print("\nAgora, digite os valores de 1 a 20 para os atributos:")
    forca = input("   - Força: ")
    destreza = input("   - Destreza: ")
    constituicao = input("   - Constituição: ")
    inteligencia = input("   - Inteligência: ")
    sabedoria = input("   - Sabedoria: ")
    carisma = input("   - Carisma: ")
    
    atributos = f"Força {forca}, Destreza {destreza}, Constituição {constituicao}, Inteligência {inteligencia}, Sabedoria {sabedoria}, Carisma {carisma}"
    alinhamento = input("\n5. Alinhamento (Leal e Bom, Neutro e Mau, etc.): ")

    # Gerar história do personagem com a IA
    history_template = """
    Baseado nas seguintes informações do personagem, crie um histórico envolvente:

    Nome: {nome}
    Raça: {raca}
    Classe: {classe}
    Antecedente: {antecedente}
    Atributos: {atributos}
    Alinhamento: {alinhamento}

    A história deve ser coerente com essas escolhas e refletir a personalidade do personagem.
    """

    prompt = PromptTemplate(template=history_template, input_variables=["nome", "raca", "classe", "antecedente", "atributos", "alinhamento"])
    chain = LLMChain(llm=llm, prompt=prompt)

    historia = chain.invoke({
        "nome": nome,
        "raca": raca,
        "classe": classe,
        "antecedente": antecedente,
        "atributos": atributos,
        "alinhamento": alinhamento
    })

    # Exibir o personagem criado
    print("\n✨ Seu personagem foi criado! ✨\n")
    print(f"🧝 Nome: {nome}")
    print(f"🔹 Raça: {raca}")
    print(f"⚔️ Classe: {classe}")
    print(f"📜 Antecedente: {antecedente}")
    print(f"🎲 Atributos: {atributos}")
    print(f"⚖️ Alinhamento: {alinhamento}")
    print(f"\n📖 História:\n{historia}")

# Ferramenta para o agente
tools = [
    Tool(
        name="Criar Personagem",
        func=create_character,
        description="Interage com o usuário para criar um personagem de D&D."
    ),
    Tool(
        name="Informação sobre Classes",
        func=get_class_info,
        description="Fornece informações detalhadas sobre qualquer classe de D&D."
    )
]

# Inicialização do agente
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

# Interação com o usuário
print("Bem-vindo ao assistente de criação de personagens de D&D!")
user_input = input("Vamos começar a criar seu personagem? Digite 'ok' para iniciar: ")

if user_input.lower() == "ok":
    create_character()
else:
    print("Ok, talvez na próxima vez.")
