precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
assoc = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '^': 'R'}

def infix_to_postfix(tokens):
    output, stack = [], []
    for kind, val in tokens:
        if kind in ['NUMBER', 'ID']:
            output.append(val)
        elif kind == 'OP':
            while stack and stack[-1] in precedence and (
                (assoc[val] == 'L' and precedence[val] <= precedence[stack[-1]]) or
                (assoc[val] == 'R' and precedence[val] < precedence[stack[-1]])
            ):
                output.append(stack.pop())
            stack.append(val)
        elif kind == 'LPAREN':
            stack.append(val)
        elif kind == 'RPAREN':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack:
                raise SyntaxError("Unmatched parenthesis")
            stack.pop()
        elif kind == 'ASSIGN':
            output.append('=')
    while stack:
        output.append(stack.pop())
    return output