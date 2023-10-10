include .env

info:
	@echo "PYTHON_INTERPRETER: $(PYTHON_INTERPRETER)"
	@echo "PIP_PATH: $(PIP_PATH)"

run:
	$(PYTHON_INTERPRETER) $(file)

install:
	$(PIP_PATH) install $(module)

pip-list:
	$(PIP_PATH) list

install-requirements:
	$(PIP_PATH) install -r requirements.txt

execute:
	$(PYTHON_INTERPRETER) execute.py