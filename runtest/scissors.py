def cut_sections(f, text):
    """
    Cuts out sections of the text between anchors.

    Returns:
        output - list of remaining lines
    """
    import re

    output = []

    for i in range(len(text)):

        start_line_matches = False
        if f.from_is_re:
            start_line_matches = re.match(r'.*%s' % f.from_string, text[i])
        else:
            start_line_matches = (f.from_string in text[i])

        if start_line_matches:
            if f.num_lines > 0:
                for n in range(i, i + f.num_lines):
                    output.append(text[n])
            else:
                for j in range(i, len(text)):

                    end_line_matches = False
                    if f.to_is_re:
                        end_line_matches = re.match(r'.*%s' % f.to_string, text[j])
                    else:
                        end_line_matches = (f.to_string in text[j])

                    if end_line_matches:
                        for n in range(i, j + 1):
                            output.append(text[n])
                        break

    return output


def test_cut_sections():
    from .classes import Filter

    text = '''
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
       1.0 3.0 7.0'''

    f = Filter()
    f.add(rel_tolerance=1.0e-5, from_re='raboof', num_lines=5)

    res = cut_sections(f=f.filter_list[0], text=text.splitlines())
    assert res == ['raboof 1.0 3.0 7.0', '       1.0 3.0 7.0', '       1.0 3.0 7.0', '       1.0 3.0 7.0', '       1.0 3.0 7.0']
