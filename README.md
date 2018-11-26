##API. Тестового задание для тестировщиков в ivi
 
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

>GET /character

>GET /characters

>POST /character

>PUT /character

>DELETE /character