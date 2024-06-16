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
    parser.add_argument('-s', '--skipclean', action='store_true', default=False)
    parser.add_argument('-l', '--listrepos', action='store_true', default=False)
    parser.add_argument('-c', '--commit')
    parser.add_argument('-w', '--workspace')
    parser.add_argument('-g', '--grep', action='extend', nargs='+', type=str, default=[],
                        help='include only repos containig one of the strings')
    parser.add_argument('-e', '--exclude', action='extend', nargs='+', type=str, default=[],
                        help='exclude repos containig one of the strings')

    return parser

def get_clone_parser():
    # create parser
    parser = argparse.ArgumentParser(
        description="test parser"
    )

    
    subparsers = parser.add_subparsers(
                                        dest='command', 
                                        help='Commands to run', 
                                        required=True
                                        )

    backup = subparsers.add_parser('backup')
    backup.add_argument('-w', '--workspace', required=True)
    backup.add_argument('-j', '--json', required=True)
    backup.add_argument('-r', '--recurse', action='store_true', default=False)

    restore = subparsers.add_parser('restore')
    restore.add_argument('-d', '--dryrun', action='store_false', default=True)
    restore.add_argument('-j', '--json', required=True)
    restore.add_argument('-p', '--destpath', required=True)
    restore.add_argument('-b', '--breakonerrors', action='store_true', 
                         default=False, help='break on errors if specified')

    return parser


if __name__ == '__main__':
    parser = get_clone_parser()

    args: argparse.Namespace = parser.parse_args()

    print(f'{args = }')
    for k, v in vars(args).items():
        print(f'{k} = {v}')
