.PHONY: install

install:
	uv pip install -e ".[dev]" 

test:
	uv run pytest
