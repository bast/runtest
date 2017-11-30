

Run function arguments
======================

The ``run`` function has the following signature:

.. code-block:: python

  def run(options,
          configure,
          input_files,
          extra_args=None,
          filters=None,
          accepted_errors=None):
      ...

``options`` is set by the command line interface (by the user executing runtest).

``configure`` is specific to the code at hand (see the :ref:`example-test-script`).

``input_files`` contains the input files passed to the code launcher. The data structure of
``input_files`` is set by the ``configure`` function (in other words by the code using runtest).

There are three more optional arguments to the ``run`` function which by default are set to ``None``:

``extra_args`` contains extra arguments. Again, its data structure of
is set by the ``configure`` function (in other words by the code using runtest).

``filters`` is a dictionary of suffix and filter list pairs and contains
filters to apply to the results. If we omit to pass it, then the calculations
will be run but not verified. This is useful for multi-step jobs. See also the
:ref:`example-test-script`. If the ``output_prefix`` in the ``configure`` function is set to None,
then the filters are applied to the file names literally.
