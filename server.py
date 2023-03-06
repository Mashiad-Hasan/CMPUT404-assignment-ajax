#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# You can start this by executing it in python:
# python server.py
#
# remember to:
#     pip install flask


import flask
from flask import Flask, request, jsonify
from flask import redirect, url_for
import json
app = Flask(__name__, static_url_path='/static')
app.debug = True

# An example world
# {
#    'a':{'x':1, 'y':2},
#    'b':{'x':2, 'y':3}
# }

class World:
    def __init__(self):
        self.clear()
        
    def update(self, entity, key, value):
        entry = self.space.get(entity,dict())
        entry[key] = value
        self.space[entity] = entry

    def set(self, entity, data):
        self.space[entity] = data

    def clear(self):
        self.space = dict()

    def get(self, entity):
        return self.space.get(entity,dict())
    
    def world(self):
        return self.space

# you can test your webservice from the commandline
# curl -v   -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/entity/X -d '{"x":1,"y":1}' 

myWorld = World()          

# I give this to you, this is how you get the raw body/data portion of a post in flask
# this should come with flask but whatever, it's not my project.
def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data.decode("utf8") != u''):
        return json.loads(request.data.decode("utf8"))
    else:
        return json.loads(request.form.keys()[0])

@app.route("/")
def hello():
    '''Return something coherent here.. perhaps redirect to /static/index.html '''
    return redirect(url_for('static', filename='index.html'))

# @app.route("/entity/<entity>", methods=['POST','PUT'])
# def update(entity):
#     '''update the entities via this interface'''
    
#     if request.method == 'PUT' or request.method == 'POST':
#         data = request.get_json()
#         myWorld.set(entity, data)
#         return jsonify(data), 200
#     else:
#         return "Method not allowed", 405
# @app.route("/entity/<entity>", methods=['POST','PUT'])
# def update_entities():
#     '''update the entities via this interface'''
    
#     if request.method == 'POST' or request.method == 'PUT' :
#         data = request.get_json()
#         for entity, value in data.items():
#             myWorld.set(entity, value)
#         return jsonify(data), 200
#     else:
#         return "Method not allowed", 405

@app.route("/entity/<entity>", methods=['POST','PUT'])
def update_entities(entity=None):
    '''update the entities via this interface'''
    if request.method == 'POST' or request.method == 'PUT':
        data = request.get_json()
        if entity:
            myWorld.set(entity, data)
            return jsonify(data), 200
        else:
            for entity, value in data.items():
                myWorld.set(entity, value)
            return jsonify(data), 200
    else:
        return "Method not allowed", 405


@app.route("/world", methods=['POST','GET'])    
def world():
    '''you should probably return the world here'''
    if request.method == 'GET' or request.method == 'POST':
        return jsonify(myWorld.world())
    else:
        return "Method not allowed", 405

@app.route("/entity/<entity>")    
def get_entity(entity):
    '''This is the GET version of the entity interface, return a representation of the entity'''
    
    data = myWorld.get(entity)
    # if data:
    #     return jsonify(data), 200
    # else:
    #     return "Entity not found", 404
    return jsonify(data)

@app.route("/clear", methods=['POST','GET'])
def clear():
    '''Clear the world out!'''
    if request.method == 'GET' or request.method == 'POST':
        myWorld.clear()
        return jsonify({})
    else:
        return "Method not allowed", 405

if __name__ == "__main__":
    app.run()
