import WorkPath
import Installation

import os

if __name__ == '__main__':
    work_path = WorkPath.WorkPath()
    # revisions
    states = Installation.Installation(work_path.tmp_dir)

#import sys

#input_arg = str(sys.argv)
#process_arg = [str]

#print(process_arg)
