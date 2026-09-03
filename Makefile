.PHONY: help install install-dev run build build-deploy test test-cov lint format clean clean-build clean-pyc docs

help:
	@echo "Scripts Launcher - Development Commands"
	@echo "========================================"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install        Install project dependencies"
	@echo "  install-dev    Install development dependencies"
	@echo "  run            Run the application"
	@echo "  build          Build executable (PyInstaller)"
	@echo "  build-deploy   Build and deploy executable to Desktop"
	@echo "  test           Run tests"
	@echo "  test-cov       Run tests with coverage"
	@echo "  lint           Run linting checks"
	@echo "  format         Format code with autopep8"
	@echo "  clean          Clean all build/cache files"
	@echo "  clean-build    Clean build artifacts"
	@echo "  clean-pyc      Clean Python cache files"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install pytest pytest-cov flake8 autopep8

run:
	python main.py

build:
	python build.py

build-deploy:
	python build_and_deploy.py

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	flake8 *.py tests/ --max-line-length=100

format:
	autopep8 --in-place --aggressive --max-line-length=100 *.py tests/*.py scripts/*.py

clean: clean-build clean-pyc
	rm -rf htmlcov
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf .mypy_cache

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf *.egg
	find . -name '*.whl' -delete

clean-pyc:
	find . -type f -name '*.py[cod]' -delete
	find . -type f -name '__pycache__' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true

.DEFAULT_GOAL := help
