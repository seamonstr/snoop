include ./pyproject_common/makefile-include

migrate_db:
	poetry run flask --app backend.app db migrate

upgrade_db:
	poetry run flask --app backend.app db upgrade

run:
	poetry run flask --debug --app backend.app run

shell:
	poetry run flask --debug --app backend.app shell

test:
	poetry run python -m pytest
