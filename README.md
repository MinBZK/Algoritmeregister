# About the Algorithm Register 
The Ministry of the Interior and Kingdom Relations is developing the Algorithm Register. The team does this using an open development style, through open source software. Anyone can view the team’s progress on the GitHub of the Ministry of the Interior and Kingdom Relations. The Algorithm Register is under development. The content changes over time. New algorithms are added and algorithms are updated. 
The Algorithm Register (algoritmes.overheid.nl) is being developed with open source software. The source code can be viewed here on GitHub. It can be downloaded and reused. Github is a platform with transparent version control, where technology in development can be easily shared. 
## Motivation 
The government increasingly works digitally and uses more and more algorithms when doing so. The government wants to work towards transparent and responsible use of these algorithms. Therefore, the government is making information about the algorithms used by the government available to everyone: citizens, their representatives, the media and (government) professionals. 
The goal of the Algorithm Register is formulated in a [parliamentary motion](https://www.tweedekamer.nl/kamerstukken/moties/detail?id=2021Z00984&did=2021D02426) requesting the gouverment to set up a registry that describes what algorithms are used by the gouvernment, for what purpose and what datasets are used to enable everyone to supervise the use of discrominatory and non-discrimatory algorithms. The scope of the registry has been narowed to impactful algorithms with yet to be determined criteria that will be partially based on AI Act criteria.
See the Frequently Asked Questions on the Algorithm Register for more information. 
### Open source software 
Will you join us and add your thoughts? To contribute, create an account on GitHub (https://github.com/signup ) and read this readme and the code of conduct to get started. 
Once signed-up, you can provide feedback on the code of this website, on the algorithm 'standard', on the published description or on the user-friendliness of the website, etc. 
Get started: join us and add your thoughts! 


# Technical information

In order to run the application locally, the following tooling is required:

- Docker ([installation instructions](https://docs.docker.com/get-docker/))
- Node.js. The version is specified in `frontend/.nvmrc`. It is recommended to use use [Node version manager](https://github.com/nvm-sh/nvm), the correct Node version can then be activated with with `nvm use`.
- Python. The version is specified in `backend/.python-version`. It is recommended to use [pyenv](https://github.com/pyenv/pyenv) to switch between Python versions, but this is not mandatory.
- Poetry. See the [docs](https://python-poetry.org/docs/#installation) for installation instructions.

## Running the app locally

The documentation below is tested on Ubuntu, but it should work on Windows as well.

### Environment variables

Environment variables are stored in `.env`, but because they can contain secrets (passwords), it is not in the repository. Therefore, copy and paste `.env.dummy` to `.env`. For local development, no changes are needed.

### Database

1. Start database. Run from root folder: `docker compose up -d`.

Validate the backend is running by navigating to the GUI (DBgate) on `http://localhost:8093`. There you should be able to open the database `algreg_db`.

### Backend

All commnands below should be run from the `/backend` directory.

2. Specify Python version to use for virtual environment: `poetry env use <python_version>`. (The required Python version is specified in `backend/.python-version`.)
3. Install packages: `poetry install`.
4. Run database migrations: `poetry run uvicorn upgrade head`.
5. Start backend: `poetry run uvicorn app.main:app --reload`

Validate the backend is running by navigating to the documentation on `http://localhost:8000/api-docs`.

### Frontend

1.  Install dependencies. Run from '`/frontend`: `npm install`.
2.  Start local server. Run from '`/frontend`: `npm run dev -- -o`.

Validate the frontend is running by navigating to `http://localhost:3000`.

## Run locally

1. Start database from backend. Run from `/backend`: `docker compose up -d`
2. Ensure latest migration has been completed. Run from `/backend`: `poetry run alembic upgrade head`
3. Navigate to `/frontend` and run `npm run dev`.
4. Navigate to `/backend` and run `poetry run uvicorn app.main:app --reload`

## Other

### Linting

This project uses Volar. Install Volar in Visual Studio Code and enable [take over mode](https://github.com/johnsoncodehk/volar/discussions/471) to prevent unnecessary tslint errors:

1. Run Extensions: Show Built-in Extensions command
2. Update Volar to latest version.
3. Run Extensions: Show Built-in Extensions command
4. Find TypeScript and JavaScript Language Features, right click and select Disable (Workspace)
5. Reload VSCode.

Note:
Vue linting config inspired by a repository on [Github](https://github.com/weicheng2138/nuxt3-eslint-starter).

### Icons

Icons library can be found at `https://icones.js.org/`.
