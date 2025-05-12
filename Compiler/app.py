import streamlit as st
from lexer import lexer
from infix_to_postfix import infix_to_postfix
from codegen import generate_code

# Optional: define a dummy semantic check
def check_semantics(tokens):
    # Basic placeholder: assume semantics are always valid
    pass

def compile_code(expr):
    try:
        tokens = lexer(expr)
        check_semantics(tokens)
        postfix = infix_to_postfix(tokens)
        instructions = generate_code(postfix.split() if isinstance(postfix, str) else postfix)
        return tokens, postfix, instructions
    except Exception as e:
        return None, None, f"Compilation Error: {e}"

# Streamlit UI
st.title("Expression Compiler")

user_input = st.text_input("Enter an expression (e.g., a = 3 + 4 * 2):")

if user_input:
    tokens, postfix, result = compile_code(user_input)

    if isinstance(result, str):
        st.error(result)
    else:
        st.subheader("Lexed Tokens")
        st.write(tokens)

        st.subheader("Postfix Expression")
        st.code(postfix)

        st.subheader("Stack Machine Instructions")
        st.code("\n".join(result))
