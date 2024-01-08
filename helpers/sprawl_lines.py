import re

def sprawl_lines(lines, index, regex_pattern, inclusive=False):
    # Validate index
    if index < 0 or index >= len(lines):
        raise ValueError("Index out of range")

    # Compile regex for efficiency
    pattern = re.compile(regex_pattern)

    # Check if the starting index is a boundary
    is_start_boundary = pattern.match(lines[index])

    start = 0
    if is_start_boundary:
        if inclusive:
            start = index
        else:
            start = index + 1
    else:
        for i in range(index, -1, -1):
            if pattern.match(lines[i]):
                start = i if inclusive else i + 1
                break

    end = len(lines)
    for i in range(index + 1, end):
        if pattern.match(lines[i]):
            end = i + 1 if inclusive else i
            break

    # print(start, end)
    return lines[start:end]
