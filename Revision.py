import os


class Revision:

    def revision_setup(self):
        program_url = input('Git URL:')

    def __init__(self):
        print('---Revision setup---')
        while True:
            self.revision_setup()
            if input('Add another program revision? (y/n): ') == 'n':
                break
