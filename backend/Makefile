include ./pyproject_common/makefile-include

# For new checkouts; create a new venv, get poetry 
# and all dependent packages installed.
setup:
	python -m venv .venv
	pip install poetry
	poetry install

# Target to create the migrations dir if it doesn't exist
migrations:
	poetry run flask --app backend.app db init

# Note migrations is set as an order-only prerequisite
migrate_db: | migrations
	poetry run flask --app backend.app db migrate

upgrade_db:
	poetry run flask --app backend.app db upgrade

run:
	poetry run flask --debug --app backend.app run

shell:
	poetry run flask --debug --app backend.app shell

test:
	poetry run python -m pytest 
