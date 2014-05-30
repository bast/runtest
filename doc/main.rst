

About the runtest library
=========================


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

The library is desinged to play well with CTest, to be convenient when used
interactively, and to work without trouble on Linux, Mac, and Windows. It
offers test scripts a basic argument parsing. All host program independent code
has been collected into the core library. The aim is to keep host program
specifics minimal and to specify and keep them in adapter scripts outside the
core library.
