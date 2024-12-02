import os
from rich import print
from rich.panel import Panel
from rich.prompt import Prompt

from modules.checkForGitDir import checkForGitDir
from modules.checkIfPushNeeded import checkIfPushNeeded
from utils.decryptFiles import decryptFiles
from utils.encryptFiles import encryptFiles
from utils.tableMenu import tableMenu

user = os.getlogin()

commands = {
        '1': 'feat',
        '2': 'upd',
        '3': 'bug-fix',
        '4': 'fix',
        '5': 'core',
        }

def pushChanges(commit_message_param = ''):
    # show current path
    print(f'[green]Current path: {os.getcwd()}')
    choose = tableMenu()
    if choose in ['1', '2', '3', '4', '5']:
        commit_message = commit_message_param if commit_message_param != '' else Prompt.ask('Commit message: ')
        if commit_message == '':
            print('[red]Commit message is required')
            gitPush()
        git_command= f'git add . && git commit -m "{commands[choose]}: {commit_message}" && git push'
        os.system(git_command)
        print('[green]Done')
        decryptFiles()
    else:
        if choose == '6':
            os.system('lazygit')
            gitPush()
        elif choose == '7':
            print('[red]Bye')
            exit()
        else:
            print('[red]Invalid option')
            gitPush()

def gitModules():
    if os.path.exists('.gitmodules'):
        with open('.gitmodules') as f:
            lines = f.readlines()
            for line in lines:
                if 'path' in line:
                    path = line.split('=')[1].strip()
                    if path == 'libs' and os.path.exists('libs'):
                        os.chdir(path)
                        print(f'[green]Current path: {os.getcwd()}')
                        if checkForGitDir():
                            if checkIfPushNeeded():
                                pushChanges()
                                os.chdir('..')
                            else:
                                print('[red]No changes to commit')
                                os.chdir('..')
                        else:
                            print('[red]No git dir found')
                            os.chdir('..')
                    else:
                        print(f'[red]Path {path} not found')
                        print(f'[green]Current path: {os.getcwd()}')

def gitPush(commit_message = ''):
    print(Panel(f"Pushing from {os.getcwd()}", title="Git Push", style="blue"))
    if checkForGitDir():
        os.system('git status')
        gitModules()
        if os.path.exists('.gpgrc'):
            encryptFiles()
            if checkIfPushNeeded():
                pushChanges(commit_message_param=commit_message)
            else:
                print('[red]No changes to commit')
        else:
            if checkIfPushNeeded():
                pushChanges(commit_message_param=commit_message)
            else:
                print('[red]No changes to commit')

