
install:
	poetry install

build:
	poetry build

format:pre_commit
	poetry run black switchbot_api/
	poetry run mypy switchbot_api/

clean:
	rm -rf dist

test:test_update
	poetry run pytest --cov vehicle tests

test_update:
	pytest --snapshot-update

pre_commit:
	poetry run pre-commit run end-of-file-fixer --all-files
