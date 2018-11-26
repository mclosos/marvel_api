from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'db'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/db'

mongo = PyMongo(app)


@app.route('/characters', methods=['GET'])
def get_all_heroes():
    marvel = mongo.db.marvel
    output = []
    for s in marvel.find():
        output.append({'name': s['name'], 'position': s['position'], 'universe': s['universe']})
    return jsonify({'result': output})


@app.route('/character/<name>', methods=['GET'])
def get_one_hero(name):
    marvel = mongo.db.marvel
    s = marvel.find_one({'name': name})
    if s:
        output = {'name': s['name'], 'position': s['position'], 'universe': s['universe']}
    else:
        output = "No such name"
    return jsonify({'result': output})


@app.route('/character', methods=['POST'])
def add_hero():
    marvel = mongo.db.marvel
    name = request.json['name']
    hero = marvel.find_one({'name': name})
    if hero:
        output = f"{name} is already exists"
    else:
        position = request.json['position']
        universe = request.json['universe']
        hero_id = marvel.insert({'name': name, 'position': position, 'universe': universe})
        new_hero = marvel.find_one({'_id': hero_id})
        output = {'name': new_hero['name'], 'position': new_hero['position'], 'universe': new_hero['universe']}
    return jsonify({'result': output})


@app.route('/character/<name>', methods=['PUT'])
def edit_hero(name):
    marvel = mongo.db.marvel
    hero_id = marvel.find_one({'name': name})['_id']
    if hero_id:
        name = request.json['name']
        position = request.json['position']
        universe = request.json['universe']
        marvel.update_one({'name': name}, {'$set': {'position': position, 'universe': universe}})
        new_hero = marvel.find_one({'_id': hero_id})
        output = {'name': new_hero['name'], 'position': new_hero['position'], 'universe': new_hero['universe']}
    else:
        output = "No such name"
    return jsonify({'result': [output]})


@app.route('/character/<name>', methods=['DELETE'])
def delete_hero(name):
    marvel = mongo.db.marvel
    hero = marvel.find_one({'name': name})
    if hero:
        marvel.delete_one({'name': name})
        output = f"{hero['_id']} is deleted"
    else:
        output = "No such name"
    return jsonify({'result': [output]})


if __name__ == '__main__':
    app.run(debug=True)
