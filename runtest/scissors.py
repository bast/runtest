import re


def cut_sections(
    text,
    from_string=None,
    from_is_re=False,
    to_string=None,
    to_is_re=False,
    num_lines=0,
    certain_occurrences=None,
):
    """
    Cuts out sections of the text between anchors.

    Returns:
        output - list of remaining lines
    """
    output = []
    occurrence = 0

    for i, _ in enumerate(text):

        start_line_matches = False
        if from_is_re:
            start_line_matches = re.match(r".*{0}".format(from_string), text[i])
        else:
            if from_string is None:
                # we are comparing entire file
                return text
            else:
                start_line_matches = from_string in text[i]

        if certain_occurrences and start_line_matches:
            start_line_matches = False
            occurrence += 1
            if occurrence in certain_occurrences:
                start_line_matches = True

        if start_line_matches:
            if num_lines > 0:
                for n in range(i, i + num_lines):
                    output.append(text[n])
            else:
                for j in range(i, len(text)):

                    end_line_matches = False
                    if to_is_re:
                        end_line_matches = re.match(r".*{0}".format(to_string), text[j])
                    else:
                        end_line_matches = to_string in text[j]

                    if end_line_matches:
                        for n in range(i, j + 1):
                            output.append(text[n])
                        return output

    return output


def test_cut_sections():

    text = """
1.0 2.0 3.0
1.0 2.0 3.0
1.0 2.0 3.0
1.0 2.0 3.0
1.0 2.0 3.0
1.0 2.0 3.0
1.0 2.0 3.0
raboof 1.0 3.0 7.0
       1.0 3.0 7.0
       1.0 3.0 7.0
       1.0 3.0 7.0
       1.0 3.0 7.0
       1.0 3.0 7.0
       1.0 3.0 7.0
       1.0 3.0 7.0"""

    res = cut_sections(text=text.splitlines(), from_string="raboof", num_lines=5)

    assert res == [
        "raboof 1.0 3.0 7.0",
        "       1.0 3.0 7.0",
        "       1.0 3.0 7.0",
        "       1.0 3.0 7.0",
        "       1.0 3.0 7.0",
    ]


def test_cut_sections_re():

    text = """
1.0
1.0
    raboof
2.0
2.0
    raboof2
3.0
3.0"""

    res = cut_sections(
        text=text.splitlines(),
        from_string="r.*f",
        from_is_re=True,
        to_string="r.*f2",
        to_is_re=True,
    )

    assert res == ["    raboof", "2.0", "2.0", "    raboof2"]


def test_cut_sections_all():

    text = """first line
1.0 2.0 3.0
1.0 2.0 3.0
1.0 2.0 3.0
last line"""

    res = cut_sections(text=text.splitlines())

    assert res == [
        "first line",
        "1.0 2.0 3.0",
        "1.0 2.0 3.0",
        "1.0 2.0 3.0",
        "last line",
    ]


def test_cut_second_occurrence():

    text = """
                                  Excitation energy
                      ------------------------------------------
  State                (Hartree)             (eV)
 ---------------------------------------------------------------
    1                  0.293221100656        7.978952559169
    2                  0.367474675899        9.999495258457
    3                  0.381243993180       10.374177466228
    4                  0.456801173849       12.430193075987

1.0 2.0 3.0
1.0 2.0 3.0
1.0 2.0 3.0
1.0 2.0 3.0

                                  Excitation energy
                      ------------------------------------------
  State                (Hartree)             (eV)
 ---------------------------------------------------------------
    1                  0.293220969371        7.978948986716
    2                  0.367474512524        9.999490812802
    3                  0.381243768931       10.374171364097
    4                  0.456801087010       12.430190712974

1.0 3.0 7.0

                                  Excitation energy
                      ------------------------------------------
  State                (Hartree)             (eV)
 ---------------------------------------------------------------
    1                  0.295653148264        8.045131945438
    2                  0.370199378778       10.073638200285
    3                  0.384062954228       10.450885303478
    4                  0.459577238880       12.505733653159
"""

    res = cut_sections(text=text.splitlines(), from_string="Excitation energy",
                       num_lines=8, certain_occurrences=[2])

    assert res == [
        "                                  Excitation energy",
        "                      ------------------------------------------",
        "  State                (Hartree)             (eV)",
        " ---------------------------------------------------------------",
        "    1                  0.293220969371        7.978948986716",
        "    2                  0.367474512524        9.999490812802",
        "    3                  0.381243768931       10.374171364097",
        "    4                  0.456801087010       12.430190712974",
    ]


def test_cut_first_and_third_occurrence():

    text = """
                                  Excitation energy
                      ------------------------------------------
  State                (Hartree)             (eV)
 ---------------------------------------------------------------
    1                  0.293221100656        7.978952559169
    2                  0.367474675899        9.999495258457
    3                  0.381243993180       10.374177466228
    4                  0.456801173849       12.430193075987

1.0 2.0 3.0
1.0 2.0 3.0
1.0 2.0 3.0
1.0 2.0 3.0

                                  Excitation energy
                      ------------------------------------------
  State                (Hartree)             (eV)
 ---------------------------------------------------------------
    1                  0.293220969371        7.978948986716
    2                  0.367474512524        9.999490812802
    3                  0.381243768931       10.374171364097
    4                  0.456801087010       12.430190712974

1.0 3.0 7.0

                                  Excitation energy
                      ------------------------------------------
  State                (Hartree)             (eV)
 ---------------------------------------------------------------
    1                  0.295653148264        8.045131945438
    2                  0.370199378778       10.073638200285
    3                  0.384062954228       10.450885303478
    4                  0.459577238880       12.505733653159
"""

    res = cut_sections(text=text.splitlines(), from_string="Excitation energy",
                       num_lines=8, certain_occurrences=[1,3])

    assert res == [
        "                                  Excitation energy",
        "                      ------------------------------------------",
        "  State                (Hartree)             (eV)",
        " ---------------------------------------------------------------",
        "    1                  0.293221100656        7.978952559169",
        "    2                  0.367474675899        9.999495258457",
        "    3                  0.381243993180       10.374177466228",
        "    4                  0.456801173849       12.430193075987",
        "                                  Excitation energy",
        "                      ------------------------------------------",
        "  State                (Hartree)             (eV)",
        " ---------------------------------------------------------------",
        "    1                  0.295653148264        8.045131945438",
        "    2                  0.370199378778       10.073638200285",
        "    3                  0.384062954228       10.450885303478",
        "    4                  0.459577238880       12.505733653159",
    ]
