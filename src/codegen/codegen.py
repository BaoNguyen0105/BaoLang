from functools import reduce
from typing import Dict, List, Set, Optional, Any, Tuple, Union, NamedTuple
from src.utils.visitor import ASTVisitor
from src.utils.nodes import *
from src.utils.type import *
from .BaoEmitter import *
from .frame import Frame
import copy
import traceback

class Symbol:
    def __init__(self, name: str, index: int = None):
        self.name = name
        self.index = index
    def __str__(self):
        return f'Symbol({self.name})'
    def __repr__(self):
        return self.__str__()
class Access:
    def __init__(self, frame: Frame, sym: List[Symbol], lambda_name: Optional[str]=None):
        self.frame = frame
        self.sym = sym
        self.lambda_name =lambda_name

class CodeGen(ASTVisitor):
    number_of_lambdas = 0
    def __init__(self, emitter: BaoEmitter = BaoEmitter('Main.j')):
        self.emit = emitter
        
        self.let_id = None
    def generate(self, ast: Program) -> str:
        self.visit(ast, None)

    def visit_program(self, node: "Program", o: Any = None):
        access=Access(Frame("main","V"), [])
        self.emit.print_out(self.emit.emit_class("Main","java/lang/Object"))
        self.emit.print_out(self.emit.emit_method_main(frame=access.frame))
        args_index=access.frame.get_new_index()
        self.emit.print_out(self.emit.emit_var(args_index, "args", access.frame))
        for stmt in node.statements:
            self.visit(stmt, access)
        self.emit.print_out(self.emit.jvm.emitRETURN())
        self.emit.print_out(self.emit.emit_end_method(access.frame))
        self.emit.emit_end_class()


    def visit_let_stmt(self, node: "LetStmt", o: Access = None):
        self.let_id = node.name
        idx=o.frame.get_new_index()
        o.sym.append(Symbol(node.name, idx))
        self.emit.print_out(self.emit.emit_var(idx, node.name, o.frame))

        self.visit(node.expr, o)
        self.emit.print_out(self.emit.emit_write_var(idx, o.frame))
        self.let_id = None

    def visit_expr_stmt(self, node: "ExprStmt", o: Access = None):
        self.visit(node.expr, o)

    def visit_if_expr(self, node: "IfExpr", o: Access = None):
        else_label=o.frame.get_new_label()
        end_if_label=o.frame.get_new_label()

        self.visit(node.condition, o)
        self.emit.print_out(self.emit.emit_if_false(else_label, o.frame))
        self.visit(node.then_branch, o)
        self.emit.print_out(self.emit.emit_goto(end_if_label))
        self.emit.print_out(self.emit.emit_label(else_label))
        if node.else_branch:
            self.visit(node.else_branch, o)
        self.emit.print_out(self.emit.emit_label(end_if_label))
        self.emit.print_out(self.emit.emit_nop(o.frame))


    def visit_list_access_expr(self, node: "ListAccessExpr", o: Access = None):
        self.visit(node.list_expr, o)
        self.visit(node.index_expr, o)
        self.emit.print_out(self.emit.emit_list_access(o.frame))

    def visit_binary_expr(self, node: "BinaryExpr", o: Access = None):
        self.visit(node.left, o)
        self.visit(node.right, o)
        if node.operator in ['+', '-', '*', '/','%','==','!=','<','<=','>','>=','&&','||']:
            self.emit.print_out(self.emit.emit_binary_op(node.operator, o.frame))
        

    def visit_func_call_expr(self, node: "FuncCallExpr", o: Access =
    None):
        self.visit(node.func_name, o)
        if isinstance(node.func_name,IdentifierExpr) and node.func_name.name in ['int', 'str', 'float', 'bool', 'print', 'filter', 'map', 'reduce']:
            for arg in node.arguments:
                self.visit(arg, o)
            
            self.emit.print_out(self.emit.emit_invoke_baolang_function(
                node.func_name.name, len(node.arguments), o.frame)
            )
        else:
            self.emit.print_out(self.emit.emit_new_list(o.frame))
            for arg in node.arguments:
                self.emit.print_out(self.emit.emit_dup(o.frame))
                self.visit(arg, o)
                self.emit.print_out(self.emit.emit_list_add(o.frame))
            self.emit.print_out(self.emit.emit_function_call(
                "", o.frame)
            )


    def visit_match_expr(self, node: "MatchExpr", o: Access = None):
        self.visit(node.expr, o)
        end_match_label=o.frame.get_new_label()
        for case in node.cases:
            self.visit(case, (o, end_match_label))
        self.emit.print_out(self.emit.emit_label(end_match_label))


    def visit_match_case(self, node: "MatchCase", o: Tuple[Access,int] = None):
        access, end_match_label = o
        end_case_label = access.frame.get_new_label()

        if node.pattern:
            self.emit.print_out(self.emit.emit_dup(access.frame))
            self.visit(node.pattern, access)
            self.emit.print_out(self.emit.emit_binary_op('==', access.frame))
            self.emit.print_out(self.emit.emit_if_false(end_case_label, access.frame))
            self.emit.print_out(self.emit.emit_pop(access.frame))
            self.visit(node.body, access)
            self.emit.print_out(self.emit.emit_goto(end_match_label))
            self.emit.print_out(self.emit.emit_label(end_case_label))
        else:
            self.emit.print_out(self.emit.emit_pop(access.frame))
            self.visit(node.body, access)
            self.emit.print_out(self.emit.emit_goto(end_match_label))
            

    def visit_literal_expr(self, node: "LiteralExpr", o: Access = None):
        if type(node.value)==int:
            self.emit.print_out(self.emit.emit_push_iconst(node.value, o.frame))
        elif type(node.value)== float:
            self.emit.print_out(self.emit.emit_push_fconst(str(node.value), o.frame))
        elif type(node.value)== str:
            self.emit.print_out(self.emit.emit_push_sconst(node.value, o.frame))
        elif type(node.value)== bool:
            self.emit.print_out(self.emit.emit_push_bconst(node.value, o.frame))
        else:
            raise IllegalOperandException(f"Illegal literal: {node.value}")

    def visit_identifier_expr(self, node: "IdentifierExpr", o: Access = None):
        if self.let_id == node.name:
            self.emit.print_out(self.emit.emit_read_var(0, o.frame))
            return

        if node.name in ['int', 'str', 'float', 'bool', 'print', 'filter', 'map', 'reduce']:
            return

        for sym in o.sym[::-1]:
            if sym.name == node.name:
                idx = sym.index
                self.emit.print_out(self.emit.emit_read_var(idx, o.frame))
                return
        # identifier not in symbol table -> this must be a lambda class field
        # generate code to read from field
        this_idx = 0
        self.emit.print_out(self.emit.emit_read_var(this_idx, o.frame))
        self.emit.print_out(self.emit.emit_get_field(f'{o.lambda_name}/{node.name}', o.frame))

    def visit_list_expr(self, node: "ListExpr", o: Access = None):
        self.emit.print_out(self.emit.emit_new_list(o.frame))
        for element in node.elements:
            self.emit.print_out(self.emit.emit_dup(o.frame))
            self.visit(element, o)
            self.emit.print_out(self.emit.emit_list_add(o.frame))


    def visit_unary_expr(self, node: "UnaryExpr", o: Access = None):
        self.visit(node.operand, o)
        if node.operator in ['-', '!']:
            self.emit.print_out(self.emit.emit_unary_op(node.operator, o.frame))


    def visit_lambda_expr(self, node: "LambdaExpr", o: Access = None):
        
        lambda_name=f'Lambda{CodeGen.number_of_lambdas}'
        prev_name=o.lambda_name
        o.lambda_name=lambda_name
        CodeGen.number_of_lambdas += 1
        temp=GetUsedIdentifier()
        temp.visit(node.body, None)

        for var in node.params:
            if var in temp.used_symbols:
                temp.used_symbols.remove(var)
        captured_vars=temp.used_symbols
        is_recursive = self.let_id in captured_vars
        if is_recursive:
            captured_vars.remove(self.let_id) 
        params=node.params
        self.generate_lambda_class(node, captured_vars, params,is_recursive, o)
        
        self.emit.print_out(self.emit.emit_new_lambda(lambda_name, o.frame))
        
        self.emit.print_out(self.emit.emit_dup(o.frame))
        
        for var in captured_vars:
            # Load captured variable
            for sym in o.sym[::-1]:
                if sym.name == var:
                    idx = sym.index
                    self.emit.print_out(self.emit.emit_read_var(idx, o.frame))
                    break
            else:
                # captured variable is from lambda field
                this_idx = 0
                self.emit.print_out(self.emit.emit_read_var(this_idx, o.frame))
                self.emit.print_out(self.emit.emit_get_field(f'{prev_name}/{var}', o.frame))
            # Pass to constructor
        
        arg_size=len(captured_vars)
        
        self.emit.print_out(self.emit.emit_invoke_constructor(lambda_name,["Ljava/lang/Object;"]*arg_size, o.frame))
        

    def generate_lambda_class(self,node: "LambdaExpr", captured_vars:List[str], params:List[str], is_recursive:bool, o: Access):
        """
        Generate a class for the lambda expression.
        1. Create a new Emitter for the lambda class.
        2. Generate the class header.
        3. Generate fields for captured variables.
        4. Implement constructor.
        5. Implement the call method.
        6. Deconstuct the parameter array list into individual parameters.
        7. Generate the body of the lambda.
        """

        # 1 Create a new Emitter for the lambda class.
        lambda_name=o.lambda_name
        lambda_emitter = BaoEmitter(f'{lambda_name}.j')

        # 2 Generate the class header.
        lambda_emitter.print_out(self.emit.emit_class(lambda_name,"java/lang/Object", "baolang/LambdaInterface"))

        # 3 Generate fields for captured variables.
        for var in captured_vars:
            lambda_emitter.print_out(lambda_emitter.emit_field(var))
        if is_recursive:
            lambda_emitter.print_out(lambda_emitter.emit_field(self.let_id))

        # 4 Implement constructor.
        constructor_frame = Frame("<init>", "V")
        constructor_sym =[]
        constructor_access = Access(constructor_frame, constructor_sym, lambda_name)
        arg_size=len(captured_vars)-1 if is_recursive else len(captured_vars)
        lambda_emitter.print_out(lambda_emitter.emit_method_init(["Ljava/lang/Object;"]*arg_size,constructor_frame))
        this_idx = constructor_frame.get_new_index()
        lambda_emitter.print_out(lambda_emitter.emit_var(this_idx, "this", constructor_frame))
        constructor_sym.append(Symbol("this", this_idx))
        lambda_emitter.print_out(lambda_emitter.emit_read_var(this_idx, constructor_frame))
        lambda_emitter.print_out(lambda_emitter.emit_invoke_constructor("java/lang/Object",[],constructor_frame))
        for i,var in enumerate(captured_vars):
            var_idx = constructor_frame.get_new_index()
            lambda_emitter.print_out(lambda_emitter.emit_var(var_idx, var, constructor_frame))
            constructor_sym.append(Symbol(var, var_idx))
            # Set field
            lambda_emitter.print_out(lambda_emitter.emit_read_var(this_idx, constructor_frame))
            lambda_emitter.print_out(lambda_emitter.emit_read_var(var_idx, constructor_frame))
            lambda_emitter.print_out(lambda_emitter.emit_put_field(f"{lambda_name}/{var}", constructor_frame))

        if is_recursive:
            # Set the field for recursive lambda
            lambda_emitter.print_out(lambda_emitter.emit_read_var(this_idx, constructor_frame))
            lambda_emitter.print_out(lambda_emitter.emit_read_var(this_idx, constructor_frame))
            lambda_emitter.print_out(lambda_emitter.emit_put_field(f"{lambda_name}/{self.let_id}", constructor_frame))
        lambda_emitter.print_out(lambda_emitter.jvm.emitRETURN())
        lambda_emitter.print_out(lambda_emitter.emit_end_method(constructor_frame))

        # 5 Implement the call method.
        lambda_frame = Frame("call", lambda_emitter.getObjectType())
        lambda_sym =[]
        lambda_access = Access(lambda_frame, lambda_sym, lambda_name)
        lambda_emitter.print_out(lambda_emitter.emit_method_call(lambda_frame))
        this_idx = lambda_frame.get_new_index()
        arraylist_idx = lambda_frame.get_new_index()
        lambda_emitter.print_out(lambda_emitter.emit_var(this_idx, "this", lambda_frame))
        lambda_emitter.print_out(lambda_emitter.emit_var(arraylist_idx, "args", lambda_frame))

        # 6 Deconstuct the parameter array list into individual parameters.
        for i,param in enumerate(params):
            # Deconstruct the parameter array list into individual parameters.
            lambda_emitter.print_out(lambda_emitter.emit_read_var(arraylist_idx, lambda_frame))
            lambda_emitter.print_out(lambda_emitter.emit_push_iconst(i, lambda_frame))
            lambda_emitter.print_out(lambda_emitter.emit_list_access(lambda_frame))
            param_idx = lambda_frame.get_new_index()
            lambda_emitter.print_out(lambda_emitter.emit_var(param_idx, param, lambda_frame))
            lambda_sym.append(Symbol(param, param_idx))
            lambda_emitter.print_out(lambda_emitter.emit_write_var(param_idx, lambda_frame))

        # 7 Generate the body of the lambda.
        
        env=CodeGen(lambda_emitter)
        env.visit(node.body, lambda_access)
        lambda_emitter.print_out(lambda_emitter.emit_return(lambda_frame))

        lambda_emitter.print_out(lambda_emitter.emit_end_method(lambda_frame))
        lambda_emitter.emit_end_class()
        

    def visit_block_expr(self, node: "BlockExpr", o: Access = None):
        scope = Access(o.frame, list(o.sym), o.lambda_name)
        for stmt in node.statements:
            self.visit(stmt, scope)
        self.visit(node.expression, scope)
