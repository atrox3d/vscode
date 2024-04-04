import argparse
# import sys


def get_parser():
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


if __name__ == '__main__':
    parser = get_parser()

    args: argparse.Namespace = parser.parse_args()

    for k, v in vars(args).items():
        print(f'{k} = {v}')
