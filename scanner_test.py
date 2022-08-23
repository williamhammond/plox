from scanner import Scanner
from lox_token import LoxToken
from lox_token_type import LoxTokenType
from errors import ParseError


class TestScanner:
    def test_numbers(self):
        scanner = Scanner(
            """1
            123.456
            .456
            123.
            """
        )
        tokens, errors = scanner.scan_tokens()
        assert len(errors) == 0

        assert len(tokens) == 7
        assert tokens[0] == LoxToken(LoxTokenType.NUMBER, "1", 1.0, 1)
        assert tokens[1] == LoxToken(LoxTokenType.NUMBER, "123.456", 123.456, 2)
        assert tokens[2] == LoxToken(LoxTokenType.DOT, ".", None, 3)
        assert tokens[3] == LoxToken(LoxTokenType.NUMBER, "456", 456.0, 3)
        assert tokens[4] == LoxToken(LoxTokenType.NUMBER, "123", 123.0, 4)
        assert tokens[5] == LoxToken(LoxTokenType.DOT, ".", None, 4)
        assert tokens[6] == LoxToken(LoxTokenType.EOF, "", None, 5)

    def test_identifier(self):
        scanner = Scanner("abc")

        tokens, errors = scanner.scan_tokens()
        assert len(errors) == 0
        assert len(tokens) == 2
        assert tokens[0] == LoxToken(LoxTokenType.IDENTIFIER, "abc", None, 1)
        assert tokens[1] == LoxToken(LoxTokenType.EOF, "", None, 1)

    def test_keywords(self):
        scanner = Scanner(
            "and class else false for fun if nil or return super this true var while"
        )

        tokens, errors = scanner.scan_tokens()

        assert len(errors) == 0

        assert len(tokens) == 16
        assert tokens[0] == LoxToken(LoxTokenType.AND, "and", "", 1)
        assert tokens[1] == LoxToken(LoxTokenType.CLASS, "class", "", 1)
        assert tokens[2] == LoxToken(LoxTokenType.ELSE, "else", "", 1)
        assert tokens[3] == LoxToken(LoxTokenType.FALSE, "false", "", 1)
        assert tokens[4] == LoxToken(LoxTokenType.FOR, "for", "", 1)
        assert tokens[5] == LoxToken(LoxTokenType.FUN, "fun", "", 1)
        assert tokens[6] == LoxToken(LoxTokenType.IF, "if", "", 1)
        assert tokens[7] == LoxToken(LoxTokenType.NIL, "nil", "", 1)
        assert tokens[8] == LoxToken(LoxTokenType.OR, "or", "", 1)
        assert tokens[9] == LoxToken(LoxTokenType.RETURN, "return", "", 1)
        assert tokens[10] == LoxToken(LoxTokenType.SUPER, "super", "", 1)
        assert tokens[11] == LoxToken(LoxTokenType.THIS, "this", "", 1)
        assert tokens[12] == LoxToken(LoxTokenType.TRUE, "true", "", 1)
        assert tokens[13] == LoxToken(LoxTokenType.VAR, "var", "", 1)
        assert tokens[14] == LoxToken(LoxTokenType.WHILE, "while", "", 1)
        assert tokens[15] == LoxToken(LoxTokenType.EOF, "", None, 1)

    def test_identifiers(self):
        scanner = Scanner(
            """andy formless fo _ _123 _abc ab123
               abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"""
        )

        tokens, errors = scanner.scan_tokens()
        assert len(errors) == 0

        assert tokens[0] == LoxToken(LoxTokenType.IDENTIFIER, "andy", None, 1)
        assert tokens[1] == LoxToken(LoxTokenType.IDENTIFIER, "formless", None, 1)
        assert tokens[2] == LoxToken(LoxTokenType.IDENTIFIER, "fo", None, 1)
        assert tokens[3] == LoxToken(LoxTokenType.IDENTIFIER, "_", None, 1)
        assert tokens[4] == LoxToken(LoxTokenType.IDENTIFIER, "_123", None, 1)
        assert tokens[5] == LoxToken(LoxTokenType.IDENTIFIER, "_abc", None, 1)
        assert tokens[6] == LoxToken(LoxTokenType.IDENTIFIER, "ab123", None, 1)
        assert tokens[7] == LoxToken(
            LoxTokenType.IDENTIFIER,
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_",
            None,
            2,
        )

    def test_punctuators(self):
        scanner = Scanner("(){};,+-*!===<=>=!=<>/.!")

        tokens, errors = scanner.scan_tokens()
        assert len(errors) == 0

        assert tokens[0] == LoxToken(LoxTokenType.LEFT_PAREN, "(", None, 1)
        assert tokens[1] == LoxToken(LoxTokenType.RIGHT_PAREN, ")", None, 1)
        assert tokens[2] == LoxToken(LoxTokenType.LEFT_BRACE, "{", None, 1)
        assert tokens[3] == LoxToken(LoxTokenType.RIGHT_BRACE, "}", None, 1)
        assert tokens[4] == LoxToken(LoxTokenType.SEMICOLON, ";", None, 1)
        assert tokens[5] == LoxToken(LoxTokenType.COMMA, ",", None, 1)
        assert tokens[6] == LoxToken(LoxTokenType.PLUS, "+", None, 1)
        assert tokens[7] == LoxToken(LoxTokenType.MINUS, "-", None, 1)
        assert tokens[8] == LoxToken(LoxTokenType.STAR, "*", None, 1)
        assert tokens[9] == LoxToken(LoxTokenType.BANG_EQUAL, "!=", None, 1)
        assert tokens[10] == LoxToken(LoxTokenType.EQUAL_EQUAL, "==", None, 1)
        assert tokens[11] == LoxToken(LoxTokenType.LESS_EQUAL, "<=", None, 1)
        assert tokens[12] == LoxToken(LoxTokenType.GREATER_EQUAL, ">=", None, 1)
        assert tokens[13] == LoxToken(LoxTokenType.BANG_EQUAL, "!=", None, 1)
        assert tokens[14] == LoxToken(LoxTokenType.LESS, "<", None, 1)
        assert tokens[15] == LoxToken(LoxTokenType.GREATER, ">", None, 1)
        assert tokens[16] == LoxToken(LoxTokenType.SLASH, "/", None, 1)
        assert tokens[17] == LoxToken(LoxTokenType.DOT, ".", None, 1)
        assert tokens[18] == LoxToken(LoxTokenType.BANG, "!", None, 1)
        assert tokens[19] == LoxToken(LoxTokenType.EOF, "", None, 1)

    def test_failure(self):
        scanner = Scanner("or and 1 :")
        tokens, errors = scanner.scan_tokens()

        assert len(errors) == 1
        assert type(errors[0]) is ParseError
