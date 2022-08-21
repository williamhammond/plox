from argparse import ArgumentParser
import sys


def run(source):
    print(source)


def run_prompt():
    while True:
        line = input("> ")
        if line == "":
            continue
        run(line)


def run_file(file):
    f = open(file)
    run(f.read())


def main(name):
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="file")
    args = parser.parse_args()
    if len(args.__dict__) > 1:
        sys.exit(64)
    elif args.file:
        run_file(args.file)
    else:
        run_prompt()


if __name__ == "__main__":

    main("PyCharm")
