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
reference="Diego Alonso-Álvarez, Thomas Wilson, Phoebe Pearce, Markus Führer, Daniel Farrell, & Nicholas Ekins-Daukes. (2018, February 27). Solcore (Version 5.1.0). Zenodo. http://doi.org/10.5281/zenodo.1185316")
```

Which markers were passed in a particular program run can be recalled with `r2t2.print_references()`. 

## Next steps

*R2T2* was designed initially to find out the scientific references that a given script using [Solcore](https://github.com/qpv-research-group/solcore5) was benefiting from. While useful, this is somewhat restrictive.

The immediate goal for *R2T2* is to be able to provide a list of all references that a given piece of package is based on (i.e. ALL the `science_reference` markers it contains) and not just those crossed by a particular run of a script using the package. 

## Prior art

R2T2 is based in part on work done by Markus Führer at Imperial College London, as part of the [Solcore](https://github.com/qpv-research-group/solcore5) project.