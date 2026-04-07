from collections import defaultdict
from typing import Iterable, TextIO

def validate_name(name: str, rules: dict[str, Iterable[str]]) -> bool:
    valids : Iterable[str] = rules.keys()
    for c in name:
        if not valids or c not in valids:
            return False
        valids = rules.get(c)
    return True

def generate_names(names: set[str], rules: dict[str, Iterable[str]]) -> set[str]:
    next_names = set()
    for name in names:
        for continuation in rules.get(name[-1], []):
            next_names.add(name + continuation)
    return next_names

def solve(f: TextIO) -> str:
    """
    >>> from pathlib import Path
    >>> with open(Path(__file__).parent / "example.txt") as f:
    ...     solve(f)
    '25'
    >>> with open(Path(__file__).parent / "example2.txt") as f:
    ...     solve(f)
    '1154'
    """
    names = next(f).strip().split(",")
    rules = {}
    next(f)
    for line in f:
        c, valids = line.strip().split(" > ")
        valids = valids.split(",")
        rules[c] = valids
    valid_names = [set() for _ in range(12)]
    for name in names:
        if validate_name(name, rules):
            valid_names[len(name)].add(name)
    for i in range(11):
        valid_names[i + 1] |= generate_names(valid_names[i], rules)
    
    return f"{sum(len(names) for names in valid_names[7:])}"
