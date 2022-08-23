from argparse import ArgumentParser
import sys
from scanner import Scanner

has_error = False


class Plox:
    def __init__(self):
        self.has_error = False

    def run(self, source: str):
        scanner = Scanner(source)
        tokens, errors = scanner.scan_tokens()
        if len(errors) > 0:
            self.has_error = True
            for error in errors:
                print(error)

        for token in tokens:
            print(token)

    def run_prompt(self):
        while True:
            line = input("> ")
            if line == "":
                continue
            self.run(line)
            self.has_error = False

    def run_file(self, file: str):
        f = open(file)
        self.run(f.read())
        if has_error:
            sys.exit(65)

    @staticmethod
    def report(self, line: int, where: str, message: str):
        print("[line " + str(line) + "] Error" + where + ": " + message)
        self.has_error = True

    @staticmethod
    def error(self, line: int, message: str):
        self.report(line, "", message)


def main():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="file")
    args = parser.parse_args()

    plox = Plox()
    if len(args.__dict__) > 1:
        sys.exit(64)
    elif args.file:
        plox.run_file(args.file)
    else:
        plox.run_prompt()


if __name__ == "__main__":
    main()
