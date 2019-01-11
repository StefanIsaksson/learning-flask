from flask import Flask, jsonify, request, Response
import sqlite3
import pandas as pd
import json

app = Flask(__name__)


def get_db_connection():
    return sqlite3.connect("pokemons.db")


@app.route('/generations/')
def get_generations():
    df = pd.read_sql_query("select generation, count(name) number_of_pokemons from pokemons group by generation;",
                           con=get_db_connection())
    return df.to_json(orient='records')


@app.route('/generations/<int:generation>')
def get_pokemons_by_generation(generation):
    df = pd.read_sql_query("select pokedex_number, name from pokemons where generation=?;",
                           params=[(generation)],
                           con=get_db_connection())
    return df.to_json(orient='records')


@app.route('/pokemons/<int:pokedex_number>', methods=['GET'])
def get_pokemon_by_pokedex_number(pokedex_number):
    print(pokedex_number)
    df = pd.read_sql_query("select pokedex_number, name, generation, type1, type2, is_legendary, "
                           "hp, attack, defense, sp_attack, sp_defense, speed from pokemons where pokedex_number = ?;",
                           params={pokedex_number},
                           index_col='pokedex_number',
                           con=get_db_connection())
    return df.to_json(orient='records')


def valid_pokemon(pokemon):
    if "pokedex_number" in pokemon and "name" in pokemon \
            and "generation" in pokemon and "type1" in pokemon\
            and "type2" in pokemon and "is_legendary" in pokemon:
        return True
    else:
        return False


@app.route('/pokemons/', methods=['POST'])
def add_pokemon():
    request_data = request.get_json()
    if valid_pokemon(request_data):
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('''INSERT INTO pokemons(name, pokedex_number, generation, type1, type2, is_legendary)
                          VALUES(?,?,?,?,?,?)''',
                       (request_data['name'],
                        request_data['pokedex_number'],
                        request_data['generation'],
                        request_data['type1'],
                        request_data['type2'],
                        request_data['is_legendary']))
        db.commit()
        response = Response("",status=201, mimetype='application/json')
        return response
    else:
        error_msg = {
            "error" : "Invalid pokemon passed in request",
            "helpString" : "Data passed should look similar to this: "
                           "{'name':'Bulbasaur','generation':1,'type1':'grass','type2':'poison',"
                           "'is_legendary':0,'hp':45,'attack':49,'defense':49,'sp_attack':65,"
                           "'sp_defense':65,'speed':45}"
        }
        response = Response(json.dumps(error_msg), status=400, mimetype='application/json')
        return response


if __name__ == "__main__":
    app.run(debug=True)
