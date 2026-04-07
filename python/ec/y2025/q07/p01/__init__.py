from typing import Iterable, TextIO

def validate_name(name: str, rules: dict[str, Iterable[str]]) -> bool:
    valids : Iterable[str] = rules.keys()
    for c in name:
        if not valids or c not in valids:
            return False
        valids = rules.get(c)
    return True

def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     solve(f)
    'Oroneth'
    """
    names = next(f).strip().split(",")
    rules = {}
    next(f)
    for line in f:
        c, valids = line.strip().split(" > ")
        valids = valids.split(",")
        rules[c] = valids
    for name in names:
        if validate_name(name, rules):
            return name
    return ""
