class Personagem:
    def __init__(self, nome, raca, classe, antecedente, atributos, alinhamento, historia=""):
        self.nome = nome
        self.raca = raca
        self.classe = classe
        self.antecedente = antecedente
        self.atributos = atributos
        self.alinhamento = alinhamento
        self.historia = historia

    def __str__(self):
        return f"""
        ✨ Seu personagem foi criado! ✨
        🧝 Nome: {self.nome}
        🔹 Raça: {self.raca}
        ⚔️ Classe: {self.classe}
        📜 Antecedente: {self.antecedente}
        🎲 Atributos: {self.atributos}
        ⚖️ Alinhamento: {self.alinhamento}
        📖 História:
        {self.historia}
        """
