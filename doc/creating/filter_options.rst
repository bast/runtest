

Filter options
==============


Relative tolerance
------------------

There is no default. You have to select either relative or absolute tolerance
for each test when testing floats. You cannot select both at the same time.

In this example we set the relative tolerance to 1.0e-10:

.. code-block:: python

  get_filter(from_string='Electronic energy',
             num_lines=8,
             rel_tolerance=1.0e-10)


Absolute tolerance
------------------

There is no default. You have to select either relative or absolute tolerance
for each test when testing floats. You cannot select both at the same time.

In this example we set the absolute tolerance to 1.0e-10:

.. code-block:: python

  get_filter(from_string='Electronic energy',
             num_lines=8,
             abs_tolerance=1.0e-10)


How to check entire file
------------------------

By default all lines are tested so if you omit any string anchors and number of
lines we will compare numbers from the entire file.

Example:

.. code-block:: python

  get_filter(rel_tolerance=1.0e-10)


Filtering between two anchor strings
------------------------------------

Example:

.. code-block:: python

  get_filter(from_string='@   Elements of the electric dipole',
             to_string='@   anisotropy',
             rel_tolerance=1.0e-10)

This will extract all floats between these strings including the lines of the
strings.

The start/end strings can be regular expressions, for this use from_re or
to_re. Any combination containing from_string/from_re and to_string/to_re is
possible.


Filtering a number of lines starting with string/regex
------------------------------------------------------

Example:

.. code-block:: python

  get_filter(from_string='Electronic energy',
             num_lines=8,  # here we compare 8 lines
             abs_tolerance=1.0e-10)

The start string can be a string (from_string) or a regular expression
(from_re).  In the above example we extract and compare all lines that start
with 'Electronic energy' including the following 7 lines.


Extracting single lines
-----------------------

This example will compare all lines which contain 'Electronic energy':

.. code-block:: python

  get_filter(string='Electronic energy',
             abs_tolerance=1.0e-10)

This will match the string in a *case-sensitive* fashion.

Instead of single string we can give a single regular expression (re).

.. code-block:: python

  get_filter(re='Electronic energy',
             abs_tolerance=1.0e-10)

Regexes follow the `Python syntax <https://docs.python.org/3/library/re.html#regular-expression-syntax>`_.
For example, to match in a *case-insensitive* fashion:

.. code-block:: python

  get_filter(re=r'(?i)Electronic energy',
             abs_tolerance=1.0e-10)

It is not possible to use Python regex objects directly.


How to ignore sign
------------------

Sometimes the sign is not predictable. For this set ``ignore_sign=True``.


How to ignore the order of numbers
----------------------------------

Setting ``ignore_order=True`` will sort the numbers (as they appear consecutively
between anchors, one after another) before comparing them.
This is useful for tests where some numbers can change place.


How to ignore very small or very large numbers
----------------------------------------------

You can ignore very small numbers with skip_below.
Default is 1.0e-40. Ignore all floats that are smaller than this number
(this option ignores the sign).

As an example consider the following result tensor::

        3716173.43448289          0.00000264         -0.00000346
             -0.00008183      75047.79698485          0.00000328
              0.00003493         -0.00000668      75047.79698251

              0.00023164    -153158.24017016         -0.00000493
          90142.70952070         -0.00000602          0.00000574
              0.00001946         -0.00000028          0.00000052

              0.00005844         -0.00000113    -153158.24017263
             -0.00005667          0.00000015         -0.00000022
          90142.70952022          0.00000056          0.00000696

The small numbers are actually numerical noise and we do not want to test them
at all. In this case it is useful to set ``skip_below=1.0e-4``.

Alternatively one could use absolute tolerance to avoid checking the noisy
zeros.

You can ignore very large numbers with skip_above (also this option ignores
the sign).


How to ignore certain numbers
-----------------------------

The keyword mask is useful if you extract lines which contain both interesting
and uninteresting numbers (like timings which change from run to run).

Example:

.. code-block:: python

  get_filter(from_string='no.    eigenvalue (eV)   mean-res.',
             num_lines=4,
             rel_tolerance=1.0e-4,
             mask=[1, 2, 3])

Here we use only the first 3 floats in each line. Counting starts with 1.
