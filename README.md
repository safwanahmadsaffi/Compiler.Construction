    # 🚀 Infix-TO-Postfix

    # 🚀 COMPILER-CONSTRUCTION

    **This** is a lightweight expression compiler that transforms infix mathematical expressions into postfix notation and generates simple stack-based instructions. It showcases compiler components like lexing, parsing, and code generation — all through an elegant web interface built using **Streamlit**.

    ---

    > 🔍 Great for learning compiler design, expression parsing, and stack-based evaluation.

    ---

    # README content
    # 🧮 Infix Expression Compiler (with Streamlit UI)

    This project allows you to input **infix arithmetic expressions** (e.g., `a + b * (c - d)`) and:
    - Tokenizes them
    - Converts them to postfix (Reverse Polish Notation)
    - Generates **stack machine code** instructions

    ---
    ## 📁 Project Structure


        
        ├── app.py # Main Streamlit app
        ├── lexer.py # Lexer: tokenizes input strings
        ├── infix_to_postfix.py # Parser: infix to postfix converter
        ├── codegen.py # Code generator: produces stack machine instructions
        ├── requirements.txt # Required Python packages

    ## 🚀 Features

    - ✨ **Lexical Analysis** – Tokenize arithmetic expressions
    - ✨ **Supports basic arithmetic: `+ - * / ^`
    - ✨ **Infix to Postfix Parsing** – Shunting Yard algorithm for operator precedence.
    - ✨ **Handles parentheses and variable names
    - ✨ **Code Generation** – Stack-machine-like pseudo instructions (`PUSH`, `ADD`, etc.)
    - ✨ **Outputs postfix notation
    - ✨ **Produces assembly-like instructions for stack execution


    ---

    ## ✅ Requirements

    - Python 3.8+
    - [`streamlit`](https://streamlit.io/)

    ---

    ## 📦 Installation

    Install the required packages using:
    
        pip install -r requirements.txt

    ## 🧪 How to Run the App
        Clone or download this repository
    ## 🧪 Open your terminal and run
        streamlit run app.py
    ## 🧪 Open your browser to:
        http://localhost:8501

    ---

    ## ⚙️ Usage
    Enter any arithmetic expression like:

        (a + b) * (c - 42)
    The app will return

    ## 🔁 Postfix Expression
        
        a b + c 42 - *
        
    ## 🧾 Stack Machine Instructions
        LOAD a
        LOAD b
        ADD
        LOAD c
        PUSH 42
        SUB
        MUL

    ---

    ## 🌐 Deployment Tips
    To access the app from other devices on your local network (e.g., mobile):

        streamlit run app.py --server.address 0.0.0.0 --server.port 8501
    Then access it using:

        http://<your-ip>:8501

    ---

    #  CODE
        
        st.title("Infix Expression Compiler")
        st.write("Enter an arithmetic expression (e.g., (a + b) * c):")
        
        expression = st.text_input("Expression")
        
        if expression:
        try:
        tokens = lex(expression)
        token_values = [(t[1]) for t in tokens if t[0] != 'SKIP']
        postfix = infix_to_postfix([(t[0], t[1]) for t in tokens if t[0] != 'SKIP'])
        instructions = generate_code(postfix.split())
            st.subheader("Postfix Expression")
            st.code(postfix)
            st.subheader("Stack Machine Instructions")
            st.code('\\n'.join(instructions))
        except Exception as e:
            st.error(f"Error: {e}")
        
    # USE NOW
        https://mini-x-compiler.streamlit.app/
    ---
    # Acess through:
    [https://huggingface.co/spaces/Safwanahmad619/infix-to-post-compiler/](https://huggingface.co/spaces/Safwanahmad619/infix-to-post-compiler/)

        

        
    ---
    ### 🖼️ Screenshot
    ---
    <div align="center">
    <img src="compiler.png" alt="Compiler Screenshot" width="600" style="border: 2px solid #ccc; border-radius: 10px; padding: 4px;">
    </div>

