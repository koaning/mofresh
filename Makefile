.PHONY: install, test, clean, pypi, docs

install:
	uv pip install -e ".[dev]" 

test:
	uv run pytest

clean:
	rm -rf .pytest_cache
	rm -rf */__pycache__
	rm -rf dist
pypi: clean
	uv build
	uv publish

docs: 
	uv run marimo export html-wasm demo.py -o docs/index.html --mode edit