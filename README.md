# To run the api

```bash
# for local
    python api/main.py
# or for production:
gunicorn "api.main:app"
```

API URL: http://localhost:8080

Shut down server with CTRL+C

## Running tests

```bash
# Terminal 1
python api/test.py
# Terminal 2
pytest tests
```

# TODO LIST

1. Move all route login's to api/routes folder
   - auth (done)
   - decks (done)
   - cards
   - users (done)
2. Get rid of /public endpoints and organize endpoints better:
3. Remove Exercises completely (from DB and from files) (done)
4. Logging
   - Replace all print() statements with log.error() and log.debug() (done)
5. Exception handling (done)
6. Documentation
7. When done export & Store Insomnia file in the repo
8. Configure github actions to run tests

## Endpoint List (convert to documentation)

Auth and User: (done)

- POST /login -- to authenticate with email/password
- GET /me -- returns logged in user (needs auth)

  - rm GET /users
  - GET /users/<id>
  - PATCH /users/<id>
  - no need for DELETE /users/<id>

Decks: (done)

- GET /decks (supports query parameter ?user_id=abc)
- GET /decks/<id>
- PATCH /decks/<id>
- DELETE /decks/<id>

Cards:

- GET /cards (supports query parameter ?deck_id=abc&user_id=5)
- GET /cards/<id>
- PATCH /cards/<id>
- DELETE /cards/<id>

## Refactoring & Code Cleanup

- Refactor `BaseModel.parse_obj()` to more sensible approach where possible:
  - `user = User(**payload)`
- Practice on debug route
  - Grab query param (?something=cool&another=100) and cast "another" to int
  - Grab body (needs POST endpoint)
  - Grab URL params (/user/<cool>)
