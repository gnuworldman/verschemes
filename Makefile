# Makefile for the Python verschemes project
# This has only been tested with GNU make from within the project root.

all: coverage build doc

test:
	PYTHONPATH=src coverage run --branch --module unittest discover

coverage: test
	coverage report

coverage_html: test
	coverage html

build:
	./setup.py build

doc:
	$(MAKE) -C docs html

clean:
	./setup.py clean -a
	$(MAKE) -C docs clean
	$(RM) -r dist
	$(RM) -r htmlcov
	coverage erase
	find . -type d -name '__pycache__' | xargs $(RM) -r
	find . -type f -name '*.py[co]' | xargs $(RM)
	git submodule update docs/_build/html
	git -C docs/_build/html checkout gh-pages

.PHONY: test coverage coverage_html build doc clean
