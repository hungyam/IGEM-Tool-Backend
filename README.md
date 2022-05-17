### Base framework
There are fields of (species, system, gene_name, protein_name) now.

Fields and APIs will be added through late requirements
### Setting the database
Edit the file `database_backend/settings.py`
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'resistant_system',
        'USER': 'hungyam',
        'PASSWORD': '******',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```
### Start
run `python manage.py makemigrations`

run `python manage.py sqlmigrate Resistant_System 0001(Latest Version)`

run `python manage.py migrate`

run `python manage.py runserver`
### APIs
#### Reload data from local CSV file --- `GET /reload`

The fields from left to right are (species, system, gene_name, protein_name) `delimiter=' '`

#### Get all data --- `GET /data`

- Response
```json
{
  "code": 200,
  "data": [
    {
      "species": "",
      "system": "",
      "gene": "",
      "protein": ""
    },
    ......
  ]
}
```


#### Get all species --- `GET /species`

- Response

```json
{
  "code": 200,
  "species": [
    "", "", ......
  ]
}
```

#### Get all kinds of resistant system --- `GET /system`

- Response

```json
{
  "code": 200,
  "species": [
    "", "", ......
  ]
}
```


#### Get data by key word --- `POST /data`

- Request

```json
{
  "type": "",
  "keyword": ""
}
```

- Response

```json
{
  "code": 200,
  "data": [
    {
      "species": "",
      "system": "",
      "gene": "",
      "protein": ""
    },
    ......
  ]
}
```