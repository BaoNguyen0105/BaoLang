import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "build"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "build", "lexererr"))

from antlr4 import *
from build.BaoLangLexer import BaoLangLexer
from build.BaoLangParser import BaoLangParser
from src.astgen.astgen import ASTGen
from semantic.checker import StaticChecker
from src.utils.nodes import Program
from src.semantic.error import *
from lexererr import UncloseString, IllegalEscape, ErrorToken
from src.codegen.codegen import CodeGen
from src.codegen.error import IllegalOperandException, IllegalRuntimeException
import traceback

import linecache

if len(sys.argv) >1:
    filename = sys.argv[1]
else:
    filename = "test.bao"

def error_display(error, filename, line, column):
    line_text = linecache.getline(filename, line).strip('\n')
    pointer=' ' * (column) + '^'
    error_report = [
        f"\n--- {filename} ---",
        f"Error at [Line {line}, Col {column}]: {error}",
        f"  {line} | {line_text}",
        f"    | {pointer}",
        "------------------------"
    ]
    return "\n".join(error_report)

def main():
    # 1. Take input from a file or string
    # Replace 'test.bao' with your actual code file
    input_stream = FileStream(filename)

    # 2. Initialize Lexer and Parser
    lexer = BaoLangLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(BaoParserErrorListener())
    stream = CommonTokenStream(lexer)
    parser = BaoLangParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(BaoParserErrorListener())

    # 3. Start parsing at the 'program' rule
    try:
        # 4. Generate Parse Tree (CST)
        parse_tree = parser.program()
        #print("1. Parsing successful (CST generated).")

        # 5. Generate Abstract Syntax Tree (AST)
        ast_generator = ASTGen()
        ast = ast_generator.visit(parse_tree)
        #print("2. AST Generation successful.")

        # 6. Debug: Print the AST to verify (requires a __repr__ in your nodes)
        # print("\n--- Abstract Syntax Tree ---")
        # print(ast)

        # 7. Perform Static Semantic Checking
        static_checker = StaticChecker()
        static_checker.check(ast)
        #print("3. Static Semantic Checking successful.")

        # 8. Generate Bytecode
        code_generator = CodeGen()
        bytecode = code_generator.generate(ast)
        #print("4. Bytecode Generation successful.")

    except BaoError as e:
        print(error_display(e.static_error, filename, e.line, e.column))
        sys.exit(1)
        
    except (UncloseString, IllegalEscape, ErrorToken) as e:
        print(error_display(e, filename, lexer.line, lexer.column-1))
        sys.exit(1)

    except (IllegalOperandException, IllegalRuntimeException) as e:
        print(f"Code Generation Error: {e}")
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(type(e))
        print(f"Error during compilation: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()