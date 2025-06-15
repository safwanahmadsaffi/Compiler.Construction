def check_semantics(tokens):
    declared_vars = set()
    for i, (kind, val) in enumerate(tokens):
        if kind == 'ID':
            if i+1 < len(tokens) and tokens[i+1][0] == 'ASSIGN':
                declared_vars.add(val)
            elif val not in declared_vars:
                raise NameError(f"Use of undeclared variable: {val}")