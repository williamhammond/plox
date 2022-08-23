from functools import total_ordering

from lox_token_type import LoxTokenType


class LoxToken:
    def __init__(self, token_type: LoxTokenType, lexeme: str, literal, line: int):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return (
            str(self.line)
            + " "
            + str(self.token_type)
            + " "
            + self.lexeme
            + " "
            + str(self.literal)
        )

    def __eq__(self, other):
        return (self.token_type, self.lexeme, self.literal, self.line) == (
            other.token_type,
            other.lexeme,
            other.literal,
            other.line,
        )
