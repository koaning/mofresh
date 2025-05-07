.PHONY: install

install:
	uv pip install -e ".[dev]" 

test:
	uv run pytest

clean:
	rm -rf .pytest_cache
	rm -rf */__pycache__

pypi: clean
	uv build
	uv publish
