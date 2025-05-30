import re

TOKEN_SPEC = [
    ('NUMBER',   r'\d+'),
    ('ID',       r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('OP',       r'[\+\-\*/\^]'),
    ('ASSIGN',   r'='),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('SKIP',     r'[ \t]+'),
    ('MISMATCH', r'.')
]

def lexer(code):
    tokens = []
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise SyntaxError(f'Illegal character {value!r}')
        else:
            tokens.append((kind, value))
    return tokens