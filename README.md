# Nora Foods

_System to manage Mrs. Nora's meal orders_

### Requeriments 📋

_To install the system you need:_

```
Redis
Apache
Python
Celery
```

### Install 🔧

_First, clone the proyect..._

```
$git clone 'https://github.com/sebaveraastudillo/nora-foods.git'
```

_Then, update the settings of project_

```
SLACK_TOKEN='your-token'
SLACK_CHANNEL='your-channel'
```

_Then, make migrations of the system_

```
$python manage.py makemigrations
$python manage.py migrate
```

_Then, create the super user (staff user) to nora_

```
$python manage.py createsuperuser
```

_Start service redis_

```
$sudo service redis start
```

_Check service redis_

```
$sudo service redis status
```

_Run server and the celery service_

```
$python manage runserver 8080
```

_In other terminal_

```
$celery worker -A nora.celery --loglevel=info
```

## Execute the unit test ⚙️

_Execute the unit test of the system_

```
$python manage test menu
```

## Author ✒️

* **Sebastian Vera** - *Develop System* - [sebastianveraastudillo](https://github.com/sebastianveraastudillo)

---
⌨️ con ❤️ por [sebastianveraastudillo](https://github.com/sebastianveraastudillo) 😊