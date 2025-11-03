import ast
import operator as op

# math.py - simple safe command-line calculator


# supported operators
_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.FloorDiv: op.floordiv,
}
_UNARY = {
    ast.UAdd: lambda x: +x,
    ast.USub: lambda x: -x,
}


def _eval(node):
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        oper = _OPERATORS.get(type(node.op))
        if oper is None:
            raise ValueError("unsupported operator")
        return oper(left, right)
    if isinstance(node, ast.UnaryOp):
        func = _UNARY.get(type(node.op))
        if func is None:
            raise ValueError("unsupported unary operator")
        return func(_eval(node.operand))
    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("only numbers allowed")
    if isinstance(node, ast.Num):  # older Python
        return node.n
    raise ValueError("unsupported expression")


def evaluate(expr: str):
    tree = ast.parse(expr, mode="eval")
    return _eval(tree.body)


def repl():
    print("Calculator (type 'exit' or 'quit' to leave)")
    while True:
        try:
            s = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not s:
            continue
        if s.lower() in ("exit", "quit", "q"):
            break
        try:
            result = evaluate(s)
            print(result)
        except ZeroDivisionError:
            print("Error: division by zero")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    repl()
    