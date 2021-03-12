import LineSaver
from pathlib import Path
import pickle
import os


class SelectableLineSaver(LineSaver):
    target_run = Path(os.path.expanduser("~") + '/noname.UniBench_config_run')
    in_memory_run = []

    def __init__(self, t_f):
        super().__init__(self, t_f)
        self.target_run = Path(t_f + '.UniBench_config_run')
        if not os.path.isfile(self.target_run):
            with open(self.target_run, 'w') as f:
                pickle.dump(self.in_memory, f)
        self.in_memory = self.load_from_file()
