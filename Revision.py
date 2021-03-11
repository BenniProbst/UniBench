import subprocess
import getpass


class Revision:
    suites = ''
    tests = ''

    def revision_setup(self, working_directory, program_url, username, password):
        while True:
            git_branch = input('Git branch: ')
            git_code = input('Git revision code: ')
            cmd1 = ['git', 'clone', '-n', program_url, ]
            rep = input('Add another revision code for testing? (y/n)')
            while not (rep == 'y' or rep == 'n'):
                print('What did you say?')
                rep = input('Add another revision code for testing? (y/n)')
            if rep == 'n':
                break

    def p_name(self,url):
        if str(url).endswith('.git'):
            url = str(url).removesuffix('.git')
        name = url.split("/")
        url = name[-1]
        if len(url) == 0:
            print('Failed to automatically retrieve project name, please set it now:')
            url = input('Manual project name: ')
        return url

    def __init__(self, working_directory):
        print('---Revision setup---')
        while True:
            print('Set platform login:')
            program_url = input('Git URL:')
            username = input('Target platform username: ')
            print('Target platform password: ')
            password = getpass()
            project_name = self.p_name(program_url)
            self.revision_setup(working_directory, program_url, username, password)
            rep = input('Add another revision source? (y/n)')
            while not (rep == 'y' or rep == 'n'):
                print('What did you say?')
                rep = input('Add another revision source? (y/n)')
            if rep == 'n':
                break
