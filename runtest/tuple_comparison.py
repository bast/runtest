def tuple_matches(t, f):
    """
    Checks if tuple matches based on tolerance settings.

    Args:
        t: tuple
        f: filter

    Returns:
        (tuple matches, error message) - error message is None if there is no error
    """

    x, x_ref = t

    if f.ignore_sign:
        # if ignore sign take absolute values
        x = abs(x)
        x_ref = abs(x_ref)

    if isinstance(x, int) and isinstance(x_ref, int):
        if x == x_ref:
            return (True, None)
        else:
            return (False, "expected: %s" % x_ref)

    if abs(x_ref) < f.ignore_below:
        return (True, None)

    if abs(x_ref) > f.ignore_above:
        return (True, None)

    error = x - x_ref
    if f.tolerance_is_relative:
        error /= x_ref
        if abs(error) <= f.tolerance:
            return (True, None)
        else:
            if f.ignore_sign:
                return (False, "expected: %s (rel diff: %6.2e ignoring signs)" % (x_ref, abs(1.0 - abs(x) / abs(x_ref))))
            else:
                return (False, "expected: %s (rel diff: %6.2e)" % (x_ref, abs(1.0 - x / x_ref)))
    else:
        if abs(error) <= f.tolerance:
            return (True, None)
        else:
            if f.ignore_sign:
                return (False, "expected: %s (abs diff: %6.2e ignoring signs)" % (x_ref, abs(abs(x) - abs(x_ref))))
            else:
                return (False, "expected: %s (abs diff: %6.2e)" % (x_ref, abs(x - x_ref)))
