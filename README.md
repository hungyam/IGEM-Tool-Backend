### APIs
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