from functools import reduce
from typing import Dict, List, Set, Optional, Any, Tuple, Union, NamedTuple
from src.utils.visitor import ASTVisitor
from src.utils.nodes import *
from semantic.error import *
from src.utils.type import *
import copy



RESERVED_NAMES = ['reduce', 'map', 'filter', 'int', 'str', 'float', 'bool', 'print']

class Symbol:
    """Class representing a symbol in the symbol table."""

    def __init__(self, name: str, type_: Type, used: bool = False):
        self.name = name
        self.type_ = type_
        self.used = used
    def __str__(self):
        return f"Symbol({self.name}: {self.type_})"
    def __repr__(self):
        return self.__str__()
    def mark_used(self):
        self.used = True
    def is_used(self):
        return self.used
    def update_type(self, new_type: Type):
        if is_undifined(new_type):
            return
        self.type_ = new_type
    def get_name(self):
        return self.name
    
class Storage:
    def __init__(self, symbols: List[List[Symbol]] = [[]]):
        self.symbols = symbols

    def add_symbol(self, symbol: Symbol):
        if not symbol:
            return
        self.symbols[0].append(symbol)

    def push_scope(self):
        self.symbols.insert(0, [])

    def pop_scope(self):
        if len(self.symbols) <= 1:
            raise Exception("No scope to pop")
        unused=self.get_unsed_symbols()
        for sym in unused:
            warnings.warn(f"{sym.name}", UnusedVariable)
        self.symbols.pop(0)

    def lookup(self, name: str) -> Optional[Symbol]:
        for scope in self.symbols:
            for symbol in scope:
                if symbol.name == name:
                    return symbol
        return None
    
    def lookup_current_scope(self, name: str) -> Optional[Symbol]:
        for symbol in self.symbols[0]:
            if symbol.name == name:
                return symbol
        return None
    
    def get_unsed_symbols(self) -> List[Symbol]:
        unused = []
        for symbol in self.symbols[0]:
            if not symbol.is_used():
                unused.append(symbol)
        return unused
    

    def add_symbol_RESERVED(self):
        for name in RESERVED_NAMES:
            sym=None
            match name:
                case 'reduce': sym= Symbol('reduce',   FuncType(3,UndefinedType()),True)
                case 'map': sym=    Symbol('map',      FuncType(2,ListType()),     True)
                case 'filter': sym= Symbol('filter',   FuncType(2,ListType()),     True)
                case 'int': sym=    Symbol('int',      FuncType(1,IntType()),      True)
                case 'bool': sym=   Symbol('bool',     FuncType(1,BoolType()),     True)
                case 'str': sym=    Symbol('str',      FuncType(1,StringType()),   True)
                case 'float': sym=  Symbol('float',    FuncType(1,FloatType()),    True)
                case 'print': sym=  Symbol('print',    FuncType(1,UndefinedType()),True)
            self.add_symbol(sym)


def error_wrapper(func) :
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except StaticError as e:
            node:ASTNode = args[1]  # Assuming the second argument is always the AST node
            raise BaoError(e, node.line, node.column)
    return wrapper

