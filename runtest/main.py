from .exceptions import FilterKeywordError, TestFailedError, BadFilterError


def _extract_numbers(f, text):
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

# ------------------------------------------------------------------------------


def _copy_path(root_src_dir, root_dst_dir, exclude_files=[]):
    from shutil import copy
    import os
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for f in files:
            if f not in exclude_files:
                src_file = os.path.join(src_dir, f)
                dst_file = os.path.join(dst_dir, f)
                copy(src_file, dst_file)

# ------------------------------------------------------------------------------


def _filter_file(f, file_name, output):
    """
    Input:
        - f -- filter task
        - file_name -- the output file to filter

    Returns:
        - output_filtered -- the filtered output

    Raises:
        - BadFilterError
    """
    import re

    output_filtered = []

    for i in range(len(output)):
        start_line_matches = False
        if f.from_is_re:
            start_line_matches = re.match(r'.*%s' % f.from_string, output[i])
        else:
            start_line_matches = (f.from_string in output[i])
        if start_line_matches:
            if f.num_lines > 0:
                for n in range(i, i + f.num_lines):
                    output_filtered.append(output[n])
            else:
                for j in range(i, len(output)):
                    f.end_line_matches = False
                    if f.to_is_re:
                        f.end_line_matches = re.match(r'.*%s' % f.to_string, output[j])
                    else:
                        f.end_line_matches = (f.to_string in output[j])
                    if f.end_line_matches:
                        for n in range(i, j + 1):
                            output_filtered.append(output[n])
                        break

    if output_filtered == []:
        if f.num_lines > 0:
            r = '[%i lines from "%s"]' % (f.num_lines, f.from_string)
        else:
            r = '["%s" ... "%s"]' % (f.from_string, f.to_string)
        message = 'ERROR: filter %s did not extract anything from file %s\n' % (r, file_name)
        raise BadFilterError(message)

    return output_filtered

# ------------------------------------------------------------------------------


def _check(filter_list, out_name, ref_name, verbose=False):
    """
    Compares output (work_dir/out_name) with reference (work_dir/ref_name)
    applying all filters tasks from the list of filters.

    Input:
        - work_dir -- working directory
        - out_name -- actual output file name
        - ref_name -- reference output file name
        - verbose  -- give verbose output upon failure

    Returns:
        - nothing

    Generates the following files in work_dir:
        - out_name.filtered  -- numbers extracted from output
        - out_name.reference -- numbers extracted from reference
        - out_name.diff      -- difference between the two above

    Raises:
        - TestFailedError
    """
    import os
    from .tuple_comparison import tuple_matches
    def _tuple_matches(t):
        if f.tolerance_is_relative:
            error_definition = 'relative'
        else:
            error_definition = 'absolute'
        return tuple_matches(t,
                             tolerance=f.tolerance,
                             error_definition=error_definition,
                             ignore_sign=f.ignore_sign,
                             skip_below=f.ignore_below,
                             skip_above=f.ignore_above)

    log_out = open('%s.filtered' % out_name, 'w')
    log_ref = open('%s.reference' % out_name, 'w')
    log_diff = open('%s.diff' % out_name, 'w')

    for f in filter_list:

        out_filtered = _filter_file(f, out_name, open(out_name).readlines())
        log_out.write(''.join(out_filtered))
        out_numbers, out_locations = _extract_numbers(f, out_filtered)
        if f.use_mask and out_numbers == []:
            raise FilterKeywordError('ERROR: mask %s did not extract any numbers\n' % f.mask)

        ref_filtered = _filter_file(f, ref_name, open(ref_name).readlines())
        log_ref.write(''.join(ref_filtered))
        ref_numbers, ref_locations = _extract_numbers(f, ref_filtered)
        if f.use_mask and ref_numbers == []:
            raise FilterKeywordError('ERROR: mask %s did not extract any numbers\n' % f.mask)

        if out_numbers == [] and ref_numbers == []:
            # no numbers are extracted
            if out_filtered != ref_filtered:
                log_diff.write('ERROR: extracted strings do not match\n')
                log_diff.write('own gave:\n')
                log_diff.write(''.join(out_filtered) + '\n')
                log_diff.write('reference gave:\n')
                log_diff.write(''.join(ref_filtered) + '\n')

        # we need to check for len(out_numbers) > 0
        # for pure strings len(out_numbers) is 0
        # TODO need to consider what to do with pure strings in future versions
        if len(out_numbers) == len(ref_numbers) and len(out_numbers) > 0:
            if not f.tolerance_is_set and (any(map(lambda x: isinstance(x, float), out_numbers)) or any(map(lambda x: isinstance(x, float), ref_numbers))):
                raise FilterKeywordError('ERROR: for floats you have to specify either rel_tolerance or abs_tolerance\n')
            l = map(_tuple_matches, zip(out_numbers, ref_numbers))
            matching, errors = zip(*l)  # unzip tuples to two lists
            if not all(matching):
                log_diff.write('\n')
                for k, line in enumerate(out_filtered):
                    log_diff.write('.       %s' % line)
                    for i, num in enumerate(out_numbers):
                        (line_num, start_char, length) = out_locations[i]
                        if line_num == k:
                            if errors[i]:
                                log_diff.write('ERROR   %s%s %s\n' % (' ' * start_char, '#' * length, errors[i]))

        if len(out_numbers) != len(ref_numbers):
            log_diff.write('ERROR: extracted sizes do not match\n')
            log_diff.write('own gave %i numbers:\n' % len(out_numbers))
            log_diff.write(''.join(out_filtered) + '\n')
            log_diff.write('reference gave %i numbers:\n' % len(ref_numbers))
            log_diff.write(''.join(ref_filtered) + '\n')

    log_out.close()
    log_ref.close()
    log_diff.close()

    if os.path.getsize('%s.diff' % out_name) > 0:
        log_diff = open('%s.diff' % out_name, 'r')
        diff = ''
        for line in log_diff.readlines():
            diff += line
        log_diff.close()
        message = "ERROR: test %s failed\n" % out_name
        if verbose:
            message += diff
        raise TestFailedError(message)
