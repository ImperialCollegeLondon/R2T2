# R2T2 - Research References Tracking Tool

The *Research References Tracking Tool (R2T2)* aims to fill the last remaining gap into the circle of open research, enabling not just publications to cite data or software (still a work in progress), but also the latter to cite the research articles containing the theory it codes, or the datasets it uses.

Some of the benefits of using *R2T2* in your project are:

- Give credit to all the works a given research software is based on.
- Promote those works visibility and impact.
- Promote the transparency of the code.
- Facilitate reviewing the agreement between the theory and/or maths contained in the papers and the code implementation.
- Facilitate code maintenance and improve its sustainability.

## How it works

*R2T2* works by introducing markers in the code where particular algorithms or data are implemented. General execution of code silently passes these markers, but remembers how and where they were called. The markers include a short description of the thing being reference, and the reference itself in any sensible format.

```python
from r2t2 import science_reference
...
science_reference(short_purpose="Original implementation of R2T2", 
                  reference="Diego Alonso-Álvarez, Thomas Wilson, Phoebe Pearce," 
                            "Markus Führer, Daniel Farrell, & Nicholas Ekins-Daukes."
                            "(2018, February 27). Solcore (Version 5.1.0). Zenodo."
                            "http://doi.org/10.5281/zenodo.1185316")
```

There are two methods of using this information:

Which markers were passed in a particular program run can be recalled with `r2t2.print_references()`. This includes recursively markers passed in any dependency used by the program.

Alternatively, *R2T2* can be used to provide a list of all references that a given package is based on (i.e. ALL the `science_reference` markers it contains) and not just those crossed by a particular run of a script using the package. This method is the most useful one to fulfill the aims of *R2T2*described above

For using this method, simply run in the terminal:

```bash 
$ python -m r2t2
```

which will scan all the python files recursively starting in the current directory and write the results in `references.md`. To have more control on what is scanned and where the output is written:

```bash 
$ python -m r2t2 -i some/subdirectory/or/file -o docs/references.md
```

The contents of the output file will be organised by module and contain the line where the marker was found, the short purpose and the reference itself:

```markdown
1. [test_r2t2](tests/test_r2t2.py) - Line=3  
	Short purpose: doing something smart  
	Reference: My Awesome Book, by me.  

2. [test_r2t2](tests/test_r2t2.py) - Line=4  
	Short purpose: doing something smart in two lines  
	Reference: Another Awesome Book, by me, 2019  
```

## Prior art

R2T2 is based in part on work done by Markus Führer at Imperial College London, as part of the [Solcore](https://github.com/qpv-research-group/solcore5) project.