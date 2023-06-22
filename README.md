[![image](https://github.com/bast/runtest/workflows/Test/badge.svg)](https://github.com/bast/runtest/actions)
[![image](https://coveralls.io/repos/bast/runtest/badge.png?branch=main)](https://coveralls.io/r/bast/runtest?branch=main)
[![image](https://readthedocs.org/projects/runtest/badge/?version=latest)](http://runtest.readthedocs.io)
[![image](https://img.shields.io/badge/license-%20MPL--v2.0-blue.svg)](LICENSES/MPL-2.0.txt)
[![image](https://zenodo.org/badge/DOI/10.5281/zenodo.1069004.svg)](https://doi.org/10.5281/zenodo.1069004)
[![image](https://badge.fury.io/py/runtest.svg)](https://badge.fury.io/py/runtest)


# runtest

Numerically tolerant end-to-end test library for research software.

![image of a hardware circuit with red and green light bulbs](img/runtest-small.png)

Image: [Midjourney](https://midjourney.com/), [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/legalcode)


## Installation

```
$ pip install runtest
```


## Supported Python versions

The library is tested with Python 3.7, 3.8, 3.9, 3.10.  If you want to test
runtest itself on your computer, you can follow what we do in the [CI
workflow](https://github.com/bast/runtest/blob/main/.github/workflows/test.yml).


## Documentation

- [Latest code](http://runtest.readthedocs.io/en/latest/) (main branch)


Past versions
- [1.3.z](http://runtest.readthedocs.io/en/release-1.3.z/) ([release-1.3.z branch](https://github.com/bast/runtest/tree/release-1.3.z))


## Citation

For a recommended citation, please check the at the bottom-right of
<https://zenodo.org/record/3893712>.


## Projects using runtest

- [DIRAC](http://diracprogram.org)
- [Dalton](http://daltonprogram.org) and [LSDalton](http://daltonprogram.org)
- [GIMIC](https://github.com/qmcurrents/gimic)
- [OpenRSP](http://openrsp.org)
- [MRChem](https://mrchem.readthedocs.io/en/latest/)
- GRASP (General-purpose Relativistic Atomic Structure Program)
- [eT](https://etprogram.org)

If you use runtest, please add a link to your project via a pull
request.


## Similar projects

- [testcode](http://testcode.readthedocs.io) is a python module for
  testing for regression errors in numerical (principally scientific)
  software.
