# SPDX-FileCopyrightText: 2023 Radovan Bast <radovan.bast@uit.no>
#
# SPDX-License-Identifier: MPL-2.0

recognized_kw = [
    "from_re",
    "to_re",
    "re",
    "from_string",
    "to_string",
    "string",
    "skip_below",
    "skip_above",
    "ignore_sign",
    "ignore_order",
    "mask",
    "num_lines",
    "rel_tolerance",
    "abs_tolerance",
]

incompatible_pairs = [
    ("from_re", "from_string"),
    ("to_re", "to_string"),
    ("to_string", "num_lines"),
    ("to_re", "num_lines"),
    ("string", "from_string"),
    ("string", "to_string"),
    ("string", "from_re"),
    ("string", "to_re"),
    ("string", "num_lines"),
    ("re", "from_string"),
    ("re", "to_string"),
    ("re", "from_re"),
    ("re", "to_re"),
    ("re", "num_lines"),
    ("rel_tolerance", "abs_tolerance"),
]
