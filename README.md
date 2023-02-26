# To run the api

```bash
flask --app api/main run --reload --port 8080

gunicorn "api.main:app"
```

API URL: http://localhost:8080

Shut down server with CTRL+C
