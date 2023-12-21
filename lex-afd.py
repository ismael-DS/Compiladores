# Trabalho da disciplina de Compiladores
# Implementação de um analisador léxico usando autômato finito determinístico.
# Feito por:
# ISMAEL MESQUITA DE ARAUJO | Matrícula: 20210094680
# RUANDERSON GABRIEL ALVES DA SILVA COSTA DE FONTES | Matrícula: 20210024827

class LexicalAnalyzer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        # Conjuntos de palavras-chave, símbolos e operadores
        self.keywords = {'program', 'var', 'integer', 'real', 'boolean', 'procedure', 'begin', 'end', 'if', 'then', 'else', 'while', 'do', 'not'}
        self.symbols = {';', '.', ':', '(', ')', ','}
        self.operators_relational = {'=', '<', '>', '<=', '>=', '<>'}
        self.operators_additive = {'+', '-', 'or'}
        self.operators_multiplicative = {'*', '/', 'and'}
        # Tabela de símbolos
        self.symbol_table = []

    def get_next_token(self):
        # Ignora espaços em branco e comentários
        while self.position < len(self.source_code) and (self.source_code[self.position].isspace() or self.source_code[self.position] == '{'):
            if self.source_code[self.position] == '{':
                # Ignora comentários delimitados por chaves
                self.position = self.source_code.find('}', self.position) + 1
            self.position += 1

        if self.position == len(self.source_code):
            return None

        current_char = self.source_code[self.position]

        if current_char.isalpha() or current_char == '_':
            return self.get_identifier_token()
        elif current_char.isdigit():
            return self.get_number_token()
        elif current_char in self.symbols:
            return self.get_symbol_token()
        elif current_char == ':' and self.source_code[self.position + 1] == '=':
            return self.get_assignment_token()
        elif current_char in ('<', '>') and self.source_code[self.position + 1] == '=':
            return self.get_relational_operator_token()
        elif current_char in ('=', '<>', '+', '-', '*', '/'):
            return self.get_operator_token()
        else:
            raise Exception(f"Erro léxico: Símbolo não reconhecido em: {self.source_code[self.position:]}")

    def get_identifier_token(self):
        # Obtém tokens para identificadores e palavras-chave
        start_position = self.position
        while self.position < len(self.source_code) and (self.source_code[self.position].isalnum() or self.source_code[self.position] == '_'):
            self.position += 1

        value = self.source_code[start_position:self.position]
        token_type = 'KEYWORD' if value.lower() in self.keywords else 'IDENTIFIER'
        line = self.source_code.count('\n', 0, start_position) + 1
        self.symbol_table.append((value, token_type, line))
        return value, token_type, line

    def get_number_token(self):
        # Obtém tokens para números inteiros e reais
        start_position = self.position
        while self.position < len(self.source_code) and self.source_code[self.position].isdigit():
            self.position += 1

        if self.source_code[self.position] == '.':
            self.position += 1
            while self.position < len(self.source_code) and self.source_code[self.position].isdigit():
                self.position += 1

        value = self.source_code[start_position:self.position]
        token_type = 'REAL' if '.' in value else 'INTEGER'
        line = self.source_code.count('\n', 0, start_position) + 1
        self.symbol_table.append((value, token_type, line))
        return value, token_type, line

    def get_symbol_token(self):
        # Obtém tokens para símbolos
        value = self.source_code[self.position]
        self.position += 1
        line = self.source_code.count('\n', 0, self.position) + 1
        self.symbol_table.append((value, 'DELIMITER', line))
        return value, 'DELIMITER', line

    def get_assignment_token(self):
        # Obtém tokens para o operador de atribuição
        value = self.source_code[self.position:self.position + 2]
        self.position += 2
        line = self.source_code.count('\n', 0, self.position) + 1
        self.symbol_table.append((value, 'ASSIGNMENT', line))
        return value, 'ASSIGNMENT', line

    def get_relational_operator_token(self):
        # Obtém tokens para operadores relacionais
        value = self.source_code[self.position:self.position + 2]
        self.position += 2
        line = self.source_code.count('\n', 0, self.position) + 1
        self.symbol_table.append((value, 'RELATIONAL_OPERATOR', line))
        return value, 'RELATIONAL_OPERATOR', line

    def get_operator_token(self):
        # Obtém tokens para operadores aritméticos
        value = self.source_code[self.position]
        self.position += 1
        operator_type = 'ADDITIVE_OPERATOR' if value in self.operators_additive else 'MULTIPLICATIVE_OPERATOR'
        line = self.source_code.count('\n', 0, self.position) + 1
        self.symbol_table.append((value, operator_type, line))
        return value, operator_type, line

    def analyze(self):
        # Realiza a análise léxica e exibe os tokens encontrados
        while True:
            token = self.get_next_token()
            if token is not None:
                print(f"Token: {token[0]}, Tipo: {token[1]}, Linha: {token[2]}")
            else:
                break

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

