# pipenv

- pipenv run pip freeze > requirements.txt
- pipenv install *--package_name--*

# docker

```bash
docker-compose up --build # prod
docker compose -f "local-docker-compose.yml" up -d --build # local
```

# pylint commands

```bash 
pylint --generate-rcfile > .pylintrc
```

# ngrok
```bash
ngrok http --host-header=rewrite 5000
ngrok http 8000 --basic-auth 'ngrok:issecure'
```
+ Add Header to frontend 
    ```
    "ngrok-skip-browser-warning": true
    ```