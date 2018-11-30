## API. Домашнее задание для тестировщиков в ivi
 
### Как развернуть

Необходим python 3.6

Установить пакеты

```bash
$ pip install -r requirements.txt
```

Установить MongoDB и запустить mongo

https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

### Дамп базы

База (а точнее коллекция _db.marvel_) наполняется скриптом _stan.py_. 
Скрипт берет список персонажей из API Marvel, 
скрапит информацию по ним в wiki Marvel, 
после чего записывает данные в MongoDB. 
Количество записей передается скрипту в виде числа. 

```bash
python stan.py 300
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
curl 'http://localhost:5000/character/Abyss'
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
           'http://localhost:5000/character' 
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
          'http://localhost:5000/character/Hawkeye'
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
curl -X DELETE 'http://localhost:5000/character/Abyss'
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
curl -X DELETE 'http://localhost:5000/character/Vovan'
```

```json
{
  "result": [
    "No such name"
  ]
}
```
