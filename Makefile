run-ruff-check:
	ruff check
run-ruff-check-fix:
	ruff check --fix
run-ruff-check-watch:
	ruff check --watch
run-ruff-format:
	ruff format
check-python-version:
	python3 --version
list-poetry-config:
	poetry config --list
check-poetry-version:
	poetry --version
clean:
	pyclean .