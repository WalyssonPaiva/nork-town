.PHONY: migrate
# Run database migration
migrate:
	@python manage.py db upgrade

.PHONY: migrations
# Create database migrations
migrations:
	@python manage.py db migrate

