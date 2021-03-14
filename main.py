import WorkPath
import Installation
import Revision

if __name__ == '__main__':
    work_path = WorkPath.WorkPath('program')
    revisions = Revision.Revision(work_path.out())
    var = {'Compilation Manager': {'replacements': 'There are no variation pads for the compiler.',
                                   'file_name': 'compile', 'variation': []},
           'Thread Manager': {'replacements': 'Type the thread modification command {threads} and type the number of '
                                              'test threads into the last line of the document. They will be '
                                              'recombined with all combinations above. If configuring multiple '
                                              'variations separate arguments with \';\' in the order of their '
                                              'registration list and separate varaitions to that argument type with '
                                              '\',\'. Example before running the application: export '
                                              'OMP_NUM_THREADS={threads} . Configuraion in last line may look like '
                                              'this: 2-6 or 1,2,3',
                              'file_name': 'threads', 'variation': ['{threads}']},
           'Program Manager': {'replacements': 'There are two variation pads for the Program manager. Both use text.',
                               'file_name': 'program', 'variation': ['{flags}', '{problem}']},
           }
    states = Installation.Installation(revisions.working_directory, var)
