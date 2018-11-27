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
    for hero in marvel.find():
        output.append({'name': hero['name'], 'height': hero['height'], 'weight': hero['weight'],
                       'universe': hero['universe'], 'other_aliases': hero['other_aliases'],
                       'education': hero['education'], 'identity': hero['identity']})
    return jsonify({'result': output})


@app.route('/character/<name>', methods=['GET'])
def get_one_hero(name):
    marvel = mongo.db.marvel
    hero = marvel.find_one({'name': name})
    if hero:
        output = {'name': hero['name'], 'height': hero['height'], 'weight': hero['weight'],
                  'universe': hero['universe'], 'other_aliases': hero['other_aliases'],
                  'education': hero['education'], 'identity': hero['identity']}
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
        height = request.json['height']
        weight = request.json['weight']
        universe = request.json['universe']
        other_aliases = request.json['other_aliases']
        education = request.json['education']
        identity = request.json['identity']
        hero_id = marvel.insert({'name': name, 'height': height, 'weight': weight, 'universe': universe,
                                 'other_aliases': other_aliases, 'education': education, 'identity': identity})
        new_hero = marvel.find_one({'_id': hero_id})
        output = {'name': new_hero['name'], 'height': new_hero['height'], 'weight': new_hero['weight'],
                  'universe': new_hero['universe'], 'other_aliases': new_hero['other_aliases'],
                  'education': new_hero['education'], 'identity': new_hero['identity']}
    return jsonify({'result': output})


@app.route('/character/<name>', methods=['PUT'])
def edit_hero(name):
    marvel = mongo.db.marvel
    hero_id = marvel.find_one({'name': name})['_id']
    if hero_id:
        name = request.json['name']
        height = request.json['height']
        weight = request.json['weight']
        universe = request.json['universe']
        other_aliases = request.json['other_aliases']
        education = request.json['education']
        identity = request.json['identity']
        marvel.update_one({'name': name}, {'$set': {'height': height, 'weight': weight, 'universe': universe,
                           'other_aliases': other_aliases, 'education': education, 'identity': identity}})
        new_hero = marvel.find_one({'_id': hero_id})
        output = {'name': new_hero['name'], 'height': new_hero['height'], 'weight': new_hero['weight'],
                  'universe': new_hero['universe'], 'other_aliases': new_hero['other_aliases'],
                  'education': new_hero['education'], 'identity': new_hero['identity']}
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
