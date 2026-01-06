from functools import reduce
from build.BaoLangVisitor import BaoLangVisitor
from build.BaoLangParser import BaoLangParser
from src.utils.nodes import *

class ASTGen(BaoLangVisitor):
    """AST Generator that converts parse trees into AST nodes."""

    def visitProgram(self, ctx: BaoLangParser.ProgramContext) -> Program:
        statements = [self.visit(stmt) for stmt in ctx.stmt()]
        line = ctx.start.line
        column = ctx.start.column
        return Program(statements, line, column)

    def visitStmt(self, ctx: BaoLangParser.StmtContext) -> Stmt:
        if ctx.letStmt():
            return self.visitLetStmt(ctx.letStmt())
        elif ctx.exprStmt():
            return self.visitExprStmt(ctx.exprStmt())
        else:
            raise Exception("Unknown statement type")
        
    def visitLetStmt(self, ctx: BaoLangParser.LetStmtContext) -> LetStmt:
        name = ctx.ID().getText()
        expr = self.visit(ctx.expr())
        line = ctx.start.line
        column = ctx.start.column
        return LetStmt(name, expr, line, column)

    def visitExprStmt(self, ctx: BaoLangParser.ExprStmtContext) -> ExprStmt:
        expr = self.visit(ctx.expr())
        line = ctx.start.line
        column = ctx.start.column
        return ExprStmt(expr, line, column)
    
    def visitIfExpr2(self, ctx: BaoLangParser.IfExpr2Context) -> IfExpr:
        condition = self.visit(ctx.expr(0))
        then_branch = self.visit(ctx.expr(1))
        else_branch = self.visit(ctx.expr(2)) if ctx.expr(2) else None
        line = ctx.start.line
        column = ctx.start.column
        return IfExpr(condition, then_branch, else_branch, line, column)
    
    def visitListAccessExpr(self, ctx: BaoLangParser.ListAccessExprContext) -> ListAccessExpr:
        list_expr = self.visit(ctx.expr(0))
        index_expr = self.visit(ctx.expr(1))
        line = ctx.start.line
        column = ctx.start.column
        return ListAccessExpr(list_expr, index_expr, line, column)    
    
    def visitAddSubExpr(self, ctx: BaoLangParser.AddSubExprContext) -> Expr:
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        operator = ctx.PLUS().getText() if ctx.PLUS() else ctx.MINUS().getText()
        line = ctx.start.line
        column = ctx.start.column
        return BinaryExpr(left, operator, right, line, column)
    
    def visitMatchExpr(self, ctx: BaoLangParser.MatchExprContext) -> MatchExpr:
        matched_expr = self.visit(ctx.expr())
        cases = reduce(lambda acc, case_ctx: acc + self.visit(case_ctx), ctx.matchCase(), [])
        line = ctx.start.line
        column = ctx.start.column
        return MatchExpr(matched_expr, cases, line, column)
    
    def visitMulDivModExpr(self, ctx: BaoLangParser.MulDivModExprContext) -> Expr:
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        operator = None
        if ctx.MULTIPLY():
            operator = ctx.MULTIPLY().getText()
        elif ctx.DIVIDE():
            operator = ctx.DIVIDE().getText()
        elif ctx.MODULO():
            operator = ctx.MODULO().getText()
        line = ctx.start.line
        column = ctx.start.column
        return BinaryExpr(left, operator, right, line, column)
    
    def visitFuncCallExpr(self, ctx: BaoLangParser.FuncCallExprContext) -> FuncCallExpr:
        func_name = self.visit(ctx.expr(0))
        args = [self.visit(arg) for arg in ctx.expr()][1:]
        line = ctx.start.line
        column = ctx.start.column
        return FuncCallExpr(func_name, args, line, column)
    
    def visitParenExpr(self, ctx):
        return self.visit(ctx.expr())
    
    def visitEqExpr(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        operator = ctx.EQUAL().getText() if ctx.EQUAL() else ctx.NOTEQUAL().getText()
        line = ctx.start.line
        column = ctx.start.column
        return BinaryExpr(left, operator, right, line, column)
    
    def visitNotExpr(self, ctx):
        operand = self.visit(ctx.expr())
        operator = ctx.NOT().getText()
        line = ctx.start.line
        column = ctx.start.column
        return UnaryExpr(operator, operand, line, column)
    
    def visitLambdaExpr(self, ctx):
        params = self.visit(ctx.paramList()) if ctx.paramList() else []
        body = self.visit(ctx.expr())
        line = ctx.start.line
        column = ctx.start.column
        return LambdaExpr(params, body, line, column)
    
    def visitNegExpr(self, ctx):
        operand = self.visit(ctx.expr())
        operator = ctx.MINUS().getText()
        line = ctx.start.line
        column = ctx.start.column
        return UnaryExpr(operator, operand, line, column)
    
    def visitLogicExpr(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        operator = None
        if ctx.AND():
            operator = ctx.AND().getText()
        elif ctx.OR():
            operator = ctx.OR().getText()
        line = ctx.start.line
        column = ctx.start.column
        return BinaryExpr(left, operator, right, line, column)
    
    def visitBlockExpr(self, ctx):
        stmts = [self.visit(stmt) for stmt in ctx.stmt()]
        expr= self.visit(ctx.expr())
        line = ctx.start.line
        column = ctx.start.column
        return BlockExpr(stmts, expr, line, column)
    
    def visitRelExpr(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        operator = None
        if ctx.LT():
            operator = ctx.LT().getText()
        elif ctx.LE():
            operator = ctx.LE().getText()
        elif ctx.GT():
            operator = ctx.GT().getText()
        elif ctx.GE():
            operator = ctx.GE().getText()
        line = ctx.start.line
        column = ctx.start.column
        return BinaryExpr(left, operator, right, line, column)
    
    def visitLitExpr(self, ctx):
        line = ctx.start.line
        column = ctx.start.column
        if ctx.INTLIT():
            value = int(ctx.INTLIT().getText())
            return IntLit(value, line, column)
        elif ctx.FLOATLIT():
            value = float(ctx.FLOATLIT().getText())
            return FloatLit(value, line, column)
        elif ctx.STRINGLIT():
            value = ctx.STRINGLIT().getText()
            return StringLit(value, line, column)
        elif ctx.BOOLLIT():
            value = ctx.BOOLLIT().getText() == "true"
            return BoolLit(value, line, column)
        else:
            raise Exception("Unknown literal type")
    
    def visitListExpr(self, ctx):
        elements = [self.visit(elem) for elem in ctx.expr()]
        line = ctx.start.line
        column = ctx.start.column
        return ListExpr(elements, line, column)
    
    def visitIfExpr1(self, ctx):
        condition = self.visit(ctx.expr(0))
        then_branch = self.visit(ctx.expr(1))
        else_branch = self.visit(ctx.expr(2)) if ctx.expr(2) else None
        line = ctx.start.line
        column = ctx.start.column
        return IfExpr(condition, then_branch, else_branch, line, column)
    
    def visitIdExpr(self, ctx: BaoLangParser.IdExprContext) -> IdentifierExpr:
        name = ctx.ID().getText()
        line = ctx.start.line
        column = ctx.start.column
        return IdentifierExpr(name, line, column)
    
    def visitMatchCase(self, ctx: BaoLangParser.MatchCaseContext) -> MatchCase:
        patterns = self.visit(ctx.pattern())
        body = self.visit(ctx.expr())
        line = ctx.start.line
        column = ctx.start.column
        return [MatchCase(pattern, body, line, column) for pattern in patterns]
    
    def visitPattern(self, ctx):
        line = ctx.start.line
        column = ctx.start.column
        if ctx.INTLIT():
            value = int(ctx.INTLIT().getText())
            return [IntLit(value, line, column)]
        elif ctx.FLOATLIT():
            value = float(ctx.FLOATLIT().getText())
            return [FloatLit(value, line, column)]
        elif ctx.STRINGLIT():
            value = ctx.STRINGLIT().getText()
            return [StringLit(value, line, column)]
        elif ctx.BOOLLIT():
            value = ctx.BOOLLIT().getText() == "true"
            return [BoolLit(value, line, column)]
        elif ctx.ID():
            name = ctx.ID().getText()
            return [IdentifierExpr(name, line, column)]
        elif ctx.DEFAULT():
            return [None]
        elif ctx.pattern():
            return [self.visit(pattern) for pattern in ctx.pattern()]
    
    def visitParamList(self, ctx):
        return [id.getText() for id in ctx.ID()]
    
    
    
    
    
    
