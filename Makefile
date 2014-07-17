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

github_readme:
	test "`head -1 README`" = ".. include:: docs/description.rst"
	$(RM) README.rst
	echo 'This file was produced with no help from GitHub, who refuse to implement the include directive or reuse a non-broken reStructuredText processor.  Maybe someday they will realize that DRY does not stand for "Definitely Repeat Yourself" and that it is rude to force workarounds upon your users.\n\nWe now return you to your regularly scheduled program (or library).\n' > README.rst
	cat docs/description.rst >> README.rst
	tail -n +2 README >> README.rst

doc: github_readme
	$(MAKE) -C docs html

clean:
	./setup.py clean -a
	$(MAKE) -C docs clean
	$(RM) MANIFEST
	$(RM) -r dist
	$(RM) -r htmlcov
	coverage erase
	find . -type d -name '__pycache__' | xargs $(RM) -r
	find . -type f -name '*.py[co]' | xargs $(RM)
	git submodule update docs/_build/html
	git -C docs/_build/html checkout gh-pages

.PHONY: test coverage coverage_html build github_readme doc clean
