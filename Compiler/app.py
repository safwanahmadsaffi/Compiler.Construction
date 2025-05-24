import streamlit as st
from lexer import lexer
from infix_to_postfix import infix_to_postfix
from codegen import generate_code

# Extract only the string tokens from lexer output
def extract_token_values(lexer_output):
    return [token[1] for token in lexer_output]

# Semantic checker with basic token validation
def check_semantics(tokens):
    valid_operators = {'+', '-', '*', '/', '(', ')', '='}
    for token in tokens:
        if not (token.isdigit() or token in valid_operators or token.isidentifier()):
            raise ValueError(f"Invalid token: {token}")

# Updated infix_to_postfix using Shunting Yard algorithm
def infix_to_postfix(tokens):
    output = []
    stack = []
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    for token in tokens:
        if token.isdigit() or token.isidentifier():
            output.append(token)
        elif token in precedence:
            while stack and stack[-1] != '(' and precedence[token] <= precedence.get(stack[-1], 0):
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()

    while stack:
        output.append(stack.pop())

    return output

# Updated code generator
def generate_code(postfix_tokens):
    instructions = []
    for token in postfix_tokens:
        if token.isdigit() or token.isidentifier():
            instructions.append(f"PUSH {token}")
        else:
            instructions.append(token.upper())
    return instructions

# Main compiler logic
def compile_code(expr):
    try:
        raw_tokens = lexer(expr)
        token_values = extract_token_values(raw_tokens)
        check_semantics(token_values)
        postfix = infix_to_postfix(token_values)
        instructions = generate_code(postfix)
        return token_values, postfix, instructions
    except Exception as e:
        return None, None, f"Compilation Error: {e}"

st.markdown("<div class='welcome-header'><h2>Expression Compiler</h2><p>Convert infix expressions to postfix & stack code</p></div>", unsafe_allow_html=True)

expr = st.text_input("Enter an expression (e.g., `x = 3 + 4 * 2`)")

if expr:
    tokens, postfix, result = compile_code(expr)

    if isinstance(result, str):
        st.error(result)
    else:
        st.markdown("<div class='content-container'>", unsafe_allow_html=True)

        st.markdown("### 🔍 Tokens")
        st.json(tokens)

        st.markdown("### ➕ Postfix Expression")
        st.code(" ".join(postfix), language='text')

        st.markdown("### 🛠️ Generated Stack Instructions")
        st.code("\n".join(result), language='text')

        st.markdown("</div>", unsafe_allow_html=True)
