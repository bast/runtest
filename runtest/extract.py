def extract_numbers(f, text):
    """
    Input:
        - f -- filter task
        - text -- list of lines where we extract numbers from

    Returns:
        - numbers -- list of numbers
        - locations -- locations of each number, list of triples
                      (line, start position, length)
    """
    import re

    numeric_const_pattern = r"""
    [-+]? # optional sign
    (?:
        (?: \d* \. \d+ ) # .1 .12 .123 etc 9.1 etc 98.1 etc
        |
        (?: \d+ \.? ) # 1. 12. 123. etc 1 12 123 etc
    )
    # followed by optional exponent part if desired
    (?: [EeDd] [+-]? \d+ ) ?
    """

    pattern_int = re.compile('^-?[0-9]+$', re.VERBOSE)
    pattern_float = re.compile(numeric_const_pattern, re.VERBOSE)
    pattern_d = re.compile(r'[dD]')

    numbers = []
    locations = []

    for n, line in enumerate(text):
        i = 0
        for w in line.split():
            # do not consider words like TzB1g
            # otherwise we would extract 1 later
            if re.match(r'^[0-9\.eEdD\+\-]*$', w):
                i += 1
                if (f.use_mask) and (i not in f.mask):
                    continue
                is_integer = False
                if len(pattern_float.findall(w)) > 0:
                    is_integer = (pattern_float.findall(w) == pattern_int.findall(w))
                # apply floating point regex
                for m in pattern_float.findall(w):
                    index = line.index(m)
                    # substitute dD by e
                    m = pattern_d.sub('e', m)
                    if is_integer:
                        numbers.append(int(m))
                    else:
                        numbers.append(float(m))
                    locations.append((n, index, len(m)))

    return numbers, locations
