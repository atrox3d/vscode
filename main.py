import sys
import argparse

import test_simplegit
import test_modules
import update_projects
import clone_repos

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="main parser"
    )
    choices = {
        'update': update_projects,
        'clone': clone_repos,
        'simplegit': test_simplegit,
        'modules': test_modules
    }
    parser.add_argument(
                        'choice',
                        # nargs='?',
                        choices=choices.keys()
                        )
    
    parser.add_argument('rest', nargs='*')

    args, other = parser.parse_known_args()

    print(f'{args = }')
    for k, v in vars(args).items():
        print(f'{k} = {v}')
    
    print(sys.argv)
    sys.argv.pop(1)
    print(sys.argv)
    sys.exit(
        choices[args.choice].main()
        # update_projects.main()
        )

