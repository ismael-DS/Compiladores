# Trabalho da disciplina de Compiladores
# Implementação de um analisador léxico usando expressões regulares (REGEX).
# Feito por:
# ISMAEL MESQUITA DE ARAUJO | Matrícula: 20210094680
# RUANDERSON GABRIEL ALVES DA SILVA COSTA DE FONTES | Matrícula: 20210024827

import re

class LexicalAnalyzer:
    def __init__(self, source_code):
        # Inicialização do analisador léxico
        self.source_code = source_code
        self.position = 0
        self.current_token = None
        # Conjuntos de palavras-chave, símbolos e operadores
        self.keywords = {'program', 'var', 'integer', 'real', 'boolean', 'procedure', 'begin', 'end', 'if', 'then', 'else', 'while', 'do', 'not'}
        self.symbols = {';', '.', ':', '(', ')', ','}
        self.operators_relational = {'=', '<', '>', '<=', '>=', '<>'}
        self.operators_additive = {'+', '-', 'or'}
        self.operators_multiplicative = {'*', '/', 'and'}
        # Tabela de símbolos
        self.symbol_table = []

    def get_next_token(self):
        # Obtém o próximo token no código-fonte
        while self.position < len(self.source_code) and (self.source_code[self.position].isspace() or self.source_code[self.position] == '{'):
            if self.source_code[self.position] == '{':
                # Ignora comentários delimitados por chaves
                self.position = self.source_code.find('}', self.position) + 1

            self.position += 1

        if self.position == len(self.source_code):
            return None

        for pattern, token_type in [
            (r'\b(program|var|integer|real|boolean|procedure|begin|end|if|then|else|while|do|not)\b', 'KEYWORD'),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),
            (r'\d+', 'INTEGER'),
            (r'\d+\.\d*', 'REAL'),
            (r':=', 'ASSIGNMENT'),
            (r';|\.|\:|\(|\)|\,', 'DELIMITER'),
            (r'=[<>]?|<>', 'RELATIONAL_OPERATOR'),
            (r'\+|-|or', 'ADDITIVE_OPERATOR'),
            (r'\*|/|and', 'MULTIPLICATIVE_OPERATOR')
        ]:
            regex = re.compile(pattern)
            match = regex.match(self.source_code, self.position)
            if match:
                value = match.group(0)
                self.position = match.end()

                if token_type == 'IDENTIFIER' and value.lower() in self.keywords:
                    token_type = 'KEYWORD'

                line = self.source_code.count('\n', 0, self.position) + 1
                self.symbol_table.append((value, token_type, line))

                return (value, token_type, line)

        # Se nenhum padrão for encontrado, levanta um erro
        raise Exception(f"Erro léxico: Símbolo não reconhecido em: {self.source_code[self.position:]}")

    def analyze(self):
        # Realiza a análise léxica e exibe os tokens encontrados
        while True:
            token = self.get_next_token()
            if token is not None:
                print(f"Token: {token[0]}, Tipo: {token[1]}, Linha: {token[2]}")
            else:
                break  # Termina o loop quando não há mais tokens

if __name__ == "__main__":
    # Código-fonte de exemplo
    source_code = """program teste; {programa exemplo}
    var
    valor1: integer;
    valor2: real;
    begin
    valor1 := 10;
    end.
    """

    # Criação e execução do analisador léxico
    lexer = LexicalAnalyzer(source_code)
    lexer.analyze()
