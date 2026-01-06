"""AST Node Definitions for BaoLang"""


from abc import ABC, abstractmethod
from typing import Any, List, Optional, Union, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .visitor import ASTVisitor

class ASTNode(ABC):
    """Base class for all AST nodes."""

    def __init__(self, line: int = None, column: int = None):
        self.line = line
        self.column = column

    @abstractmethod
    def accept(self, visitor: "ASTVisitor", o: Any = None):
        """Accept a visitor for the Visitor pattern."""
        pass

    def __str__(self):
        """Default string representation."""
        return f"{self.__class__.__name__}()"

# Program
class Program(ASTNode):
    """Root node representing the entire OPLang program."""

    def __init__(self, statements: Optional[List["Stmt"]] = None, line: int = None, column: int = None):
        super().__init__(line, column)
        self.statements: List[Stmt] = statements if statements is not None else []

    def accept(self, visitor, o=None):
        return visitor.visit_program(self, o)

    def __str__(self):
        statements_str = "\n".join([str(stmt) for stmt in self.statements])
        return f"Program(\n{"\n".join([str(stmt) for stmt in self.statements])})"

#Statements
class Stmt(ASTNode):
    pass

class LetStmt(Stmt):
    def __init__(self, name: str, expr: "Expr", line: int = None, column: int = None):
        super().__init__(line, column)
        self.name = name
        self.expr = expr

    def accept(self, visitor, o=None):
        return visitor.visit_let_stmt(self, o)

    def __str__(self):
        return f"LetStmt({self.name} = {self.expr})"
    
class ExprStmt(Stmt):
    def __init__(self, expr: "Expr", line: int = None, column: int = None):
        super().__init__(line, column)
        self.expr = expr

    def accept(self, visitor, o=None):
        return visitor.visit_expr_stmt(self, o)

    def __str__(self):
        return f"ExprStmt({self.expr})"
    
# Expressions
class Expr(ASTNode):
    pass   

class IfExpr(Expr):
    def __init__(self, condition: Expr, then_branch: Expr, else_branch: Optional[Expr] = None, line: int = None, column: int = None):
        super().__init__(line, column)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor, o=None):
        return visitor.visit_if_expr(self, o)

    def __str__(self):
        return f"IfExpr({self.condition},\n then {self.then_branch},\n else {self.else_branch})"
    
class ListAccessExpr(Expr):
    def __init__(self, list_expr: Expr, index_expr: Expr, line: int = None, column: int = None):
        super().__init__(line, column)
        self.list_expr = list_expr
        self.index_expr = index_expr

    def accept(self, visitor, o=None):
        return visitor.visit_list_access_expr(self, o)

    def __str__(self):
        return f"ListAccessExpr({self.list_expr}[{self.index_expr}])"
    
class BinaryExpr(Expr):
    def __init__(self, left: Expr, operator: str, right: Expr, line: int = None, column: int = None):
        super().__init__(line, column)
        self.left = left
        self.operator = operator
        self.right = right
    def accept(self, visitor, o=None):
        return visitor.visit_binary_expr(self, o)
    def __str__(self):
        return f"BinaryExpr({self.left} {self.operator} {self.right})"
    
class FuncCallExpr(Expr):  
    def __init__(self, func_name: Expr, arguments: List[Expr], line: int = None, column: int = None):
        super().__init__(line, column)
        self.func_name = func_name
        self.arguments = arguments

    def accept(self, visitor, o=None):
        return visitor.visit_func_call_expr(self, o)

    def __str__(self):
        return f"FuncCallExpr({self.func_name}, args={", ".join([arg.__str__() for arg in self.arguments])})"
    
class MatchExpr(Expr):
    def __init__(self, expr: Expr, cases: List["MatchCase"], line: int = None, column: int = None):
        super().__init__(line, column)
        self.expr = expr
        self.cases = cases

    def accept(self, visitor, o=None):
        return visitor.visit_match_expr(self, o)

    def __str__(self):
        return f"MatchExpr({self.expr},\n {"".join([match_case.__str__() for match_case in self.cases])})"
    
