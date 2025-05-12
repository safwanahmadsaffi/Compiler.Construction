def generate_code(postfix):
    instructions = []
    for token in postfix:
        if token.isdigit():
            instructions.append(f'PUSH {token}')
        elif token.isidentifier():
            instructions.append(f'LOAD {token}')
        elif token in '+-*/^':
            instructions.append({
                '+': 'ADD', '-': 'SUB', '*': 'MUL',
                '/': 'DIV', '^': 'POW'
            }[token])
        elif token == '=':
            instructions.append('STORE')
    return instructions