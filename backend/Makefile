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

# Note migrations is set as an order-only prerequisite;
# will trigger migrations target if the dir doesn't exist,
# but not if it does, regardless of the dir's timestamp
migrate_db: | migrations
	poetry run flask --app backend.app db migrate

# For dev purposes; utilities to update your dev DB
upgrade_db:
	poetry run flask --app backend.app db upgrade

run:
	poetry run flask --debug --app backend.app run

# Start a shell with Flask app initialised; SqlAlchemy puts 
# references  to the model classes and "db" object in the shell's
# global scope.
shell:
	poetry run flask --app backend.app shell

# Run all unit tests
test:
	poetry run python -m pytest 

clean:
	rm -rf dist

build: clean
	./docker_build.sh