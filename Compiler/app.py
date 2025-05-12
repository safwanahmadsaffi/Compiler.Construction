import streamlit as st
from lexer import lexer
from infix_to_postfix import infix_to_postfix
from codegen import generate_code

# Dummy semantic checker (optional to replace)
def check_semantics(tokens):
    pass  # Currently no checks

def compile_code(expr):
    try:
        tokens = lexer(expr)
        check_semantics(tokens)
        postfix = infix_to_postfix(tokens)
        instructions = generate_code(postfix.split() if isinstance(postfix, str) else postfix)
        return tokens, postfix, instructions
    except Exception as e:
        return None, None, f"Compilation Error: {e}"

# Inject CSS styles
st.markdown("""
<style>
/* Base styles */
.main { background-color: #1a1a2e; color: #ffffff; }
.stApp { background-color: #1a1a2e; }

/* Custom container */
.content-container {
    background-color: #16213e; padding: 20px; border-radius: 15px;
    margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

/* Welcome header */
.welcome-header {
    background: linear-gradient(135deg, #0f3460 0%, #533483 100%);
    color: white; padding: 30px; border-radius: 15px; margin-bottom: 30px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}
.welcome-header h1 { font-size: 2.5rem; margin-bottom: 10px; color: #ffffff; font-weight: 700; }
.welcome-header p { font-size: 1.2rem; color: #e2e8f0; margin-bottom: 0; }

/* Metric card */
.metric-card {
    background: linear-gradient(145deg, #162447 0%, #1f4068 100%);
    padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    text-align: center; height: 100%; transition: transform 0.3s ease;
}
.metric-card:hover { transform: translateY(-5px); }
.metric-card h3 { color: #e2e8f0; font-size: 1.2rem; margin-bottom: 15px; }
.stat-number { font-size: 2rem; font-weight: bold; color: #4CAF50; margin: 10px 0; }
.stat-label { color: #bdc3c7; font-size: 0.9rem; }

/* Cards */
.appointment-card, .medication-card {
    background-color: #1f4068; padding: 20px; border-radius: 12px;
    margin: 15px 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    border-left: 4px solid #4CAF50;
}
.appointment-card h4, .medication-card h4 { color: #ffffff; margin-bottom: 10px; font-size: 1.1rem; }
.appointment-card p, .medication-card p { color: #bdc3c7; margin: 0; }

/* Charts */
.chart-container {
    background-color: #162447; padding: 20px; border-radius: 15px;
    margin: 20px 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

/* Section headers */
.section-header { color: #ffffff; font-size: 1.5rem; margin: 30px 0 20px 0; padding-bottom: 10px; border-bottom: 2px solid #3498db; }

/* Status indicators */
.status-normal { color: #4CAF50; }
.status-warning { color: #f39c12; }
.status-alert { color: #e74c3c; }

/* Button styles */
.stButton > button {
    background-color: #3498db !important; color: white !important;
    border: none !important; padding: 10px 24px !important;
    border-radius: 5px !important; font-weight: 500 !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover {
    background-color: #2980b9 !important; transform: translateY(-2px) !important;
}

/* Input fields */
.stTextInput > div > div > input {
    background-color: #1f4068 !important; color: white !important;
    border: 1px solid #3498db !important;
}
.stSelectbox > div > div > select {
    background-color: #1f4068 !important; color: white !important;
    border: 1px solid #3498db !important;
}
</style>
""", unsafe_allow_html=True)

# UI Layout
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
        st.code(postfix, language='text')

        st.markdown("### 🛠️ Generated Stack Instructions")
        st.code("\n".join(result), language='text')

        st.markdown("</div>", unsafe_allow_html=True)
