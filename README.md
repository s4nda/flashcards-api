# To run the api

```bash
flask --app api/main run --reload --port 8080
```

API URL: http://localhost:8080

Shut down server with CTRL+C


# jwt - json web tokens
>import jwt
>dve built in funkcije: 
    - .encode()
    - .decode()
> my_token = jwt.encode({"payload":"payload"}, "secretkey")
>jwt.decode(my_token,"secretkey")