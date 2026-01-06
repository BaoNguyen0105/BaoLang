import os
from typing import List, Optional, Union
from .jasmin_code import JasminCode
from .error import IllegalOperandException
from src.utils.nodes import *
from .frame import *
from src.utils.type import *

class BaoEmitter:
    def __init__(self, filename:str):
        self.filename = filename
        if not self.filename.endswith('.j'):
            self.filename += '.j'
        self.filepath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "runtime", filename
        )
        self.buff: List[str] = []
        self.jvm = JasminCode()

    def getObjectType(self)->str:
        return "Ljava/lang/Object;"
    def getIntType(self)->str:
        return "Ljava/lang/Integer;"
    def getBoolType(self)->str:
        return "Ljava/lang/Boolean;"
    def getStringType(self)->str:
        return "Ljava/lang/String;"
    def getFloatType(self)->str:
        return "Ljava/lang/Float;"
    def getArrayListType(self)->str:
        return "Ljava/util/ArrayList;"
    def getBaoLangFunctions(self)->str:
        return "baolang/BaoLangFunctions"
    def getBaoLangOperators(self)->str:
        return "baolang/BaoLangOperators"
    def getLambdaInterface(self)->str:
        return "baolang/LambdaInterface"

    def emit_class(self, class_name:str, super_class:Optional[str]=None, interfaces:Optional[str]=None):
        result=[]
        result.append(self.jvm.emitSOURCE(class_name + ".java"))
        result.append(self.jvm.emitCLASS("public "+ class_name))
        result.append(self.jvm.emitSUPER(super_class if super_class else "java/lang/Object")) 
        result.append(self.jvm.emitIMPLEMENTS(interfaces) if interfaces else "")
        return "".join(result)
    
    def emit_method_main(self, frame:Frame):
        frame.enter_scope(True)
        result=[]
        result.append(self.jvm.emitMETHOD("main", "([Ljava/lang/String;)V", isStatic=True))
        result.append(self.jvm.emitLABEL(frame.get_start_label()))
        return "".join(result)
    
    def emit_method_call(self, frame:Frame):
        frame.enter_scope(True)
        result=[]
        result.append(self.jvm.emitMETHOD("call", f"({self.getArrayListType()}){self.getObjectType()}", isStatic=False))
        result.append(self.jvm.emitLABEL(frame.get_start_label()))
        return "".join(result)
    
    def emit_method_init(self,param:List[str], frame:Frame):
        frame.enter_scope(True)
        result=[]
        result.append(self.jvm.emitMETHOD("<init>", f"({"".join(param)})V", isStatic=False))
        result.append(self.jvm.emitLABEL(frame.get_start_label()))
        return "".join(result)
    
    def emit_invoke_constructor(self,class_name:str,param_types, frame:Frame):
        frame.pop()
        for _ in param_types:
            frame.pop()
        return self.jvm.emitINVOKESPECIAL(f"{class_name}/<init>",f"({"".join(param_types)})V")
    
    def emit_field(self, name:str):
        return self.jvm.emitINSTANCEFIELD(name, self.getObjectType())
    
    def emit_get_field(self, name:str, frame:Frame):
        frame.push()
        return self.jvm.emitGETFIELD(name, self.getObjectType())
    
    def emit_put_field(self, name:str, frame:Frame):
        frame.pop()
        return self.jvm.emitPUTFIELD(name, self.getObjectType())
    
    def emit_end_method(self, frame:Frame):
        result=[]
        result.append(self.jvm.emitLABEL(frame.get_end_label()))
        result.append(self.jvm.emitLIMITSTACK(frame.get_max_op_stack_size()))
        result.append(self.jvm.emitLIMITLOCAL(frame.get_max_index()))
        result.append(self.jvm.emitENDMETHOD())
        frame.exit_scope()
        return "".join(result)
    
    def emit_end_class(self):
        file = open(self.filepath, "w")
        tmp = "".join(self.buff)
        file.write(tmp)
        file.close()
        return ""
    
    def print_out(self, code:str):
        self.buff.append(code)

    def emit_var_this(self, index:int, type_:str, frame:Frame):
        return self.jvm.emitVAR(
            index, "this", type_, frame.get_start_label(), frame.get_end_label()
            )

    def emit_var(self, index: int, name: str, frame:Frame):
        return self.jvm.emitVAR(
            index, name, self.getObjectType(), frame.get_start_label(), frame.get_end_label()
            )

    def emit_read_var(self, index, frame:Frame):
        frame.push()
        return self.jvm.emitALOAD(index)
    
    def emit_write_var(self, index, frame:Frame):
        frame.pop()
        return self.jvm.emitASTORE(index)
    
    def emit_binary_op(self, op:str, frame:Frame):
        op_map={
            "+":"add",
            "-":"sub",
            "*":"mul",
            "/":"div",
            "%":"mod",
            "&&":"and",
            "||":"or",
            ">":"gt",
            "<":"lt",
            ">=":"ge",
            "<=":"le",
            "==":"eq",
            "!=":"ne"
        }
        method_name=op_map.get(op)
        if method_name is None:
            raise IllegalOperandException(f"Illegal binary operator: {op}")
        frame.pop()
        frame.pop()
        frame.push()
        return self.jvm.emitINVOKESTATIC(
            self.getBaoLangOperators()+"/"+method_name,
            self.getFunctionType(param_count=2)
        )
    def emit_unary_op(self, op:str, frame:Frame):
        op_map={
            "-":"neg",
            "!":"not"
        }
        method_name=op_map.get(op)
        if method_name is None:
            raise IllegalOperandException(f"Illegal unary operator: {op}")
        frame.pop()
        frame.push()
        return self.jvm.emitINVOKESTATIC(
            self.getBaoLangOperators()+"/"+method_name,
            self.getFunctionType(param_count=1)
        )
    def emit_function_call(self, name:str, frame:Frame):
        frame.pop()
        frame.pop()
        frame.push()
        result=[]

        result.append(self.jvm.emitINVOKEINTERFACE(
            self.getLambdaInterface()+"/call",
            f"({self.getArrayListType()}){self.getObjectType()}",
            2
        ))
        return "".join(result)
    def emit_list_access(self, frame:Frame):
        frame.pop()
        frame.pop()
        frame.push()
        result=[]
        result.append(self.jvm.emitCHECKCAST("java/lang/Integer"))
        result.append(self.jvm.emitINVOKEVIRTUAL("java/lang/Integer/intValue","()I"))
        result.append(self.jvm.emitINVOKEVIRTUAL("java/util/ArrayList/get",
            f"(I){self.getObjectType()}"))
        return "".join(result)
    
    def emit_new_lambda(self, class_name:str, frame:Frame):
        frame.push()
        result=[]
        result.append(self.jvm.emitNEW(class_name))
        return "".join(result)
    
    def emit_new_list(self, frame:Frame):
        frame.push()
        frame.push()
        frame.pop()
        result=[]
        result.append(self.jvm.emitNEW("java/util/ArrayList"))
        result.append(self.jvm.emitDUP())
        result.append(self.jvm.emitINVOKESPECIAL("java/util/ArrayList/<init>","()V"))
        return "".join(result)
    
    def emit_push_iconst(self, in_: Union[int, str], frame:Frame) -> str:
        result=[]
        if type(in_) is int:
            frame.push()
            i = in_
            if i >= -1 and i <= 5:
                result.append(self.jvm.emitICONST(i))
            elif i >= -128 and i <= 127:
                result.append(self.jvm.emitBIPUSH(i))
            elif i >= -32768 and i <= 32767:
                result.append(self.jvm.emitSIPUSH(i))
            else:
                result.append(self.jvm.emitLDC(str(i)))
        elif type(in_) is str:
            result.append(self.emit_push_iconst(int(in_), frame))
        result.append(self.jvm.emitINVOKESTATIC("java/lang/Integer/valueOf",
            "(I)Ljava/lang/Integer;"))
        return "".join(result)
            
    def emit_push_fconst(self, in_: str, frame:Frame) -> str:
        """
        Emit instruction to push float constant onto operand stack.

        Args:
            in_: String representation of float value
            frame: Frame object for stack management

        Returns:
            Generated JVM instruction string
        """
        f = float(in_)
        frame.push()
        rst = "{0:.4f}".format(f)
        result=[]
        if rst == "0.0000" or rst == "1.0000" or rst == "2.0000":
            result.append(self.jvm.emitFCONST(rst[:3]))
        else:
            result.append(self.jvm.emitLDC(rst))
        result.append(self.jvm.emitINVOKESTATIC("java/lang/Float/valueOf",
            "(F)Ljava/lang/Float;"))
        return "".join(result)
    def emit_push_sconst(self, in_: str, frame:Frame) -> str:
        frame.push()
        result=[]
        result.append(self.jvm.emitLDC(f"\"{in_}\""))
        return "".join(result)
    
    def emit_push_bconst(self, in_: bool, frame:Frame) -> str:
        frame.push()
        result=[]
        if in_ == True:
            result.append(self.jvm.emitICONST(1))
        elif in_ == False:
            result.append(self.jvm.emitICONST(0))
        else:
            raise IllegalOperandException(f"Illegal bollean constant: {in_}")
        result.append(self.jvm.emitINVOKESTATIC("java/lang/Boolean/valueOf",
            "(Z)Ljava/lang/Boolean;"))
        return "".join(result)

    
    def emit_dup(self, frame:Frame):
        frame.push()
        return self.jvm.emitDUP()
    def emit_list_add(self, frame:Frame):
        frame.pop()
        frame.pop()

        result=[]
        result.append(self.jvm.emitINVOKEVIRTUAL("java/util/ArrayList/add",
            f"({self.getObjectType()})Z"))
        result.append(self.jvm.emitPOP())
        return "".join(result)

    def emit_return(self, frame:Frame):
        frame.pop()
        return self.jvm.emitARETURN()
    
    def emit_if_false(self, label:int, frame:Frame):
        frame.pop()
        result=[]
        result.append(self.jvm.emitCHECKCAST("java/lang/Boolean"))
        result.append(self.jvm.emitINVOKEVIRTUAL("java/lang/Boolean/booleanValue","()Z"))
        result.append(self.jvm.emitIFEQ(label))
        return "".join(result)
    
    def emit_goto(self, label:int):
        return self.jvm.emitGOTO(label)
    def emit_label(self, label:int):
        return self.jvm.emitLABEL(label)
    def emit_nop(self, frame:Frame):
        return self.jvm.emitNOP()
    def emit_pop(self, frame:Frame):
        frame.pop()
        return self.jvm.emitPOP()
    def getFunctionType(self, param_count:int)->str:
        param_types = self.getObjectType() * param_count
        return f"({param_types}){self.getObjectType()}"
    
    def emit_invoke_baolang_function(self, name:str, param_count:int, frame:Frame):
        for _ in range(param_count):
            frame.pop()
        frame.push()
        return self.jvm.emitINVOKESTATIC(
            self.getBaoLangFunctions()+"/"+name,
            self.getFunctionType(param_count=param_count)
        )