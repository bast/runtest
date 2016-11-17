

Generated files
===============


The test script generates three files per run with the suffixes
".diff", ".filtered", and ".reference".

The ".filtered" file contains the extracted numbers from the present run.

The ".reference" file contains the extracted numbers from the reference file.

If the test passes, the ".diff" file is an empty file. If the test fails, it contains
information about the difference between the present run and the reference file.
