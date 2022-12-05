include ./pyproject_common/makefile-include

migrate_db:
	poetry run flask --app backend.app db migrate

upgrade_db:
	poetry run flask --app backend.app db upgrade
