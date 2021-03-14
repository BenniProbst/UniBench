import getpass
import os
import LineSaver
import WorkPath
import shutil


class Revision:
    revision_setups_line = None
    working_directory = None

    def cmd_git(self, program_url, project_path, project_name, git_branch, git_code):
        # SHA Ziel ordner und repository universell einrichten, dass es herunterlädt
        commands = []
        cmd1 = 'git -C ' + project_path + '/' + project_name + '-' + git_branch + '-' + git_code + ' clone ' + \
               program_url
        commands.append(cmd1)
        cmd2 = 'git checkout ' + git_code
        commands.append(cmd2)
        return commands

    def revision_setup(self, program_url, username, password, project_path, project_name):
        print('---Revision setup---')
        if not os.path.isdir(project_path):
            print('Path does not exist and will be created: \n' + project_path)
        if not os.path.isdir(project_path):
            os.makedirs(project_path)
        os.chdir(project_path)
        local_saver_path = project_path + '/revisions'
        revisions_line = LineSaver.LineSaver(local_saver_path)
        login_keys = {'Username:': username, 'Password:': password}
        revision_count = 0
        while True:
            git_branch = ''
            git_code = ''
            commands = []
            revision_output_folder = ['']
            try:
                rep = ''
                if not revisions_line.is_empty() and revision_count == 0:
                    rep = input('The revision configuration file' + revisions_line.target_file +
                                'already exists. Do you want to replace it with a new configuration or add anything? '
                                '(y/n/add)')
                    while not (rep == 'y' or rep == 'n' or rep == 'add'):
                        print('What did you say?')
                        rep = input('The revision configuration file' + revisions_line.target_file +
                                    'already exists. Do you want to replace it with a new configuration or add '
                                    'anything? (y/n/add)')
                    if rep == 'y':
                        revisions_line.reset()
                        git_branch = input('Git branch: ')
                        git_code = input('Git revision SHA: ')
                        commands = self.cmd_git(program_url, project_path, project_name, git_branch, git_code)
                        revision_output_folder = [project_path + '/' + project_name + '-' + git_branch + '-' + git_code]
                        if not os.path.isdir(revision_output_folder[0]):
                            os.makedirs(revision_output_folder[0])
                        os.chdir(revision_output_folder[0])
                        revisions_line.append(revision_output_folder[0])
                    elif rep == 'add':
                        git_branch = input('Git branch: ')
                        git_code = input('Git revision SHA: ')
                        commands = self.cmd_git(program_url, project_path, project_name, git_branch, git_code)
                        revision_output_folder = [project_path + '/' + project_name + '-' + git_branch + '-' + git_code]
                        if revisions_line.exists(revision_output_folder[0]):
                            shutil.rmtree(revision_output_folder[0])
                            revisions_line.remove(revision_output_folder[0])
                        if not os.path.isdir(revision_output_folder[0]):
                            os.makedirs(revision_output_folder[0])
                        os.chdir(revision_output_folder[0])
                        revisions_line.append(revision_output_folder[0])
                        revision_output_folder = revisions_line.load_from_file()
                    elif rep == 'n':
                        os.chdir(project_path)
                        revision_output_folder = revisions_line.load_from_file()
                        break
                else:
                    git_branch = input('Git branch: ')
                    git_code = input('Git revision SHA: ')
                    commands = self.cmd_git(program_url, project_path, project_name, git_branch, git_code)
                    revision_output_folder = [project_path + '/' + project_name + '-' + git_branch + '-' + git_code]
                    if not os.path.isdir(revision_output_folder[0]):
                        os.makedirs(revision_output_folder[0])
                    os.chdir(revision_output_folder[0])
                    revisions_line.append(revision_output_folder[0])
                # for loop action check
                for rev in revision_output_folder:
                    print('--Revision command checker--')
                    command_saver_path = rev + '/git_commands'
                    console_config = LineSaver.SelectableLineSaver(command_saver_path)

                    if not console_config.is_empty_run():
                        rep = input('The revision run configuration file' + console_config.target_file +
                                    ' and its run configuration' + console_config.target_run +
                                    'already exists. Do you want to replace it with a new configuration? (y/n)')
                        while not (rep == 'y' or rep == 'n'):
                            print('What did you say?')
                            rep = input('The revision run configuration file' + console_config.target_file +
                                        ' and its run configuration' + console_config.target_run +
                                        'already exists. Do you want to replace it with a new configuration? (y/n)')
                        if rep == 'y':
                            console_config.reset_run()
                            console_config.configure(commands, login_keys)
                    else:
                        console_config.configure(commands, login_keys)
                    revision_count += 1

                os.chdir(project_path)
                rep = input('Add another revision code for testing? (y/n)')
                while not (rep == 'y' or rep == 'n'):
                    print('What did you say?')
                    rep = input('Add another revision code for testing? (y/n)')
                if rep == 'n':
                    break
            except Exception:
                print('Something went wrong! Deleting half finished revision folder!')
                os.chdir(project_path)
                shutil.rmtree(revision_output_folder[revision_count])
                if len(revisions_line.load_from_memory()) > 0:
                    rep = input('To correct the error type \'y\', to exit type \'n\'. (y/n)')
                    while not (rep == 'y' or rep == 'n'):
                        print('What did you say?')
                        rep = input('To correct the error type \'y\', to exit type \'n\'. (y/n)')
                    if rep == 'n':
                        break
        return True

    def p_name(self, url):
        if str(url).endswith('.git'):
            url = str(url).removesuffix('.git')
        name = url.split("/")
        url = name[-1]
        if len(url) == 0:
            print('Failed to automatically retrieve project name, please set it now:')
            url = input('Manual project name: ')
        return url

    def __init__(self, work_dir):
        self.working_directory = os.path.realpath(work_dir)
        saver_path = work_dir + '/revision_setups'
        self.revision_setups_line = LineSaver.LineSaver(saver_path)
        print('-----Revision setup-----')
        print('WARNING: ALL WORKING SOURCES (FOLDERS AND RECURSIVE FILES) WILL BE DELETED AN OVERWRITTEN TO UPDATE '
              'TEST PROPERTIES!!!')
        source_count = 0
        while True:
            print('----Online source setup----')
            print('Set platform login:')
            program_url = input('Git URL:')
            username = input('Target platform username: ')
            password = getpass.getpass(prompt='Target platform password: ')
            project_name = self.p_name(program_url)
            project_path = self.working_directory + '/' + project_name
            print('Default main project folder, named ' + project_name + ', where sub-revisions will be stored to:\n'
                  + project_path)
            use_default_project_name = input('Do you want to use the default path for revision enrollment inside of '
                                             'that directory? (y/n)')

            while not (use_default_project_name == 'y' or use_default_project_name == 'n'):
                print('What did you say?')
                print(
                    'Default main project folder, named ' + project_name + ', where sub-revisions will be stored to:\n'
                    + project_path)
                use_default_project_name = input('Do you want to use the default path for revision enrollment inside '
                                                 'of that directory? (y/n)')
            if use_default_project_name == 'n':
                project_path = WorkPath.WorkPath('project').out()
            if not self.revision_setups_line.is_empty() and source_count == 0:
                rep = input(
                    'The configuration file' + self.revision_setups_line.target_file + 'already exists. Do you want '
                                                                                       'to replace it with a new '
                                                                                       'configuration? (y/n)')
                while not (rep == 'y' or rep == 'n'):
                    print('What did you say?')
                    rep = input(
                        'The configuration file' + self.revision_setups_line.target_file + 'already exists. Do you '
                                                                                           'want to replace it with a'
                                                                                           ' new configuration? (y/n)')
                if rep == 'y':
                    self.revision_setups_line.reset()
                    self.revision_setups_line.append(project_path)
            else:
                self.revision_setups_line.append(project_path)
            self.revision_setup(program_url, username, password, project_path, project_name)
            source_count += 1
            rep = input('Add another revision source? (y/n)')
            while not (rep == 'y' or rep == 'n'):
                print('What did you say?')
                rep = input('Add another revision source? (y/n)')
            if rep == 'n':
                break
