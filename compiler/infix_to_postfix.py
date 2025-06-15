import re

# --- Token Types ---
NUMBER, OPERATOR, LPAREN, RPAREN = 'NUMBER', 'OPERATOR', 'LPAREN', 'RPAREN'

# --- Lexer: Converts an expression string into a list of tokens ---
def lexer(expression):
    token_specification = [
        (NUMBER,   r'\d+'),        # Integer numbers
        (OPERATOR, r'[+\-*/^]'),   # Arithmetic operators
        (LPAREN,   r'\('),         # Left parenthesis
        (RPAREN,   r'\)'),         # Right parenthesis
        ('SKIP',   r'\s+'),        # Skip spaces
        ('MISMATCH', r'.')         # Any other character is a mismatch
    ]
    
    tokens = []
    # Combine all token patterns into a single regular expression
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

    # Match tokens one by one
    for mo in re.finditer(tok_regex, expression):
        kind = mo.lastgroup    # Type of the matched token
        value = mo.group()     # Value of the matched token
        
        if kind == NUMBER:
            tokens.append(('NUMBER', value))
        elif kind == OPERATOR:
            tokens.append(('OPERATOR', value))
        elif kind == LPAREN:
            tokens.append(('LPAREN', value))
        elif kind == RPAREN:
            tokens.append(('RPAREN', value))
        elif kind == 'SKIP':
            continue  # Ignore whitespace
        elif kind == 'MISMATCH':
            raise SyntaxError(f'Unexpected character {value}')
    
    return tokens  # List of (type, value) pairs

# --- Precedence and Associativity for Operators ---
precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}     # Higher number = higher precedence
associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '^': 'R'}  # L = left-associative, R = right-associative

# --- Convert Infix Tokens to Postfix (Shunting Yard Algorithm) ---
def infix_to_postfix(tokens):
    output = []  # Postfix expression list
    stack = []   # Operator stack

    for token_type, token in tokens:
        if token_type == 'NUMBER':
            output.append(token)  # Numbers go directly to output
        elif token_type == 'OPERATOR':
            # Handle operator precedence and associativity
            while stack and stack[-1][0] == 'OPERATOR':
                top = stack[-1][1]
                if (
                    (associativity[token] == 'L' and precedence[token] <= precedence[top]) or
                    (associativity[token] == 'R' and precedence[token] < precedence[top])
                ):
                    output.append(stack.pop()[1])  # Pop operator to output
                else:
                    break
            stack.append((token_type, token))  # Push current operator onto stack
        elif token_type == 'LPAREN':
            stack.append((token_type, token))  # Push left parenthesis
        elif token_type == 'RPAREN':
            # Pop operators until matching left parenthesis is found
            while stack and stack[-1][0] != 'LPAREN':
                output.append(stack.pop()[1])
            if not stack or stack[-1][0] != 'LPAREN':
                raise SyntaxError('Mismatched parentheses')  # No matching '('
            stack.pop()  # Discard the '('

    # Pop remaining operators from the stack
    while stack:
        if stack[-1][0] == 'LPAREN':
            raise SyntaxError('Mismatched parentheses')  # Unmatched '('
        output.append(stack.pop()[1])

    return ' '.join(output)  # Join tokens with spaces

# --- Wrapper to Compile and Handle Errors ---
def compile_expression(expression):
    try:
        tokens = lexer(expression)             # Step 1: Tokenize
        postfix = infix_to_postfix(tokens)     # Step 2: Convert to postfix
        return postfix
    except SyntaxError as e:
        return f"Syntax Error: {e}"            # Return error message

# --- Entry Point for Testing ---
if __name__ == "__main__":
    expr = input("Enter infix expression: ")   # Get input from user
    result = compile_expression(expr)          # Compile expression
    print("Postfix expression:", result)       # Print the result
