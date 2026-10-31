"""
PA 3 dependency: paste in YOUR OWN completed PA 2 lexer.py here.

This is the same file from PA 2's repo -- copy your own working
tokenize() implementation over this stub before starting parser.py.
Every PA repo is independent (no shared filesystem across repos), so
each pipeline stage bundles its own copy of the prior stages.

Complete tokenize() below. See the assignment, Part B,
for the full requirements. Must use a single compiled master regex
with named groups -- not a hand-rolled character-by-character loop.
"""

import re
from dataclasses import dataclass
from typing import List


@dataclass
class Token:
    type: str
    lexeme: str
    line: int


class LexError(Exception):
    pass


_TOKEN_SPEC = [
    ("NEWLINE", r"\n"),
    ("WS",      r"[ \t]+"),
    ("COMMENT", r"#[^\n]*"),
    ("NUMBER",  r"\d+"),
    ("IDENT",   r"[A-Za-z_][A-Za-z0-9_]*"),
    ("PLUS",    r"\+"),
    ("MINUS",   r"-"),
    ("STAR",    r"\*"),
    ("SLASH",   r"/"),
    ("LPAREN",  r"\("),
    ("RPAREN",  r"\)"),
    ("ASSIGN",  r"="),
    ("SEMI",    r";"),
]
 
_MASTER_RE = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in _TOKEN_SPEC)
)
 
_KEYWORDS = {
    "let": "LET",
}
 
_SKIP = {"WS", "COMMENT"}

def tokenize(source: str) -> List[Token]:
    """
    Convert `source` into a list of Token objects, ending in an EOF
    token with an empty lexeme. Recognize NUMBER, IDENT, LET, PLUS,
    MINUS, STAR, SLASH, LPAREN, RPAREN, ASSIGN, SEMI. Discard
    whitespace and '#'-prefixed comments without emitting tokens for
    them. Track 1-indexed line numbers. Raise LexError (with the
    offending character and line) on unrecognized input.
    """
    tokens: List[Token] = []
    pos = 0
    line = 1
    length = len(source)
 
    while pos < length:
        match = _MASTER_RE.match(source, pos)
 
        if match is None:
            bad_char = source[pos]
            raise LexError(
                f"Unrecognized character {bad_char!r} on line {line}"
            )
 
        kind = match.lastgroup
        lexeme = match.group()
        pos = match.end()
 
        if kind == "NEWLINE":
            line += 1
            continue
 
        if kind in _SKIP:
            continue
 
        if kind == "IDENT" and lexeme in _KEYWORDS:
            kind = _KEYWORDS[lexeme]
 
        tokens.append(Token(kind, lexeme, line))
 
    tokens.append(Token("EOF", "", line))
    return tokens