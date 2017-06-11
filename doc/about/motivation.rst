

Motivation
==========


Scope
-----

When testing numerical codes against functionality regression, you typically
cannot use a plain diff against the reference outputs due to numerical noise in
the digits and because there may be many numbers that change all the time and
that you do not want to test (e.g. date and time of execution).

The aim of this library is to make the testing and maintenance of tests easy.
The library allows to extract portions of the program output(s) which are
automatically compared to reference outputs with a relative or absolute
numerical tolerance to compensate for numerical noise due to machine precision.


Design decisions
----------------

The library is designed to play well with CTest, to be convenient when used
interactively, and to work without trouble on Linux, Mac, and Windows. It
offers a basic argument parsing for test scripts.
