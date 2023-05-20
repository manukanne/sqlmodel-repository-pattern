from re import sub

def to_camel(s: str) -> str:
    """Converts an input string to a camel string.

    Args:
        s (str): Input string.

    Returns:
        str: Camel string.
    """
    ret = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return ''.join([ret[0].lower(), ret[1:]])