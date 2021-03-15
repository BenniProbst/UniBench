import WorkPath
import Installation
import Revision

if __name__ == '__main__':
    config_file_names = ['revison_setups', 'revisions']
    work_path = WorkPath.WorkPath('program')
    revisions = Revision.Revision(work_path.out(), config_file_names)
    var = {'Compilation Manager': {'replacements': 'There are {flag} pads for the compiler.',
                                   'file_name': 'compile', 'variation': ['{flag}']},
           'Thread Manager': {'replacements': 'There is a {threads} pad before running the program.',
                              'file_name': 'threads', 'variation': ['{threads}']},
           'Program Manager': {'replacements': 'There are two variation pads for the Program manager {flags} and {'
                                               'problem}. Both use text.',
                               'file_name': 'program', 'variation': ['{flags}', '{problem}']},
           }
    states = Installation.Installation(revisions.working_directory, var, config_file_names)
