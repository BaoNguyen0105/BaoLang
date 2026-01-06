"""Semantic Error Classes for BaoLang"""
import warnings
from antlr4.error.ErrorListener import ErrorListener

def custom_format(message, category, filename, lineno, line=None):
    # This changes the output to a clean, one-line format
    return f'warning - {message}\n'

# Apply the new format
warnings.formatwarning = custom_format

class StaticError(Exception):
    """Base class for all static semantic errors in OPLang"""
    pass

class TypeMismatchInExpression(StaticError):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f"Type Mismatch In Expression: {self.expr}"
    
class UndeclaredIdentifier(StaticError):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Undefined Identifier: {self.name}"
    
class RedeclaredIdentifier(StaticError):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Redeclared Identifier: {self.name}"

class IllegalArrayLiteral(StaticError):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f"Illegal Array Literal: {self.expr}"
    
class IncompleteIfExpression(StaticError):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f"Incomplete If Expression: {self.expr}"
    
class NonExhaustiveMatch(StaticError):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f"Non Exhaustive Match Cases: {self.expr}"

class IdentifierNotFunction(StaticError):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Identifier Not Function: {self.name}"
    
class IdentifierNotList(StaticError):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Identifier Not Array: {self.name}"

class IdentifierIsReserved(StaticError):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Identifier Is Reserved: {self.name}"    

class ListAccessMustBeInteger(StaticError):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f"List Access Must Be Integer: {self.expr}"
    
class IfConditionNotBoolean(StaticError):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f"If Condition Not Boolean: {self.expr}"
    
class TooManyArguments(StaticError):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f"Too Many Arguments In Function Call: {self.expr}"
    
class TooFewArguments(StaticError):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f"Too Few Arguments In Function Call: {self.expr}"
    
class CircularDependency(StaticError):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Circular Dependency Detected: {self.name}"

class IdentifierShadowing(Warning):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Identifier Shadowing Warning: {self.name}"
    
class UnusedVariable(Warning):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Unused Variable Warning: {self.name}"
    
class BaoError(Exception):
    """Base class for all BaoLang errors."""
    def __init__(self, static_error: StaticError, line: int = None, column: int = None):
        self.static_error = static_error
        self.line = line
        self.column = column

    def __str__(self):
        return f"[Line {self.line}, Column {self.column}] {self.static_error}"
    
class BaoParserErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # Raise BaoError so main.py catches it
        raise BaoError(f"Syntax Error: {msg}", line, column)