class GetUsedIdentifier(ASTVisitor):
    def __init__(self ):
        self.used_symbols: List[str] = []
    def visit_program(self, node: "Program", o: Any = None):
        for stmt in node.statements:
            self.visit(stmt, o)

    def visit_let_stmt(self, node: "LetStmt", o: Any = None):
        self.visit(node.expr, o)

    def visit_expr_stmt(self, node: "ExprStmt", o: Any = None):
        self.visit(node.expr, o)

    def visit_if_expr(self, node: "IfExpr", o: Any = None):
        self.visit(node.then_branch, o)
        if node.else_branch:
            self.visit(node.else_branch, o)

    def visit_list_access_expr(self, node: "ListAccessExpr", o: Any = None):
        self.visit(node.list_expr, o)
        self.visit(node.index_expr, o)

    def visit_binary_expr(self, node: "BinaryExpr", o: Any = None):
        self.visit(node.left, o)
        self.visit(node.right, o)

    def visit_func_call_expr(self, node: "FuncCallExpr", o: Any = None):
        self.visit(node.func_name, o)
        for arg in node.arguments:
            self.visit(arg, o)

    def visit_match_expr(self, node: "MatchExpr", o: Any = None):
        for case in node.cases:
            self.visit(case, o)

    def visit_match_case(self, node: "MatchCase", o: Any = None):
        self.visit(node.body, o)

    def visit_literal_expr(self, node: "LiteralExpr", o: Any = None):
        pass

    def visit_identifier_expr(self, node: "IdentifierExpr", o: Any = None):
        if node.name not in ['int', 'str', 'float', 'bool', 'print', 'filter', 'map', 'reduce'] and node.name not in self.used_symbols:
            self.used_symbols.append(node.name)
    def visit_list_expr(self, node: "ListExpr", o: Any = None):
        for element in node.elements:
            self.visit(element, o)
    def visit_unary_expr(self, node: "UnaryExpr", o: Any = None):
        self.visit(node.operand, o)
    def visit_lambda_expr(self, node: "LambdaExpr", o: Any = None):
        self.visit(node.body, o)
        for var in node.params:
            if var in self.used_symbols:
                self.used_symbols.remove(var)

    def visit_block_expr(self, node: "BlockExpr", o: Any = None):
        for stmt in node.statements:
            self.visit(stmt, o)
        self.visit(node.expression, o)