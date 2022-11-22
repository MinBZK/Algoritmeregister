# linting

Vue linting config inspired by a repository on [Github](https://github.com/weicheng2138/nuxt3-eslint-starter).

# Prerequisites

The following tooling is required:

- Docker
- Node.js. The version is specified in `frontend/.nvmrc`. It is recommended to use use [Node version manager](https://github.com/nvm-sh/nvm), the correct Node version can then be activated with with `nvm use`.
- Python. The version is specified in `backend/.python-version`. It is recommended to use [pyenv](https://github.com/pyenv/pyenv) to switch between Python versions.
- Poetry. See the [docs](https://python-poetry.org/docs/#installation) for installation instructions.

# Setup development environment

## Environment variables

Environment variables are stored in `.env`, but because they can contain secrets (passwords), it is not in the repository. Therefore, copy and paste `.env.dummy` to `.env`. For local development, no changes are needed.

## Frontend

**Install dependencies:**

- Navigate to `/frontend/` and install packages with `npm install`.

**Linting:**

This project uses Volar. Install Volar in Visual Studio Code and enable [take over mode](https://github.com/johnsoncodehk/volar/discussions/471) to prevent unnecessary tslint errors:

1. Run Extensions: Show Built-in Extensions command
2. Update Volar to latest version.
3. Run Extensions: Show Built-in Extensions command
4. Find TypeScript and JavaScript Language Features, right click and select Disable (Workspace)
5. Reload VSCode.

## Backend

**Install dependencies:**

1. `poetry env use <python_version>`. The Python version is specified in `backend/.python-version`.
2. `poetry install`

# Start development environment

1. Open multi-root workspace: `File` > `Open workspace from file` > `/.vscode/rijksoverheid-vue-fastapi-postgres.code-workspace` or use <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> and search for `Open workspace from file`
2. Start database: `docker compose up`
3. Ensure latest migration has been completed: `poetry run alembic upgrade head`
4. Navigate to `/frontend` and run `npm run dev`.
5. Navigate to `/backend` and run `poetry run uvicorn app.main:app --reload`

## for Github:

The following tooling is required:

- Docker
- Node.js. The version is specified in `frontend/.nvmrc`. It is recommended to use use [Node version manager](https://github.com/nvm-sh/nvm), the correct Node version can then be activated with with `nvm use`.
- Python. The version is specified in `backend/.python-version`. It is recommended to use [pyenv](https://github.com/pyenv/pyenv) to switch between Python versions.
- Poetry. See the [docs](https://python-poetry.org/docs/#installation) for installation instructions.

The following steps are required for running locally:

1. Copy and paste `.env.dummy` to `.env`.
2. Navigate to `/frontend` and install packages with `npm install`.
3. run `poetry env use <python_version>`. The Python version is specified in `backend/.python-version`.
4. Navigate to `/backend` and install packages with `poetry install`
5. Start database: `docker compose up`
6. Navigate to `/backend` and run `poetry run alembic upgrade head`
7. Navigate to `/frontend` and run `npm run dev`.
8. Navigate to `/backend` and run `poetry run uvicorn app.main:app --reload`
