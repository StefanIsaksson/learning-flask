from flask import Flask, jsonify, request, Response, send_from_directory
import sqlite3
import pandas as pd
import json
from flask_cors import CORS


app = Flask(__name__, static_url_path='')
CORS(app)


def get_db_connection():
    return sqlite3.connect("pokemons.db")


@app.route('/generations/')
def get_generations():
    df = pd.read_sql_query("SELECT generation, COUNT(name) number_of_pokemons FROM pokemons GROUP BY generation;",
                           con=get_db_connection())
    if df.empty:
        return Response("", status=404)
    else:
        response_message = df.to_json(orient='records')
        return Response(response_message, status=200, mimetype='application/json')


@app.route('/generations/<int:generation>')
def get_pokemons_by_generation(generation):
    df = pd.read_sql_query("SELECT pokedex_number, name FROM pokemons WHERE generation=?;",
                           params=[(generation)],
                           con=get_db_connection())
    if df.empty:
        return Response("", status=404)
    else:
        response_message = df.to_json(orient='records')
        return Response(response_message, status=200, mimetype='application/json')

@app.route('/pokemons/')
def get_pokemons():
    df = pd.read_sql_query("SELECT pokedex_number, name, generation FROM pokemons;",
                           con=get_db_connection())
    if df.empty:
        return Response("", status=404)
    else:
        response_message = df.to_json(orient='records')
        return Response(response_message, status=200, mimetype='application/json')

@app.route('/pokemons/<int:pokedex_number>', methods=['GET'])
def get_pokemon(pokedex_number):
    df = pd.read_sql_query("SELECT pokedex_number, name, generation, type1, type2, is_legendary, "
                           "hp, attack, defense, sp_attack, sp_defense, speed FROM pokemons WHERE pokedex_number = ?;",
                           params={pokedex_number},
                           con=get_db_connection())
    if df.empty:
        return Response("", status=404)
    else:
        response_message = df.to_json(orient='records')
        return Response(response_message, status=200, mimetype='application/json')

@app.route('/pokemons_stats/<int:pokedex_number>', methods=['GET'])
def get_pokemon_with_extra_stats(pokedex_number):
    df = pd.read_sql_query("SELECT pokedex_number, name, generation, type1, type2, is_legendary, "
                           "hp, attack, defense, sp_attack, sp_defense, speed FROM pokemons;",
                           con=get_db_connection())
    if df.empty:
        return Response("", status=404)
    else:
        df['hp_rank_pct'] = df['hp'].rank(pct=True, ascending=1)
        df['attack_rank_pct'] = df['attack'].rank(pct=True, ascending=1)
        df['defense_rank_pct'] = df['defense'].rank(pct=True, ascending=1)
        df['sp_attack_rank_pct'] = df['sp_attack'].rank(pct=True, ascending=1)
        df['sp_defense_rank_pct'] = df['sp_defense'].rank(pct=True, ascending=1)
        df['speed_rank_pct'] = df['speed'].rank(pct=True, ascending=1)

        df['hp_rank'] = df['hp'].rank(method='first', ascending=False)
        df['attack_rank'] = df['attack'].rank(method='first', ascending=False)
        df['defense_rank'] = df['defense'].rank(method='first', ascending=False)
        df['sp_attack_rank'] = df['sp_attack'].rank(method='first', ascending=False)
        df['sp_defense_rank'] = df['sp_defense'].rank(method='first', ascending=False)
        df['speed_rank'] = df['speed'].rank(method='first', ascending=False)
        df['total_nr_pokemons_ranked'] = df.shape[0]

        df = df[df['pokedex_number'] == pokedex_number]
        response_message = df.to_json(orient='records')
        return Response(response_message, status=200, mimetype='application/json')

@app.route('/pokemons/<int:pokedex_number>', methods=['DELETE'])
def delete_pokemon(pokedex_number):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM pokemons WHERE pokedex_number = ?", (pokedex_number,))
    db.commit()
    result = cursor.rowcount
    if result > 0:
        return Response("", status=204)
    else:
        return Response("", status=404)


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


@app.route('/pokemons/<int:pokedex_number>', methods=['PUT'])
def replace_pokemon(pokedex_number):
    request_data = request.get_json()
    if valid_pokemon(request_data):
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute('''UPDATE pokemons SET name = ? WHERE pokedex_number = ? ''',
                       (request_data['name'], pokedex_number))

        db.commit()
        response = Response("",status=204, mimetype='application/json')
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
    app.run(host='0.0.0.0')
