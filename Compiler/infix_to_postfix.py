
import re

# Token types
NUMBER, OPERATOR, LPAREN, RPAREN = 'NUMBER', 'OPERATOR', 'LPAREN', 'RPAREN'

# Lexer: Convert input string to tokens
def lexer(expression):
    token_specification = [
        (NUMBER,   r'\d+'),
        (OPERATOR, r'[+\-*/^]'),
        (LPAREN,   r'\('),
        (RPAREN,   r'\)'),
        ('SKIP',   r'\s+'),
        ('MISMATCH', r'.')
    ]
    tokens = []
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
    for mo in re.finditer(tok_regex, expression):
        kind = mo.lastgroup
        value = mo.group()
        if kind == NUMBER:
            tokens.append(('NUMBER', value))
        elif kind == OPERATOR:
            tokens.append(('OPERATOR', value))
        elif kind == LPAREN:
            tokens.append(('LPAREN', value))
        elif kind == RPAREN:
            tokens.append(('RPAREN', value))
        elif kind == 'MISMATCH':
            raise SyntaxError(f'Unexpected character {value}')
    return tokens

# Parser/Converter: Infix to Postfix using Shunting Yard Algorithm
precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '^': 'R'}

def infix_to_postfix(tokens):
    output = []
    stack = []
    for token_type, token in tokens:
        if token_type == 'NUMBER':
            output.append(token)
        elif token_type == 'OPERATOR':
            while stack and stack[-1][0] == 'OPERATOR':
                top = stack[-1][1]
                if (associativity[token] == 'L' and precedence[token] <= precedence[top]) or                    (associativity[token] == 'R' and precedence[token] < precedence[top]):
                    output.append(stack.pop()[1])
                else:
                    break
            stack.append((token_type, token))
        elif token_type == 'LPAREN':
            stack.append((token_type, token))
        elif token_type == 'RPAREN':
            while stack and stack[-1][0] != 'LPAREN':
                output.append(stack.pop()[1])
            if not stack or stack[-1][0] != 'LPAREN':
                raise SyntaxError('Mismatched parentheses')
            stack.pop()
    while stack:
        if stack[-1][0] == 'LPAREN':
            raise SyntaxError('Mismatched parentheses')
        output.append(stack.pop()[1])
    return ' '.join(output)

# Error handler wrapper
def compile_expression(expression):
    try:
        tokens = lexer(expression)
        postfix = infix_to_postfix(tokens)
        return postfix
    except SyntaxError as e:
        return f"Syntax Error: {e}"

# Example usage
if __name__ == "__main__":
    expr = input("Enter infix expression: ")
    result = compile_expression(expr)
    print("Postfix expression:", result)
