"""
PA 4: The USILang Symbol Table -- starter.

Complete Environment and check_program below. See
PA_04_The_USILang_Symbol_Table.md, Part B, for the full requirements.
"""

from typing import Optional

from parser import Assignment, BinOp, Declaration, Number, Program, Variable


class SemanticError(Exception):
    pass


class Environment:
    def __init__(self, parent: Optional["Environment"] = None) -> None:
        self.parent = parent
        self._names: dict = {}

    def define(self, name: str, line: int) -> None:
        if name in self._names:
            raise SemanticError(
                f"Duplicate declaration of '{name}' "
                f"(line {line}; originally declared line {self._names[name]})."
            )
        self._names[name] = line

    def resolve(self, name: str, line: Optional[int] = None) -> int:
        if name in self._names:
            return self._names[name]
        if self.parent is not None:
            return self.parent.resolve(name, line)
        if line is None:
            raise SemanticError(f"Use of undeclared variable '{name}'.")
        raise SemanticError(f"Use of undeclared variable '{name}' (line {line}).")


def check_expr(expr, env: Environment) -> None:
    if isinstance(expr, Variable):
        env.resolve(expr.name, expr.line)
    elif isinstance(expr, BinOp):
        check_expr(expr.left, env)
        check_expr(expr.right, env)


def check_program(ast: Program) -> Environment:
    env = Environment()
    for stmt in ast.statements:
        if isinstance(stmt, Declaration):
            check_expr(stmt.expr, env)
            env.define(stmt.name, stmt.line)
        elif isinstance(stmt, Assignment):
            env.resolve(stmt.name, stmt.line)
            check_expr(stmt.expr, env)
    return env