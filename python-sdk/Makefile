.PHONY: run test requierments.txt pipclean

run:
	PYTHONPATH=. python ezd/cli/main.py

test:
	PYTHONPATH=. pytest

requierments.txt:
	pip freeze > requierments.txt

pipclean:
	pip freeze | xargs pip uninstall -y

pipinstall:
	pip install -r requierments.txt