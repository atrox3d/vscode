import atrox3d.simplegit as git

repos = git.repos.load('repos.json')
print(repos)

git.repos.restore('repos.json', r'd:\\test\\test\\test\\test')
