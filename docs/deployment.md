Development
===========

### Install requirements
```bash
~# pip install -r requirements/dev.txt
```

### Run Django
```bash
~# python manage.py runserver --settings=backend.settings.dev
```

### Run Celery in debug mode
```bash
~# celery -A backend worker -l info -E
```

### SuperUser
```
user: nora
password: nora
```
