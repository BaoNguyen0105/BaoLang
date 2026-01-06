"""AST Visitor Base Class for BaoLang"""


from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .nodes import *

class ASTVisitor(ABC):
    """Abstract base class for AST visitors."""

    def visit(self, node: "ASTNode", o: Any = None):
        """Visit a node using the visitor pattern."""
        return node.accept(self, o)
    
    @abstractmethod
    def visit_program(self, node: "Program", o: Any = None):
        pass

    @abstractmethod
    def visit_let_stmt(self, node: "LetStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_expr_stmt(self, node: "ExprStmt", o: Any = None):
        pass

    @abstractmethod
    def visit_if_expr(self, node: "IfExpr", o: Any = None):
        pass

    @abstractmethod
    def visit_list_access_expr(self, node: "ListAccessExpr", o: Any = None):
        pass

    @abstractmethod
    def visit_binary_expr(self, node: "BinaryExpr", o: Any = None):
        pass

    @abstractmethod
    def visit_func_call_expr(self, node: "FuncCallExpr", o: Any =
    None):
        pass

    @abstractmethod
    def visit_match_expr(self, node: "MatchExpr", o: Any = None):
        pass

    @abstractmethod
    def visit_match_case(self, node: "MatchCase", o: Any = None):
        pass

    @abstractmethod
    def visit_literal_expr(self, node: "LiteralExpr", o: Any = None):
        pass

    @abstractmethod
    def visit_identifier_expr(self, node: "IdentifierExpr", o: Any = None):
        pass

    @abstractmethod
    def visit_list_expr(self, node: "ListExpr", o: Any = None):
        pass

    @abstractmethod
    def visit_unary_expr(self, node: "UnaryExpr", o: Any = None):
        pass

    @abstractmethod
    def visit_lambda_expr(self, node: "LambdaExpr", o: Any = None):
        pass

    @abstractmethod
    def visit_block_expr(self, node: "BlockExpr", o: Any = None):
        pass

    

