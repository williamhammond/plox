from lox_token_type import LoxTokenType


class LoxToken:
    def __init__(self, token_type: LoxTokenType, lexeme: str, literal, line: int):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return str(self.token_type) + " " + self.lexeme + " " + str(self.literal)
