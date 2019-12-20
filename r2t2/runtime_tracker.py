from .r2t2 import track_science, print_references
import sys
import os


def runtime_tracker(script, args):
    track_science()

    sys.argv = [script, *args]
    sys.path[0] = os.path.dirname(script)

    try:
        with open(script) as fp:
            code = compile(fp.read(), script, "exec")

        # try to emulate __main__ namespace as much as possible
        # What trace python module uses https://docs.python.org/3.7/library/trace.html
        globs = {
            "__file__": script,
            "__name__": "__main__",
            "__package__": None,
            "__cached__": None,
        }
        exec(code, globs, globs)

    except OSError as err:
        sys.exit("Cannot run file %r because: %s" % (sys.argv[0], err))

    except SystemExit:
        pass

    print_references()
