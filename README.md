# BaoLang

BaoLang is a clean, functional-oriented language designed for simplicity and logic. It features first-class functions, automatic memory management, and powerful pattern matching.

## Key Features

* **Functional First**: Functions are values. Pass them, return them, and compose them.
* **Smart Closures**: Functions remember the variables from where they were created.
* **Currying**: Easily transform a function with multiple arguments into a chain of nested functions.
* **Pattern Matching**: Use the `match` expression for elegant and readable logic branching.
* **Recursion**: Built-in support for self-referencing recursive logic.

## File Structure
.
├── external
│   ├── antlr-4.13.2-complete.jar
│   └── jasmin.jar
├── src
│   ├── astgen
│   │   └── astgen.py
│   ├── codegen
│   │   ├── BaoEmitter.py
│   │   ├── baolang
│   │   │   ├── BaoLangFunctions.java
│   │   │   ├── BaoLangOperators.java
│   │   │   └── LambdaInterface.java
│   │   ├── codegen.py
│   │   ├── emitter.py
│   │   ├── error.py
│   │   ├── frame.py
│   │   └── jasmin_code.py
│   ├── grammar
│   │   ├── BaoLang.g4
│   │   └── lexererr.py
│   ├── semantic
│   │   ├── checker.py
│   │   └── error.py
│   └── utils
│       ├── nodes.py
│       ├── type.py
│       └── visitor.py
├── Makefile
├── requirements.txt
├── main.py
└── test.bao


## Getting Started
### 0. Install necessary dependencies
```bash
make venv
```

### 1. Compile your Code
Turn your `.bao` source file into executable instructions:
```bash
make file <<filename>>.bao
```
### 2. Build and Run
Use the build tool to finalize the executable and run it:
```bash
make run
```


