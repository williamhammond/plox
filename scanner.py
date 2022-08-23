from typing import List

from errors import ParseError
from lox_token import LoxToken
from lox_token_type import LoxTokenType


class Scanner:
    _source = ""
    _keywords = {
        "and": LoxTokenType.AND,
        "class": LoxTokenType.CLASS,
        "else": LoxTokenType.ELSE,
        "false": LoxTokenType.FALSE,
        "fun": LoxTokenType.FUN,
        "for": LoxTokenType.FOR,
        "if": LoxTokenType.IF,
        "nil": LoxTokenType.NIL,
        "or": LoxTokenType.OR,
        "print": LoxTokenType.PRINT,
        "return": LoxTokenType.RETURN,
        "super": LoxTokenType.SUPER,
        "this": LoxTokenType.THIS,
        "true": LoxTokenType.TRUE,
        "var": LoxTokenType.VAR,
        "while": LoxTokenType.WHILE,
    }

    def __init__(self, source: str):
        self._source = source
        self._tokens = []
        self._errors = []
        self._start = 0
        self._current = 0
        self._line = 1

    def scan_tokens(self) -> (List[LoxToken], List[ParseError]):
        while not self.is_at_end():
            self._start = self._current
            self.scan_token()
        self._tokens.append(LoxToken(LoxTokenType.EOF, "", None, self._line))
        return self._tokens, self._errors

    def is_at_end(self) -> bool:
        return self._current >= len(self._source)

    def advance(self) -> str:
        temp = self._current
        self._current += 1
        return self._source[temp]

    def add_token(self, token_type: LoxTokenType, literal=None):
        text = self._source[self._start : self._current]
        if literal is not None:
            self._tokens.append(LoxToken(token_type, text, literal, self._line))
        else:
            self._tokens.append(LoxToken(token_type, text, None, self._line))

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self._source[self._current] != expected:
            return False

        self._current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self._source[self._current]

    def peek_next(self) -> str:
        if self._current + 1 >= len(self._source):
            return "\0"
        return self._source[self._current + 1]

    def number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

        self.add_token(
            LoxTokenType.NUMBER, float(self._source[self._start : self._current])
        )

    def is_alpha(self, s: str) -> bool:
        return ("a" <= s <= "z") or ("A" <= s <= "Z") or s == "_"

    def is_alpha_numeric(self, s: str) -> bool:
        return self.is_alpha(s) or s.isdigit()

    def identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()
        text = self._source[self._start : self._current]
        if text in self._keywords:
            token_type = self._keywords[text]
        else:
            token_type = LoxTokenType.IDENTIFIER
        self.add_token(token_type)

    def scan_token(self):
        c = self.advance()
        match c:
            case "(":
                self.add_token(LoxTokenType.LEFT_PAREN)
            case ")":
                self.add_token(LoxTokenType.RIGHT_PAREN)
            case "{":
                self.add_token(LoxTokenType.LEFT_BRACE)
            case "}":
                self.add_token(LoxTokenType.RIGHT_BRACE)
            case ",":
                self.add_token(LoxTokenType.COMMA)
            case ".":
                self.add_token(LoxTokenType.DOT)
            case "-":
                self.add_token(LoxTokenType.MINUS)
            case "+":
                self.add_token(LoxTokenType.PLUS)
            case ";":
                self.add_token(LoxTokenType.SEMICOLON)
            case "/":
                self.add_token(LoxTokenType.SLASH)
            case "*":
                self.add_token(LoxTokenType.STAR)
            case "!":
                self.add_token(
                    LoxTokenType.BANG_EQUAL if self.match("=") else LoxTokenType.BANG
                )
            case "=":
                self.add_token(
                    LoxTokenType.EQUAL_EQUAL if self.match("=") else LoxTokenType.EQUAL
                )
            case "<":
                self.add_token(
                    LoxTokenType.LESS_EQUAL if self.match("=") else LoxTokenType.LESS
                )
            case ">":
                self.add_token(
                    LoxTokenType.GREATER_EQUAL
                    if self.match("=")
                    else LoxTokenType.GREATER
                )
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(LoxTokenType.SLASH)
            case "\n":
                self._line += 1
            case " ":
                pass
            case "\t":
                pass
            case "\r":
                pass
            case _:
                if c.isdigit():
                    self.number()
                elif self.is_alpha(c):
                    self.identifier()
                else:
                    self._errors.append(ParseError("Unexpected character : " + c))
        pass
