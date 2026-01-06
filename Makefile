EXTERNAL_DIR=$(CURDIR)/external
GRAMMAR_DIR=$(CURDIR)/src/grammar
BUILD_DIR=$(CURDIR)/build
SRC_DIR=$(CURDIR)/src


ANTLR_VERSION=4.13.2
VENV = venv
PYTHON = $(VENV)/bin/python
ARGS = $(filter-out $@,$(MAKECMDGOALS))
RUNTIME_DIR=$(SRC_DIR)/runtime
BAOLANG_DIR=$(SRC_DIR)/codegen/baolang

.PHONY: grammar build clear test

grammar: build
	@java -jar $(EXTERNAL_DIR)/antlr-$(ANTLR_VERSION)-complete.jar -Dlanguage=Python3 -visitor $(GRAMMAR_DIR)/BaoLang.g4 -o $(BUILD_DIR)
	@cp $(GRAMMAR_DIR)/lexererr.py $(BUILD_DIR)/
	@touch $(BUILD_DIR)/__init__.py

build:
	@mkdir -p $(BUILD_DIR)

test: grammar baolang
	@PYTHONPATH=$(BUILD_DIR):$(SRC_DIR):$$PYTHONPATH $(PYTHON) main.py $(ARGS)
	@java -jar $(EXTERNAL_DIR)/jasmin.jar $(RUNTIME_DIR)/*.j -d $(RUNTIME_DIR) > /dev/null
	@java -cp $(RUNTIME_DIR):. Main 

baolang:
	@javac -d $(RUNTIME_DIR) $(BAOLANG_DIR)/*.java -nowarn > /dev/null
clear:
	@rm -rf $(BUILD_DIR)
	@rm -rf $(RUNTIME_DIR)/*.j
	@rm -rf $(RUNTIME_DIR)/*.class

venv:
	@echo "installing the necessary dependencies..."
	@python3 -m venv $(VENV)
	@./$(VENV)/bin/pip install -r requirements.txt
	@echo "Installation completed"
%:
	@: