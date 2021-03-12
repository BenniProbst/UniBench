import WorkPath
import Installation
import Revision


if __name__ == '__main__':
    work_path = WorkPath.WorkPath()
    revisions = Revision.Revision(work_path.out())
    states = Installation.Installation(revisions)
