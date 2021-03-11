import WorkPath
import Installation
import Revision


if __name__ == '__main__':
    work_path = WorkPath.WorkPath()
    revisions = Revision.Revision(work_path.tmp_dir)
    states = Installation.Installation(revisions)
