# see https://makefiletutorial.com/

SHELL := /bin/bash -eu -o pipefail

update_pip_and_wheel:
	pip install -U pip wheel

install_prod:
	pip install  '.[ui]'

install_dev:
	pip install -e '.[dev,ui]'

wheel:
	pip install build twine
	python -m build . --wheel

isort:
	isort src tests $${ARGS:-}

pylint:
	pylint src tests

coverage_run:
	coverage run -m pytest -m 'not integration'

coverage_report:
	coverage report

coverage_report_html:
	coverage html

coverage: coverage_run coverage_report

mypy:
	mypy src

pip-audit:
	pip-audit --ignore-vuln=PYSEC-2022-42969

code_check: \
	isort \
	pylint \
	coverage_run coverage_report \
	mypy \
	pip-audit
