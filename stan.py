#!/usr/bin/env python3

import re
import sys
from hashlib import md5
from time import time

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

API_URL = "http://gateway.marvel.com/"
CHARACTERS = "/v1/public/characters"
PUBLIC_KEY = "2c73a697cff73f06f44ee35901af4026"
PRIVATE_KEY = "d4755b610eb7604babc8cb3ebaecaf2abb1ea0db"
MONGO_URL = "mongodb://localhost:27017"
OFFSET = 20


def parse_character_page(url):
    result = dict()
    detail_page = BeautifulSoup(requests.get(url).text, "lxml")

    stats = detail_page.find_all(class_="bioheader__stats")
    for s in stats:
        k, v = [i.text for i in s.contents]
        result[k] = v

    bio = detail_page.find_all(class_="bioGroup__Item")
    for b in bio:
        k, v = [i.text for i in b.contents]
        result[k.lower().replace(" ", "_")] = v

    return result


def get_characters_list(offset=0):
    ts = str(time())
    params = dict(
        apikey=PUBLIC_KEY,
        ts=ts,
        hash=md5((ts + PRIVATE_KEY + PUBLIC_KEY).encode()).hexdigest(),
        offset=offset
    )
    response = requests.get(API_URL + CHARACTERS, params=params).json()
    results = response["data"]["results"]

    characters_list = []
    for r in results:
        urls = r["urls"]
        detail_url = next((page["url"] for page in urls if page["type"] == "detail"))
        characters_list.append(dict(name=r["name"], detail_url=detail_url))
    return characters_list


def get_detail(character):
    allowed_params = ["name", "height", "weight", "universe", "other_aliases", "education", "identity"]

    detail = parse_character_page(character["detail_url"])

    # о некоторых героях нет подробной информации на сайте
    if "height" not in detail.keys():
        return None
    if "weight" not in detail.keys():
        return None
    # страници с несколькими героями тоже не интересуют
    if ";" in detail["height"]:
        return None

    height = re.findall(r'\d+', detail["height"])
    if len(height) == 1:
        detail["height"] = int(int(height[0]) * 30.48)
    if len(height) == 2:
        detail["height"] = int(int(height[1]) * 2.54 + int(height[0]) * 30.48)
    else:
        return None
    try:
        weight = re.findall(r'\d+', detail["weight"])[0]
        detail["weight"] = float(weight) * 0.45
    except (IndexError, KeyError):
        print('ALARM!!! ', detail)
        pass
    detail["name"] = character["name"]

    return {k: v for k, v in detail.items() if k in allowed_params}


def get_heroes(n):
    c = 0
    offset = 0
    while c < n:
        for character in get_characters_list(offset=offset):
            hero = get_detail(character)

            if hero:
                c += 1
                yield hero

            if c >= n:
                break

        offset += OFFSET


if __name__ == "__main__":
    if len(sys.argv) < 2:
        n = 10
    else:
        try:
            n = int(sys.argv[1])
        except ValueError:
            sys.exit()

    mongo = MongoClient(MONGO_URL)
    mongo.db.marvel.drop()
    marvel = mongo.db.marvel
    number = 0
    for hero in get_heroes(n):
        if not marvel.find_one({"name": hero["name"]}):
            marvel.insert(hero)
            number += 1
            print(f'{number}.{hero["name"]} added')
