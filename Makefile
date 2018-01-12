.PHONY: clean-pyc clean-build docs
BUILDDIR = ./~build

help:
	@echo "fullclean           remove build artifacts"
	@echo "clean               remove Python file artifacts"
	@echo "qa                  check style with flake8"
	@echo "develop             setup development environment"


.setup-git:
	git config branch.autosetuprebase always
	chmod +x hooks/*
	cd .git/hooks && ln -fs ../../hooks/* .

clean:
	rm -fr ${BUILDDIR} dist *.egg-info .coverage pep8.out \
	    coverage.xml flake.out pytest.xml MANIFEST
	find src -name __pycache__ -o -name "*.py?" -o -name "*.orig" -prune | xargs rm -rf
	find src -name django.mo | xargs rm -f


fullclean:
	@rm -fr .tox .cache
	$(MAKE) clean

develop:
	pip install -U pip
	pip install -e .[dev]
	$(MAKE) .setup-git

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr docs/_build
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

qa:
	flake8 src/drf_querystringfilter tests
	isort -rc drf_querystringfilter tests --check-only
	check-manifest

docs:
	rm -f docs/drf-querystringfilter.rst
	rm -f docs/modules.rst
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
