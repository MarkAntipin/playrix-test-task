# Playrix test task; migrate data from google sheets to gridly service

## Run script
### Do not forget to put your token.json (google sheets token) file in the root of the project!

### Without Docker
**Dependencies:**

- python3.12
- poetry (https://python-poetry.org)


**Create .env file with: (look at [.env.example](.env.example))**
```
GOOGLE_SHEETS_SPREADSHEET_ID=
GOOGLE_SHEETS_TOKEN_FILE_NAME=

GRIDLY_API_KEY=
GRIDLY_DB_ID=
```

**Install libs:**
```
poetry install
```

**Run**
```
poetry run python run.py 
```
You can look throw logs in console output and check if everything is ok

### With Docker
Build image:
```
docker build --no-cache -t playrix-test-task .
```

Change in docker-compose.yml env vars and:
```
docker run --env-file .env playrix-test-task
```


## Development

### Guide through the code
- [run.py](run.py) - script entry point
- [repositories](src%2Frepositories) - data access layer
- [services](src%2Fservices) - business logic layer
- [app.py](src%2Fapp.py) - main app class to run
- [utils](src%2Futils) - helper functions for logging, http requests and etc.


### Linter:
```
poetry run ruff check . --fix
```

### Unit Tests:
```
pytest -v tests
```
