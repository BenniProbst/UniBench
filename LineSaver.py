import os
from pathlib import Path
import pickle


class LineSaver:
    target_file = Path(os.path.expanduser("~") + '/noname.UniBench_config')

    def __init__(self, t_f):
        self.target_file = Path(t_f)
        working_dir = Path(os.path.dirname(self.target_file.absolute()))
        if not os.path.isdir(working_dir):
            os.makedirs(working_dir)
        if not os.path.isfile(self.target_file):
            with open(self.target_file, 'w') as f:
                pickle.dump([''], f)

    def save(self, listing):
        with open(self.target_file, 'wb') as f:
            pickle.dump(listing, f)

    def load(self):
        with open(self.target_file, 'rb') as f:
            return pickle.load(f)
