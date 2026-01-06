"""Module defining types used in BaoLang semantic analysis."""
from typing import Dict, List, Set, Optional, Any, Tuple, Union, NamedTuple
from abc import ABC, abstractmethod
from ..semantic.error import *
import operator

def is_bool(type_):
    return isinstance(type_, BoolType)
def is_int(type_):
    return isinstance(type_, IntType)
def is_float(type_):
    return isinstance(type_, FloatType)
def is_string(type_):
    return isinstance(type_, StringType)
def is_list(type_):
    return isinstance(type_, ListType)
def is_func(type_):
    return isinstance(type_, FuncType)
def is_undifined(type_):
    return isinstance(type_, UndefinedType)
def is_same_type(type1, type2):
    return isinstance(type1, type(type2)) or isinstance(type2, type(type1))


class Type(ABC):
    """Base class for all types in BaoLang"""
    @abstractmethod
    def __str__(self):
        pass
    
    def __neg__(self):
        raise TypeMismatchInExpression(f"Cannot negate {self}")
    def __add__(self, other):
        raise TypeMismatchInExpression(f"Cannot add {self} and {other}")
    def __sub__(self, other):
        raise TypeMismatchInExpression(f"Cannot sub {self} and {other}")
    def __mul__(self, other):
        raise TypeMismatchInExpression(f"Cannot mul {self} and {other}")
    def __truediv__(self, other):
        raise TypeMismatchInExpression(f"Cannot div {self} and {other}")
    def __mod__(self, other):
        raise TypeMismatchInExpression(f"Cannot mod {self} and {other}")
    def __eq__(self, other):
        raise TypeMismatchInExpression(f"Cannot compare {self} eq {other}")
    def __ne__(self, other):
        raise TypeMismatchInExpression(f"Cannot compare {self} ne {other}")
    def __lt__(self, other):
        raise TypeMismatchInExpression(f"Cannot compare {self} lt {other}")
    def __le__(self, other):
        raise TypeMismatchInExpression(f"Cannot compare {self} le {other}")
    def __gt__(self, other):
        raise TypeMismatchInExpression(f"Cannot compare {self} gt {other}")
    def __ge__(self, other):
        raise TypeMismatchInExpression(f"Cannot compare {self} ge {other}")
    def __and__(self, other):
        raise TypeMismatchInExpression(f"Cannot and {self} and {other}")
    def __or__(self, other):
        raise TypeMismatchInExpression(f"Cannot or {self} and {other}")
    def __not__(self):
        raise TypeMismatchInExpression(f"Cannot not {self}")


class IntType(Type):
    def __str__(self):
        return "int"
    def _basic_op(self,other, strict=False):
        if isinstance(other, IntType):
            return IntType()
        
        if not strict:
            if isinstance(other, FloatType):
                return FloatType()
        
        raise TypeMismatchInExpression(f"Cannot operate {self} and {other}")
    def __add__(self, other):
        try:
            return self._basic_op(other)
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot add {self} and {other}")
    def __sub__(self, other):
        try:
            return self._basic_op(other)
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot subtract {self} and {other}")
    def __mul__(self, other):
        try:
            return self._basic_op(other)
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot multiply {self} and {other}")
    def __truediv__(self, other):
        try:
            return self._basic_op(other)
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot divide {self} and {other}")
    def __mod__(self, other):
        try:
            return self._basic_op(other, strict=True)
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot modulo {self} and {other}")
    def __eq__(self, other):
        try:
            self._basic_op(other)
            return BoolType()
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot compare {self} eq {other}")
    def __ne__(self, other):
        try:
            self._basic_op(other)
            return BoolType()
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot compare {self} ne {other}")
    def __lt__(self, other):
        try:
            self._basic_op(other)
            return BoolType()
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot compare {self} lt {other}")
    def __le__(self, other):
        try:
            self._basic_op(other)
            return BoolType()
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot compare {self} le {other}")
    def __gt__(self, other):
        try:
            self._basic_op(other)
            return BoolType()
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot compare {self} gt {other}")
    def __ge__(self, other):
        try:
            self._basic_op(other)
            return BoolType()
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot compare {self} ge {other}")
    def __neg__(self):
        return IntType()

    
class BoolType(Type):
    def __str__(self):
        return "bool"
    def _basic_op(self, other):
        if isinstance(other, BoolType):
            return BoolType()
        raise TypeMismatchInExpression(f"Cannot operate {self} and {other}")
    def __and__(self, other):
        try:
            return self._basic_op(other)
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot and {self} and {other}")
    def __or__(self, other):
        try:
            return self._basic_op(other)
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot or {self} and {other}")
    def __not__(self):
        return BoolType()
    def __eq__(self, other):
        try:
            return self._basic_op(other)
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot compare {self} eq {other}")
    def __ne__(self, other):
        try:
            return self._basic_op(other)
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot compare {self} ne {other}")
    
class StringType(Type):
    def __str__(self):
        return "string"
    def _basic_op(self, other):
        if isinstance(other, StringType):
            return StringType()
        raise TypeMismatchInExpression(f"Cannot operate {self} and {other}")
    def __add__(self, other):
        try:
            return self._basic_op(other)
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot add {self} and {other}")
    def __eq__(self, other):
        try:
            self._basic_op(other)
            return BoolType()
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot compare {self} eq {other}")
    def __ne__(self, other):
        try:
            self._basic_op(other)
            return BoolType()
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot compare {self} ne {other}")
    
