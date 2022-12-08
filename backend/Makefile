include ./pyproject_common/makefile-include

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