class LiteralExpr(Expr):
    def __init__(self, value: Any, line: int = None, column: int = None):
        super().__init__(line, column)
        self.value = value

    def accept(self, visitor, o=None):
        return visitor.visit_literal_expr(self, o)

    def __str__(self):
        return f"LiteralExpr({self.value})"
    
class IntLit(LiteralExpr):
    def __init__(self, value: int, line: int = None, column: int = None):
        super().__init__(value, line, column)

    def accept(self, visitor, o=None):
        return super().accept(visitor, o)

    def __str__(self):
        return f"IntLit({self.value})"
    
class FloatLit(LiteralExpr):
    def __init__(self, value: float, line: int = None, column: int = None):
        super().__init__(value, line, column)

    def accept(self, visitor, o=None):
        return super().accept(visitor, o)

    def __str__(self):
        return f"FloatLit({self.value})"
    
class StringLit(LiteralExpr):
    def __init__(self, value: str, line: int = None, column: int = None):
        super().__init__(value, line, column)

    def accept(self, visitor, o=None):
        return super().accept(visitor, o)

    def __str__(self):
        return f"StringLit({self.value})"
    
class BoolLit(LiteralExpr):
    def __init__(self, value: bool, line: int = None, column: int = None):
        super().__init__(value, line, column)

    def accept(self, visitor, o=None):
        return super().accept(visitor, o)

    def __str__(self):
        return f"BoolLit({self.value})"
    
class IdentifierExpr(Expr):
    def __init__(self, name: str, line: int = None, column: int = None):
        super().__init__(line, column)
        self.name = name

    def accept(self, visitor, o=None):
        return visitor.visit_identifier_expr(self, o)

    def __str__(self):
        return f"IdentifierExpr({self.name})"
    
class ListExpr(Expr):
    def __init__(self, elements: List[Expr], line: int = None, column: int = None):
        super().__init__(line, column)
        self.elements = elements

    def accept(self, visitor, o=None):
        return visitor.visit_list_expr(self, o)

    def __str__(self):
        return f"ListExpr([{"".join([elem.__str__() for elem in self.elements])}])"
    
class UnaryExpr(Expr):  
    def __init__(self, operator: str, operand: Expr, line: int = None, column: int = None):
        super().__init__(line, column)
        self.operator = operator
        self.operand = operand

    def accept(self, visitor, o=None):
        return visitor.visit_unary_expr(self, o)

    def __str__(self):
        return f"UnaryExpr({self.operator}{self.operand})"
    
class MatchCase(ASTNode):
    def __init__(self, pattern: Optional[Expr], body: Expr, line: int = None, column: int = None):
        super().__init__(line, column)
        self.pattern = pattern
        self.body = body

    def accept(self, visitor, o=None):
        return visitor.visit_match_case(self, o)

    def __str__(self):
        return f"MatchCase({self.pattern.__str__() if self.pattern else 'default'}: {self.body})"

class LambdaExpr(Expr):
    def __init__(self, params: List[str], body: Expr, line: int = None, column: int = None):
        super().__init__(line, column)
        self.params = params
        self.body = body

    def accept(self, visitor, o=None):
        return visitor.visit_lambda_expr(self, o)

    def __str__(self):
        return f"LambdaExpr({", ".join(self.params)}: {self.body})"

class BlockExpr(Expr):
    def __init__(self, statements: Optional[List[Stmt]], expression:Expr, line: int = None, column: int = None):
        super().__init__(line, column)
        self.statements = statements
        self.expression = expression

    def accept(self, visitor, o=None):
        return visitor.visit_block_expr(self, o)

    def __str__(self):
        return f"BlockExpr(\n{"".join([stmt.__str__() for stmt in self.statements])},\n{self.expression})"
    