def my_great_function():
    """
    Original implementation of R2T2
    Diego Alonso-Álvarez, et al.
    (2018, February 27). Solcore (Version 5.1.0). Zenodo.
    http://doi.org/10.5281/zenodo.1185316
    """
    pass

if __name__ == "__main__":
    import os

    # run static to avoid infinite loop
    os.system("python3 -m r2t2 -s --docstring docs/examples/reference_docstring.py")