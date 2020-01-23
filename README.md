# R2T2 - Research References Tracking Tool

The *Research References Tracking Tool (R2T2)* aims to fill the last remaining gap into the circle of open research, enabling not just publications to cite data or software (still a work in progress), but also the latter to cite the research articles containing the theory it codes, or the datasets it uses.

Some of the benefits of using *R2T2* in your project are:

- Facilitate giving credit to all the works software is based on. 
- Promote those works’ visibility and impact.
- Promote the transparency of the code: bi-directional link between theory and
 the specific code that implements it.
- Facilitate code maintenance and improve its sustainability.

## How it works

*R2T2* works by decorating those functions, classes or methods where
 particular algorithms described in a paper are implemented or data stored in
  a repository is used. General execution of code silently passes these
   decorators, but remembers how and where they were called. 
   The decorators include a short description of the thing being reference, and
    the reference itself in any sensible format.

```python
from r2t2 import add_reference
...
@add_reference(short_purpose="Original implementation of R2T2", 
                  reference="Diego Alonso-Álvarez, et al."
                            "(2018, February 27). Solcore (Version 5.1.0). Zenodo."
                            "http://doi.org/10.5281/zenodo.1185316")
def my_great_function():
    pass
```

Several references can be added by stacking multiple `@add_reference
` decorators.

```python
@add_reference(short_purpose="some comment",  reference="Reference 1")
@add_reference(short_purpose="another comment",  reference="Reference 2")
def my_great_function():
    pass
```

There are two methods of using this information:

### Runtime tracker

Which markers were passed when running a particular script `my_script.py` can be recalled with:
 
 ```bash 
$ python -m r2t2 my_script.py
```
 
This prints a list of markers passed in the script run and recursively in any
 dependency used by the program. Input arguments needed by the script can be
  added after its name.

 ```bash 
$ python -m r2t2 my_script.py arg1 arg2
```

### Static tracker

Alternatively, *R2T2* can be used to provide a list of all references that a
 given package is based on (i.e. ALL the `add_reference` decorators it contains
 ) and not just those crossed by a particular run of a script using the package.

For using this method, simply run in the terminal:

```bash 
$ python -m r2t2
```

which will scan all the python files recursively starting in the current
 directory. By default, it prints the results in the terminal. To analyse a single file, use the flag `-s` (from "static") to prevent r2t2 to treat it as a script to run:

 ```bash 
$ python -m r2t2 -s my_script.py
```
 
To have more control on what is scanned, the format of the output and where the
 output is written:

```bash 
$ python -m r2t2 -f markdown -o docs/list_of_references.md some/subdirectory 
```

The contents of the output will be organised by decorated object in the
 order they were encountered 
 and contain the line where the decorator was found, a link to that location, and the list of the short purposes and the references itself:

```markdown
Referenced in: roasted_chicken  
Source: [tests/test_r2t2.py](tests/test_r2t2.py:7)  
Line: 7

	[1] Roasted chicken recipe - Great British Roasts, 2019  
```

## Prior art

R2T2 is based in part on work done by Markus Führer at Imperial College London, as part of the [Solcore](https://github.com/qpv-research-group/solcore5) project.