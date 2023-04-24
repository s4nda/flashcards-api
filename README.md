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
