# About the Algorithm Register

The Ministry of the Interior and Kingdom Relations is developing the Algorithm Register. The team does this using an open development style, through open source software. Anyone can view the team’s progress on the GitHub of the Ministry of the Interior and Kingdom Relations. The Algorithm Register is under development. The content changes over time. New algorithms are added and algorithms are updated.
The Algorithm Register (algoritmes.overheid.nl) is being developed with open source software. The source code can be viewed here on GitHub. It can be downloaded and reused. Github is a platform with transparent version control, where technology in development can be easily shared.

## Motivation

The government increasingly works digitally and uses more and more algorithms when doing so. The government wants to work towards transparent and responsible use of these algorithms. Therefore, the government is making information about the algorithms used by the government available to everyone: citizens, their representatives, the media and (government) professionals.
See the Frequently Asked Questions on the Algorithm Register for more information.

### Open source software

Will you join us and add your thoughts? To contribute, create an account on GitHub (https://github.com/signup ) and read this readme and the code of conduct to get started.
Once signed-up, you can provide feedback on the code of this website, on the algorithm 'standard', on the published description or on the user-friendliness of the website, etc.
Get started: join us and add your thoughts!

# Technical information

In order to run the application locally, the following tooling is required:

- Docker. ([installation instructions](https://docs.docker.com/get-docker/))
- Node.js. The version is specified in `frontend/.nvmrc`. It is recommended to use use [Node version manager](https://github.com/nvm-sh/nvm), the correct Node version can then be activated with with `nvm use`.
- Python. The version is specified in `backend/.python-version`. It is recommended to use [pyenv](https://github.com/pyenv/pyenv) to switch between Python versions, but this is not mandatory.
- Poetry. See the [docs](https://python-poetry.org/docs/#installation) for installation instructions.

## Running the app locally

The documentation below is tested on Ubuntu, but it should work on Windows as well.

### Environment variables

Environment variables are stored in `.env` in the frontend and backend, but because they can contain secrets (passwords), it is not in the repository. Therefore, copy and paste `.env.dummy` to `.env`.

### Database

Start database.

1. Ensure that docker is running
2. Run from `/backend` folder: `docker compose up -d`.

Validate the backend is running by navigating to the GUI (DBgate) on `http://localhost:8002`. There you should be able to open the database `algreg_db`.
The database can be populated using the ETL. Validate the ETL service is running by navigating to the ETL GUI on `http://localhost:8001`. Click on `Synchroniseer` to start the synchronization process.

### Backend

All commands below should be run from the `/backend` directory.

2. Specify Python version to use for virtual environment: `poetry env use <python_version>`. (The required Python version is specified in `backend/.python-version`.)
3. Install packages: `poetry install`.
4. Run database migrations: `poetry run alembic upgrade head`.
5. Start backend: `poetry run uvicorn app.main:app --reload`

Validate the backend is running by navigating to the documentation on `http://localhost:8000/api-docs`.

### Frontend

1.  Install dependencies. Run from '`/frontend`: `npm install`.
2.  Start local server. Run from '`/frontend`: `npm run dev -- --port 3000`.

Validate the frontend is running by navigating to `http://localhost:3000`.

There is also a second frontend: 'frontend-beheer' (management frontend). This frontend is used to manage the algorithms. To run it, follow these steps:

1. Install dependencies. Run from '`/frontend-beheer`: `npm install`.
2. Start local server. Run from '`/frontend-beheer`: `npm run dev -- --port 3001`.

Validate that frontend-beheer is running by navigating to `http://localhost:3001`.

### Linting

This project uses Volar. Install Volar in Visual Studio Code and enable [take over mode](https://github.com/johnsoncodehk/volar/discussions/471) to prevent unnecessary tslint errors:

1. Run Extensions: Show Built-in Extensions command
2. Update Volar to latest version.
3. Run Extensions: Show Built-in Extensions command
4. Find TypeScript and JavaScript Language Features, right click and select Disable (Workspace)
5. Reload VSCode.

Note:
Vue linting config inspired by a repository on [Github](https://github.com/weicheng2138/nuxt3-eslint-starter).

### Versioning

This register allows use of multiple versions of the metadatastandard. To add a new version (`v0_x_x`), follow these steps:

1. in `/backend/app/schemas/config`, you see the metadatastandard in JSON format. Create a new file with your file version name, e.g. `v0_x_x.json`. Change the standard as you see fit.
2. in `/backend/app/routers`, duplicate one of the version folders. Rename it the same as your version in step 1, e.g. `v0_x_x`. Do not change the content.
3. add the name of this file in the \_\_init\_\_.py file in the same folder, e.g. `from . import v0_1, v0_x_x  # noqa`.
4. If your new schema involves changes to the database (notably for new columns) you'll have to do a SQLAlchemy model change (in `/backend/app/models/algoritme_version.py`) as well as a database migration.
5. The frontend needs a configuration file in `backend/app/config/layouts` named similar to the other files, e.g. `v0_x_x.json`. The configuration file defines how the data should be displayed in the tabs.

### Icons

Icons library can be found at `https://icones.js.org/`.
