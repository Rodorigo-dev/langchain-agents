from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from gerador_personagem import criar_personagem

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do modelo
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

if __name__ == "__main__":
    print("Bem-vindo ao assistente de criação de personagens de D&D!")
    user_input = input("Vamos começar a criar seu personagem? Digite 'ok' para iniciar: ").strip().lower()

    if user_input == "ok":
        personagem = criar_personagem(llm)
        print(personagem)
    else:
        print("Ok, até a próxima!")
