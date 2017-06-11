

Audience
========


Explain runtest in one sentence
-------------------------------

Runtest will assist you in running an entire calculation/simulation, extracting portions for the simulation outputs,
and comparing these portions with reference outputs and scream if the results have changed above a predefined numerical
tolerance.


When should one use runtest?
----------------------------

- You compute numerical results.
- You want a library that understands that floating point precision is limited.
- You want to be able to update tests by updating reference outputs.
- You look for an end-to-end testing support.


When should one not use runtest?
--------------------------------

- You look for a unit test library which tests single functions. Much better alternatives exist for this.
