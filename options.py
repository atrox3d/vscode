import argparse
# import sys


def get_update_parser():
    # create parser
    parser = argparse.ArgumentParser(
        description="test parser"
    )

    parser.add_argument('-a', '--all', action='store_true', default=False)
    parser.add_argument('-p', '--pull', action='store_true', default=False)
    parser.add_argument('-P', '--push', action='store_true', default=False)
    parser.add_argument('-d', '--dryrun', action='store_true', default=False)
    parser.add_argument('-r', '--recurse', action='store_true', default=False)
    parser.add_argument('-c', '--commit')
    parser.add_argument('-w', '--workspace')

    return parser

def get_clone_parser():
    # create parser
    parser = argparse.ArgumentParser(
        description="test parser"
    )

    parser.add_argument('-d', '--dryrun', action='store_true', default=True)
    parser.add_argument('-r', '--recurse', action='store_true', default=True)
    parser.add_argument('-b', '--breakonerrors', action='store_true', default=True)
    parser.add_argument('-w', '--workspace', required=True)
    parser.add_argument('-j', '--json', required=True)

    return parser


if __name__ == '__main__':
    parser = get_update_parser()

    args: argparse.Namespace = parser.parse_args()

    for k, v in vars(args).items():
        print(f'{k} = {v}')
