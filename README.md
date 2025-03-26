## Guia de comandos

```sh
python -m venv .venv
```
**Windows**
```ps1
.venv\Scripts\activate
```
**Linux**
```sh
. .venv/bin/activate
```

```sh
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