class StaticChecker(ASTVisitor):
    """Static checker for BaoLang AST."""
    def check(self, ast):
        """Perform static checking on the AST."""
        self.visit(ast, None)

    @error_wrapper
    def visit(self, node, o):
        return super().visit(node,o)

    def __init__(self):
        self.storage=Storage()
        self.storage.add_symbol_RESERVED()
        self.cur_let_id=None
    
    def visit_program(self, node: "Program", o: Any = None):
        """
        + Visit all statements
        + Check for unused variables
        """
        for stmt in node.statements:
            self.visit(stmt, o)
        
        for sym in self.storage.get_unsed_symbols():
            warnings.warn(f"{sym.name}", UnusedVariable)

    
    def visit_let_stmt(self, node: "LetStmt", o: Any = None):
        """
        + Check if variable name is reserved/redeclared
        + Temporarily add variable to symbol table
        + Visit the value expression
        + Update variable type in symbol table
        """

        name=node.name
        if type(node.expr) is not LambdaExpr:
            self.cur_let_id=name
        if name in RESERVED_NAMES:
            raise IdentifierIsReserved(name)
        if self.storage.lookup_current_scope(name):
            raise RedeclaredIdentifier(name)
        if self.storage.lookup(name):
            warnings.warn(f"{name}", IdentifierShadowing)

        
        temp_symbol=Symbol(name,UndefinedType(),False)
        self.storage.add_symbol(temp_symbol)

        value_type=self.visit(node.expr,UndefinedType())

        temp_symbol.update_type(value_type)
        self.cur_let_id=None

    
    def visit_expr_stmt(self, node: "ExprStmt", o: Any = None):
        """
        + Visit the expression
        """
        self.visit(node.expr, UndefinedType())

    
    def visit_if_expr(self, node: "IfExpr", o: Type = None):
        """
        + Visit condition expression and check if it's boolean
        + Visit then and else expressions
        """
        expected_type = o
        cond_type = self.visit(node.condition, BoolType())
        if not is_bool(cond_type):
            raise IfConditionNotBoolean(node.condition)
        
        then_type = self.visit(node.then_branch, expected_type)

        if node.else_branch:
            else_type = self.visit(node.else_branch, expected_type) 
            if not is_same_type(then_type, else_type):
                return UndefinedType()
        return then_type

    
    def visit_list_access_expr(self, node: "ListAccessExpr", o: Any = None):
        """
        + Determine if the primary expression is a list
        + Determine if the index expression is an integer
        """
        expected_type = o
        primary_type=self.visit(node.list_expr, ListType())
        index_type=self.visit(node.index_expr, IntType())
        if not is_int(index_type):
            raise ListAccessMustBeInteger(node.index_expr)
        if not is_list(primary_type):
            raise IdentifierNotList(node.list_expr)
        return expected_type

    
    def visit_binary_expr(self, node: "BinaryExpr", o: Any = None):
        """
        + Visit left and right expressions
        + Determine result type based on operator
        + Update left or right type if necessary
        """
        expected_type = o
        left_type=self.visit(node.left, UndefinedType())
        if is_undifined(left_type):
            right_type=self.visit(node.right, UndefinedType())
            left_type=self.visit(node.left, right_type)
        else:
            right_type=self.visit(node.right, left_type)


        match node.operator:
            case '+':
                return left_type + right_type
            case '-':
                return left_type - right_type
            case '*':
                return left_type * right_type
            case '/':
                return left_type / right_type
            case '%':
                return left_type % right_type
            case '&&':
                return left_type and right_type
            case '||':
                return left_type or right_type
            case '==':
                return left_type == right_type
            case '!=':
                return left_type != right_type
            case '<':
                return left_type < right_type
            case '<=':
                return left_type <= right_type
            case '>':
                return left_type > right_type
            case '>=':
                return left_type >= right_type

    
    def visit_func_call_expr(self, node: "FuncCallExpr", o: Any =
    None):
        """
        + Determine if the function identifier is a function
        + Check argument count
        + Check argument types
        """
        expected_type = o
        arg_types = []
        for arg in node.arguments:
            arg_types+=[self.visit(arg, UndefinedType())]

        primary_type=self.visit(node.func_name, FuncType(len(arg_types),expected_type))
        if not is_func(primary_type):
            raise IdentifierNotFunction(node.func_name)
        primary_type:FuncType
        
        if len(arg_types) < primary_type.param_len:
            raise TooFewArguments(node)
        if len(arg_types) > primary_type.param_len:
            raise TooManyArguments(node)
        
        return primary_type.return_type
        
    def visit_match_expr(self, node: "MatchExpr", o: Any = None):
        """
        + Visit the primary expression
        + Visit all case expressions and check for type consistency
        """
        expected_type = o
        primary_type=self.visit(node.expr, UndefinedType())
        case_types = [self.visit(case, (primary_type, expected_type)) for case in node.cases]
        if not all(is_same_type(case_type, case_types[0]) for case_type in case_types):
            return UndefinedType()
        return case_types[0]

    
    def visit_match_case(self, node: "MatchCase", o: Any = None):
        """
        + Check pattern type against primary expression type
        + Visit case body expression
        """
        primary_type, expected_type = o
        pattern_type = self.visit(node.pattern, primary_type) if node.pattern else primary_type
        if not is_same_type(pattern_type, primary_type):
            raise TypeMismatchInExpression(node)
        body_type=self.visit(node.body, expected_type)
        
        return body_type

    
    def visit_literal_expr(self, node: "LiteralExpr", o: Any = None):
        """
        + Return the type of the literal
        """
        if isinstance(node, IntLit):
            return IntType()
        elif isinstance(node, FloatLit):
            return FloatType()
        elif isinstance(node, BoolLit):
            return BoolType()
        elif isinstance(node, StringLit):
            return StringType()
        else:
            raise Exception("Unknown literal type")

    
    def visit_identifier_expr(self, node: "IdentifierExpr", o: Any = None):
        """
        + Lookup identifier in symbol table
        + Update usage status
        + Update type if necessary
        """
        expected_type = o
        if self.cur_let_id == node.name:
            raise CircularDependency(node.name)
        symbol=self.storage.lookup(node.name)

        if not symbol:
            raise UndeclaredIdentifier(node.name)
        
        symbol.mark_used()
        if is_undifined(symbol.type_):
            symbol.update_type(expected_type)

        return symbol.type_

    
    def visit_list_expr(self, node: "ListExpr", o: Any = None):
        """
        + Visit all element expressions
        """
        expected_type = o
        element_types = [self.visit(element, UndefinedType()) for element in node.elements]
        return ListType()

    
    def visit_unary_expr(self, node: "UnaryExpr", o: Any = None):
        """
        + Visit the operand expression
        """
        expected_type = o
        operand_type=self.visit(node.operand, expected_type)
        match node.operator:
            case '-':
                return -operand_type
            case '!':
                return not operand_type

    
    def visit_lambda_expr(self, node: "LambdaExpr", o: Any = None):
        """
        + Create new scope for lambda parameters
        + Visit parameter declarations
        + Visit lambda body expression
        """
        expected_type = o
        expected_ret_type = expected_type.return_type if is_func(expected_type) and not is_undifined(expected_type) else UndefinedType()

        self.storage.push_scope()
        for param in node.params:
            param_symbol=Symbol(param, UndefinedType())
            self.storage.add_symbol(param_symbol)

        body_type=self.visit(node.body, expected_ret_type)
        self.storage.pop_scope()
        return FuncType(len(node.params), body_type)

    
    def visit_block_expr(self, node: "BlockExpr", o: Any = None):
        """
        + Create new scope for block statements
        + Visit all statements
        + Visit return expression
        """
        expected_type = o
        self.storage.push_scope()
        for stmt in node.statements:
            self.visit(stmt, o)
        expr_type=self.visit(node.expression, expected_type)
        self.storage.pop_scope()
        return expr_type

