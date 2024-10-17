set -e

PYRIGHT_PYTHON_FORCE_VERSION=v1.1.332
poetry run python -m black app tests common alembic/versions
poetry run python -m flake8 app tests common
poetry run pyright app tests common
# poetry run isort app --check-only