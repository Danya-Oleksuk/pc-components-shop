ifeq ($(OS),Windows_NT)
    VENV_BIN := .venv/Scripts
else
    VENV_BIN := .venv/bin
endif



format:
	$(VENV_BIN)/ruff format
	$(VENV_BIN)/ruff check --fix


runserver:
	$(VENV_BIN)/python ./manage.py runserver


test:
	$(VENV_BIN)/python ./manage.py test
