.PHONY: install run run-csv run-verlet run-luna test test-pure clean help

PYTHON := python

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) main.py

run-csv:
	$(PYTHON) main.py --salida csv

run-verlet:
	$(PYTHON) main.py --metodo verlet

run-luna:
	$(PYTHON) main.py --g 1.62

test:
	$(PYTHON) -m pytest tests/ -v

test-pure:
	$(PYTHON) -m venv .venv_pure
	.venv_pure/Scripts/pip install pytest -q
	.venv_pure/Scripts/pytest tests/test_dominio.py -v
	@echo "OK — el dominio pasa sin numpy ni matplotlib"

clean:
	powershell -Command "Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force"
	powershell -Command "Get-ChildItem -Recurse -Filter *.pyc | Remove-Item -Force"
	-del resultados.csv 2>NUL

help:
	@echo "Comandos disponibles:"
	@echo "  make install     instala dependencias"
	@echo "  make run         ejecuta simulacion normal"
	@echo "  make run-csv     ejecuta simulacion y exporta CSV"
	@echo "  make run-verlet  ejecuta con metodo Verlet"
	@echo "  make run-luna    ejecuta con gravedad lunar"
	@echo "  make test        corre tests"
	@echo "  make clean       limpia archivos generados"