class FloatType(Type):
    def __str__(self):
        return "float"
    def _basic_op(self,other):
        if isinstance(other, IntType):
            return FloatType()
        if isinstance(other, FloatType):
            return FloatType()
        raise TypeMismatchInExpression(f"Cannot operate {self} and {other}")
    def __add__(self, other):
        try:
            return self._basic_op(other)
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot add {self} and {other}")
    def __sub__(self, other):
        try:
            return self._basic_op(other)
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot subtract {self} and {other}")
    def __mul__(self, other):
        try:
            return self._basic_op(other)
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot multiply {self} and {other}")
    def __truediv__(self, other):
        try:
            return self._basic_op(other)
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot divide {self} and {other}")
    def __eq__(self, other):
        try:
            self._basic_op(other)
            return BoolType()
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot compare {self} eq {other}")
    def __ne__(self, other):
        try:
            self._basic_op(other)
            return BoolType()
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot compare {self} ne {other}")
    def __lt__(self, other):
        try:
            self._basic_op(other)
            return BoolType()
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot compare {self} lt {other}")
    def __le__(self, other):
        try:
            self._basic_op(other)
            return BoolType()
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot compare {self} le {other}")
    def __gt__(self, other):
        try:
            self._basic_op(other)
            return BoolType()
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot compare {self} gt {other}")
    def __ge__(self, other):
        try:
            self._basic_op(other)
            return BoolType()
        except TypeMismatchInExpression:
            raise TypeMismatchInExpression(f"Cannot compare {self} ge {other}")
    def __neg__(self):
        return FloatType()

class FuncType(Type):
    id=0
    def __init__(self, param_len:int, return_type: Type):
        self.param_len = param_len
        self.return_type = return_type
        self.id = FuncType.id
        FuncType.id += 1

    def __str__(self):
        return f"function"
    
    def __eq__(self, other):
        if isinstance(other, FuncType) and self.id == other.id:
            return BoolType()
        raise TypeMismatchInExpression(f"Cannot compare {self} and {other}")
    
    def __ne__(self, other):
        if isinstance(other, FuncType) and self.id == other.id:
            return BoolType()
        raise TypeMismatchInExpression(f"Cannot compare {self} and {other}")


class ListType(Type):
    def __init__(self):
        pass

    def __str__(self):
        return f"list"
    def __add__(self, other):
        if isinstance(other, ListType):
            return ListType()
        raise TypeMismatchInExpression(f"Cannot add {self} and {other}")
    def __mul__(self, other):
        if isinstance(other, IntType):
            return ListType()
        raise TypeMismatchInExpression(f"Cannot multiply {self} and {other}")
    def __eq__(self, other):
        if isinstance(other, ListType):
            return BoolType()
        raise TypeMismatchInExpression(f"Cannot compare {self} and {other}")
    def __ne__(self, other):
        if isinstance(other, ListType):
            return BoolType()
        raise TypeMismatchInExpression(f"Cannot compare {self} and {other}")

class UndefinedType(IntType, FloatType, StringType, BoolType, ListType, FuncType):
    def __str__(self):
        return "undifined"
    def __neg__(self):
        if isinstance(self, (UndefinedType, IntType, FloatType)):
            return self 
        raise TypeMismatchInExpression(f"Cannot negate {self}")   
    def __add__(self, other):
        if isinstance(other, (UndefinedType, IntType, FloatType, StringType, ListType)):
            return other 
        raise TypeMismatchInExpression(f"Cannot add {self} and {other}")
    def __sub__(self, other):
        if isinstance(other, (UndefinedType, IntType, FloatType)):
            return other
        raise TypeMismatchInExpression(f"Cannot sub {self} and {other}")
    def __mul__(self, other):
        if isinstance(other, (UndefinedType, IntType, FloatType, ListType)):
            return other  
        raise TypeMismatchInExpression(f"Cannot mul {self} and {other}")
    def __truediv__(self, other):
        if isinstance(other, (UndefinedType, IntType, FloatType)):
            return other 
        raise TypeMismatchInExpression(f"Cannot div {self} and {other}")   
    def __mod__(self, other):
        if isinstance(other, (UndefinedType, IntType)):
            return other
        raise TypeMismatchInExpression(f"Cannot mod {self} and {other}") 
    def __eq__(self, other):
        return BoolType()    
    def __ne__(self, other):
        return BoolType()    
    def __lt__(self, other):
        return BoolType()     
    def __le__(self, other):
        return BoolType()     
    def __gt__(self, other):
        return BoolType()     
    def __ge__(self, other):
        return BoolType()     
    def __and__(self, other):
        if isinstance(other,(UndefinedType, BoolType)):
            return BoolType()
        raise TypeMismatchInExpression(f"Cannot and {self} and {other}")    
    def __or__(self, other):
        if isinstance(other,(UndefinedType, BoolType)):
            return BoolType()
        raise TypeMismatchInExpression(f"Cannot or {self} and {other}")
    def __not__(self):
        if isinstance(self,(UndefinedType, BoolType)):
            return BoolType()
        raise TypeMismatchInExpression(f"Cannot not {self}")