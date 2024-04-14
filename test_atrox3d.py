from atrox3d.simplegit import git, repos

projects = repos.load('repos.json')
print(projects)

repos.restore('repos.json', r'd:\\test\\test\\test\\test')

