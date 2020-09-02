#
# Runs all examples to make sure they don't return errors
#
# The code in this file is adapted from Pints
# (see https://github.com/pints-team/pints)
#
import re
import os
import sys
import subprocess


def run_notebook_and_scripts(executable="python"):
    """
    Runs example scripts and Jupyter notebooks. Exits if they fail.
    """
    # Scan and run
    print("Testing notebooks and scripts with executable `" + str(executable) + "`")
    if not scan_for_nb_and_scripts("docs/examples", True, executable):
        print("\nErrors encountered in notebooks")
        sys.exit(1)
    print("\nOK")


def scan_for_nb_and_scripts(root, recursive=True, executable="python"):
    """
    Scans for, and tests, all notebooks and scripts in a directory.
    """
    ok = True
    debug = False

    # Scan path
    for filename in os.listdir(root):
        path = os.path.join(root, filename)

        # Recurse into subdirectories
        if recursive and os.path.isdir(path):
            # Ignore hidden directories
            if filename[:1] == ".":
                continue
            ok &= scan_for_nb_and_scripts(path, recursive, executable)

        # Test notebooks
        if os.path.splitext(path)[1] == ".ipynb":
            if debug:
                print(path)
            else:
                ok &= test_notebook(path, executable)
        # Test scripts
        elif os.path.splitext(path)[1] == ".py":
            if debug:
                print(path)
            else:
                ok &= test_script(path, executable)

    # Return True if every notebook is ok
    return ok


def test_notebook(path, executable="python"):
    """
    Tests a single notebook, exists if it doesn't finish.
    """
    import nbconvert

    print("Test " + path + " ... ", end="")
    sys.stdout.flush()

    # Load notebook, convert to python
    e = nbconvert.exporters.PythonExporter()
    code, __ = e.from_filename(path)

    # Remove coding statement, if present
    code = "\n".join([x for x in code.splitlines() if x[:9] != "# coding"])

    # Tell matplotlib not to produce any figures
    env = dict(os.environ)
    env["MPLBACKEND"] = "Template"

    # If notebook makes use of magic commands then
    # the script must be ran using ipython
    # https://github.com/jupyter/nbconvert/issues/503#issuecomment-269527834
    executable = (
        "ipython"
        if (("run_cell_magic(" in code) or ("run_line_magic(" in code))
        else executable
    )

    # Run in subprocess
    cmd = [executable] + ["-c", code]
    try:
        p = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env
        )
        stdout, stderr = p.communicate()
        # TODO: Use p.communicate(timeout=3600) if Python3 only
        if p.returncode != 0:
            # Show failing code, output and errors before returning
            print("ERROR")
            print("-- script " + "-" * (79 - 10))
            for i, line in enumerate(code.splitlines()):
                j = str(1 + i)
                print(j + " " * (5 - len(j)) + line)
            print("-- stdout " + "-" * (79 - 10))
            print(str(stdout, "utf-8"))
            print("-- stderr " + "-" * (79 - 10))
            print(str(stderr, "utf-8"))
            print("-" * 79)
            return False
    except KeyboardInterrupt:
        p.terminate()
        print("ABORTED")
        sys.exit(1)

    # Sucessfully run
    print("ok")
    return True


def test_script(path, executable="python"):
    """
    Tests a single notebook, exists if it doesn't finish.
    """
    print("Test " + path + " ... ", end="")
    sys.stdout.flush()

    # Tell matplotlib not to produce any figures
    env = dict(os.environ)
    env["MPLBACKEND"] = "Template"

    # Run in subprocess
    cmd = [executable] + [path]
    try:
        p = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env
        )
        stdout, stderr = p.communicate()
        # TODO: Use p.communicate(timeout=3600) if Python3 only
        if p.returncode != 0:
            # Show failing code, output and errors before returning
            print("ERROR")
            print("-- stdout " + "-" * (79 - 10))
            print(str(stdout, "utf-8"))
            print("-- stderr " + "-" * (79 - 10))
            print(str(stderr, "utf-8"))
            print("-" * 79)
            return False
    except KeyboardInterrupt:
        p.terminate()
        print("ABORTED")
        sys.exit(1)

    # Sucessfully run
    print("ok")
    return True


def export_notebook(ipath, opath):
    """
    Exports the notebook at `ipath` to a python file at `opath`.
    """
    import nbconvert
    from traitlets.config import Config

    # Create nbconvert configuration to ignore text cells
    c = Config()
    c.TemplateExporter.exclude_markdown = True

    # Load notebook, convert to python
    e = nbconvert.exporters.PythonExporter(config=c)
    code, __ = e.from_filename(ipath)

    # Remove "In [1]:" comments
    r = re.compile(r"(\s*)# In\[([^]]*)\]:(\s)*")
    code = r.sub("\n\n", code)

    # Store as executable script file
    with open(opath, "w") as f:
        f.write("#!/usr/bin/env python")
        f.write(code)
    os.chmod(opath, 0o775)


if __name__ == "__main__":
    run_notebook_and_scripts()
