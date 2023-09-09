import string

def strings(filename, min=4):
    strings = []
    with open(filename, errors="ignore") as f:  # Python 3.x
    # with open(filename, "rb") as f:           # Python 2.x
        result = ""
        for c in f.read():
            if c in string.printable:
                result += c
                continue
            if len(result) >= min:
                strings.append(result)
            result = ""
        if len(result) >= min:  # catch result at EOF
            strings.append(result)
    return strings
