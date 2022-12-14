import os
import sys
from jira import Jira
from git import Git
from conda import Conda


def main(project: str, env: str='', flag: str=''):
    company_name = os.environ['COMPANY_NAME']
    jira = Jira(
        url=os.environ['JIRA_URL'],
        user=os.environ['JIRA_USERNAME'],
        token=os.environ['JIRA_TOKEN'],
        project=project,
        status='"To Do"' if flag == 'start' else '"In Progress"'
    )
    if not jira.issues:
        return
    task = jira.issues[0]
    conda = Conda(env or project)
    git = Git(project, company_name)
    git.checkout(task.key)
    if flag == 'start':
        task.assign_to_me(jira)
        task.start(jira)
        git.pull()
    elif flag == 'end':
        task.end(jira)
        git.commit(task.fields.summary)
        git.push()
        conda.deactivate()


print('AUTO'.center(50, '-'))
print('-' * 50)
if len(sys.argv) < 3:
    print('Usage: python3 AUTO <project> <env> [start/end]')
else:
    params = [a for i, a in enumerate(sys.argv) if i > 0]
    main(*params)
