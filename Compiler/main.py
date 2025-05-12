from lexer import lexer
from parser import infix_to_postfix
from semantic import check_semantics
from codegen import generate_code

def compile_code(expr):
    try:
        tokens = lexer(expr)
        check_semantics(tokens)
        postfix = infix_to_postfix(tokens)
        instructions = generate_code(postfix)
        print("\nPostfix:", ' '.join(postfix))
        print("\nStack implementation :")
        for instr in instructions:
            print(" ", instr)
    except Exception as e:
        print(f"Compilation Error: {e}")
1+2
if __name__ == "__main__":
    expr = input("Enter expression: ")
    compile_code(expr)