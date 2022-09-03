"""
pdb execRcLines doesn't take into consideration
the possibility that rclines call cmdloop which will then
take directly from stdin.  This allows such commands
to be placed in .pdbrc as well
"""
import io
import pdb
import sys

class Pdb(pdb.Pdb):
    def do_stopExecRcLines_(self, args):
        return 1

    def execRcLines(self):
        if not self.rcLines:
            return
        self.rcLines.append('stopExecRcLines_')
        stripped = [l.strip() for l in self.rcLines]
        newstdin = io.StringIO(
            '\n'.join([l for l in stripped if l and not l.startswith('#')]))
        if self.use_rawinput:
            orig = sys
        else:
            orig = self
        origstdin = orig.stdin
        orig.stdin = newstdin
        # Clear rclines to avoid repeating calls due to recursion.
        self.rcLines = []
        try:
            self.cmdloop()
            remain = list(newstdin)
            if remain:
                # maintain same behavior as before.
                # :-1 to exclude the appended stopexecrclines_ if it
                # remains unprocessed.  This handles the case where
                # .pdbrc ends with "continue" or some other similar
                # command.
                self.rcLines.extend(remain[:-1])
                return True
        finally:
            orig.stdin = origstdin

if __name__ == '__main__':
    # monkey patch
    from jhsiao.pdb import Pdb
    # use properly imported class instead of __main__.Pdb
    # or globals will be screwy
    pdb.Pdb = Pdb
    pdb.main()
