

def cut_sections(text,
                 from_string=None,
                 from_is_re=False,
                 to_string=None,
                 to_is_re=False,
                 num_lines=0):
    """
    Cuts out sections of the text between anchors.

    Returns:
        output - list of remaining lines
    """
    import re

    output = []

    for i, _ in enumerate(text):

        start_line_matches = False
        if from_is_re:
            start_line_matches = re.match(r'.*%s' % from_string, text[i])
        else:
            start_line_matches = (from_string in text[i])

        if start_line_matches:
            if num_lines > 0:
                for n in range(i, i + num_lines):
                    output.append(text[n])
            else:
                for j in range(i, len(text)):

                    end_line_matches = False
                    if to_is_re:
                        end_line_matches = re.match(r'.*%s' % to_string, text[j])
                    else:
                        end_line_matches = (to_string in text[j])

                    if end_line_matches:
                        for n in range(i, j + 1):
                            output.append(text[n])
                        return output

    return output


def test_cut_sections():

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

    res = cut_sections(text=text.splitlines(),
                       from_string='raboof',
                       num_lines=5)

    assert res == ['raboof 1.0 3.0 7.0', '       1.0 3.0 7.0', '       1.0 3.0 7.0', '       1.0 3.0 7.0', '       1.0 3.0 7.0']


def test_cut_sections_re():

    text = '''
1.0
1.0
    raboof
2.0
2.0
    raboof2
3.0
3.0'''

    res = cut_sections(text=text.splitlines(),
                       from_string='r.*f',
                       from_is_re=True,
                       to_string='r.*f2',
                       to_is_re=True)

    assert res == ['    raboof', '2.0', '2.0', '    raboof2']
