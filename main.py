import sys

import test_simplegit
import test_modules
import update_projects
import clone_projects

if __name__ == '__main__':
    sys.exit(
        clone_projects.main()
        # update_projects.main()
        )

