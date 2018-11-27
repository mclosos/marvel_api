## API. Домашнее задание для тестировщиков в ivi
 
### Как развернуть

Необходим python 3.6

Установить пакеты

```bash
$ pip install -r requirements.txt
```

Установить MongoDB

```bash
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
$ echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org
```

Запускать и останавливать MongoDB так:
 
 ```bash
$ sudo service mongodb start
```

```bash
$ sudo service mongodb stop
```

Запускать демон mongod так:

```bash
$ sudo mkdir -p /data/db
$ sudo chmod -R 755 /data/db
```

```bash
$ sudo mongod start
```

### Команды API

>GET /characters

```bash
curl 'http://127.0.0.1:5000/characters'
```

```json
{
  "result": [
    {
      "education": "High school (unfinished)", 
      "height": 1.9, 
      "identity": "Publicly known", 
      "name": "Hawkeye", 
      "other_aliases": "None", 
      "universe": "Marvel Universe", 
      "weight": 104
    }, 
    {
      "education": "Unrevealed", 
      "height": 1.82, 
      "identity": "Secret", 
      "name": "Abyss", 
      "other_aliases": "None", 
      "universe": "Marvel Universe", 
      "weight": 73
    }
  ]
}

```

>GET /character

```bash
curl 'http://127.0.0.1:5000/character/Abyss'
```

```json
{
  "result": {
    "education": "Unrevealed", 
    "height": 1.82, 
    "identity": "Secret", 
    "name": "Abyss", 
    "other_aliases": "None", 
    "universe": "Marvel Universe", 
    "weight": 73
  }
}
```

>POST /character

```bash
 curl -X POST -H 'Content-type: application/json' 
      -d '{"name": "Hawkeye", "universe": "Marvel Universe", 
           "education": "High school (unfinished)", "weight": 104, 
           "height": 1.90, "identity": "Publicly known", 
           "other_aliases": "None"}' 
           'http://127.0.0.1:5000/character' 
```
```json
{
  "result": {
    "education": "High school (unfinished)", 
    "height": 1.9, 
    "identity": "Publicly known", 
    "name": "Hawkeye", 
    "other_aliases": "None", 
    "universe": "Marvel Universe", 
    "weight": 104
  }
}
```


>PUT /character

```bash
curl -X PUT -H 'Content-type: application/json' 
     -d '{"name": "Hawkeye", "universe": "Marvel Universe", 
          "education": "High School (unfinished)", "weight": 104, 
          "height": 1.90, "identity": "Publicly known", 
          "other_aliases": "None"}' 
          'http://127.0.0.1:5000/character/Hawkeye'
```

```json
{
  "result": [
    {
      "education": "High School (unfinished)", 
      "height": 1.9, 
      "identity": "Publicly known", 
      "name": "Hawkeye", 
      "other_aliases": "None", 
      "universe": "Marvel Universe", 
      "weight": 104
    }
  ]
}
```

>DELETE /character

```bash
curl -X DELETE 'http://127.0.0.1:5000/character/Abyss'
```

```json
{
  "result": [
    "5bfd2e3fa259e86dc34f29d9 is deleted"
  ]
}
```

>Если по name невозможно найти коллекцию, то отдается стандартный ответ

```bash
curl -X DELETE 'http://127.0.0.1:5000/character/Vovan'
```

```json
{
  "result": [
    "No such name"
  ]
}
```