import streamlit as st
from lexer import lexer

# --- AST Node ---
class ASTNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def to_dict(self):
        return {
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }

# --- Infix to Postfix ---
def infix_to_postfix(tokens):
    output = []
    stack = []
    precedence = {'=': 0, '+': 1, '-': 1, '*': 2, '/': 2}

    for token in tokens:
        if token.isdigit() or token.isidentifier():
            output.append(token)
        elif token in precedence:
            while stack and stack[-1] != '(' and precedence[token] <= precedence.get(stack[-1], -1):
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

# --- Build AST from Postfix ---
def build_ast(postfix_tokens):
    stack = []
    for token in postfix_tokens:
        if token.isdigit() or token.isidentifier():
            stack.append(ASTNode(token))
        else:
            right = stack.pop()
            left = stack.pop()
            stack.append(ASTNode(token, left, right))
    return stack[0]

# --- Generate Stack Instructions ---
def generate_code(postfix_tokens):
    instructions = []
    for token in postfix_tokens:
        if token.isdigit() or token.isidentifier():
            instructions.append(f"PUSH {token}")
        else:
            instructions.append(token.upper())
    return instructions

# --- Extract tokens from lexer output ---
def extract_token_values(lexer_output):
    return [token[1] for token in lexer_output]

# --- Semantic Check ---
def check_semantics(tokens):
    valid_operators = {'+', '-', '*', '/', '(', ')', '='}
    for token in tokens:
        if not (token.isdigit() or token in valid_operators or token.isidentifier()):
            raise ValueError(f"Invalid token: {token}")

# --- Main Compilation ---
def compile_code(expr):
    try:
        raw_tokens = lexer(expr)
        token_values = extract_token_values(raw_tokens)
        check_semantics(token_values)
        postfix = infix_to_postfix(token_values)
        instructions = generate_code(postfix)
        ast_root = build_ast(postfix)
        return token_values, postfix, instructions, ast_root
    except Exception as e:
        return None, None, None, f"Compilation Error: {e}"

# --- Streamlit UI ---
st.markdown("<h2>Expression Compiler</h2><p>Convert infix expressions to postfix, stack code & visualize AST</p>", unsafe_allow_html=True)

expr = st.text_input("Enter an expression (e.g., `x = 3 + 4 * 2`)")

if expr:
    tokens, postfix, result, ast = compile_code(expr)

    if isinstance(ast, str):
        st.error(ast)
    else:
        st.markdown("### 🔍 Tokens")
        st.json(tokens)

        st.markdown("### ➕ Postfix Expression")
        st.code(" ".join(postfix), language='text')

        st.markdown("### 🛠️ Generated Stack Instructions")
        st.code("\n".join(result), language='text')

        st.markdown("### 🌳 Abstract Syntax Tree (AST) - JSON")
        st.json(ast.to_dict())

        def render_dot(node):
            def visit(n):
                if n is None:
                    return ""
                label = n.value
                this_id = id(n)
                dot = f'  {this_id} [label="{label}"]\n'
                if n.left:
                    dot += visit(n.left)
                    dot += f'  {this_id} -> {id(n.left)}\n'
                if n.right:
                    dot += visit(n.right)
                    dot += f'  {this_id} -> {id(n.right)}\n'
                return dot

            return "digraph AST {\n" + visit(node) + "}"

        try:
            import graphviz
            dot_code = render_dot(ast)
            st.markdown("### 🌐 AST Tree Diagram (Graphviz)")
            st.graphviz_chart(dot_code)
        except ImportError:
            st.warning("Graphviz is not available for diagram rendering.")
