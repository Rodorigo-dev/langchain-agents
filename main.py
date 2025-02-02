import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool
from langchain.prompts import PromptTemplate
from pydantic import Field, BaseModel
from langchain_core.output_parsers import JsonOutputParser
from langchain.agents import Tool, create_openai_tools_agent, AgentExecutor

load_dotenv()


class ExtratorDeEstudante(BaseModel):
    estudante: str = Field("""Nome do estudante informado, sempre em letras minúsculas. Exemplo: joão, carlos, joana, carla""")

class DadosEstudante(BaseTool):
    name: str = "DadosEstudante" # Adicionando anotação de tipo
    description: str = " Esta ferramenta extrai o histórico e preferências de um estudante de acordo com seu histórico "

    def _run(self, input: str) -> str:
        llm = ChatOpenAI(model="gpt-4o-mini",
                        api_key = os.getenv("OPENAI_API_KEY"))
        parser = JsonOutputParser(pydantic_object=ExtratorDeEstudante)

        template = PromptTemplate(template=""" Você deve analisar o {input} para extrair o nome do usuario informado,
                                  Formato de saída: 
                                  {formato_saida}""",
                input_variables = ["input"],
                partial_variables = {"formato_saida" : parser.get_format_instructions()})
        cadeia = template | llm | parser
        resposta = cadeia.invoke({"input": input})
        return resposta['estudante']



pergunta = "Quais os dados do Rodrigo?"

llm = ChatOpenAI(model="gpt-4o-mini",
                        api_key = os.getenv("OPENAI_API_KEY"))

dados_de_estudante = DadosEstudante() # Instanciando a classe DadosEstudante

tools = [
    Tool(name = dados_de_estudante.name,
        func = dados_de_estudante.run,
        description = dados_de_estudante.description)
    ]

prompt = PromptTemplate(
    input_variables=["input", "agent_scratchpad"],
    template="""Você é um assistente útil. 
    Use as ferramentas disponíveis para responder ao usuário.
    
    Entrada do usuário: {input}

    {agent_scratchpad}"""
)


agente = create_openai_tools_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agente, tools=tools)

resposta = executor.invoke({"input" : pergunta})

#resposta = DadosEstudante().run(pergunta)
print(resposta)