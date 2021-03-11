import subprocess
import getpass


class Revision:
    suites = ''
    tests = ''

    def revision_setup(self, working_directory, program_url, username, password, project_name):
        while True:
            git_branch = input('Git branch: ')
            git_code = input('Git revision code: ')
            cmd0 = ['cd', '\"' + working_directory + '\"']
            cmd1 = ['git', 'clone', '-n', program_url,
                    working_directory + '/' + project_name + '-' + git_branch + '-' + git_code]
            cmd2 = ['git', 'checkout', git_code]
            process = subprocess.Popen(cmd0, shell=True, stdout=subprocess.PIPE)
            process.wait()
            out = []
            for line in process.stdout:
                out.append(line)
            process = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE)
            process.wait()
            out = []
            for line in process.stdout:
                out.append(line)
            process = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE)
            process.wait()
            out = []
            for line in process.stdout:
                out.append(line)

            rep = input('Add another revision code for testing? (y/n)')
            while not (rep == 'y' or rep == 'n'):
                print('What did you say?')
                rep = input('Add another revision code for testing? (y/n)')
            if rep == 'n':
                break

    def p_name(self, url):
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
            password = getpass.getpass(prompt='Target platform password: ')
            project_name = self.p_name(program_url)
            self.revision_setup(working_directory, program_url, username, password, project_name)
            rep = input('Add another revision source? (y/n)')
            while not (rep == 'y' or rep == 'n'):
                print('What did you say?')
                rep = input('Add another revision source? (y/n)')
            if rep == 'n':
                break
