from flask import Flask
import sqlite3
import pandas as pd

app = Flask(__name__)


def get_db_connection():
    return sqlite3.connect("pokemons.db")


@app.route('/generations')
def get_generations():
    df = pd.read_sql_query("select generation, count(name) number_of_pokemons from pokemons group by generation;",
                           index_col='generation',
                           con=get_db_connection())
    return df.to_json(orient='table')


@app.route('/generations/<int:generation>')
def get_pokemons_by_generation(generation):
    df = pd.read_sql_query("select pokedex_number, name from pokemons where generation=?;",
                           params=[(generation)],
                           index_col='pokedex_number',
                           con=get_db_connection())
    return df.to_json(orient='table')


@app.route('/pokemons/<int:pokedex_number>')
def get_pokemon_by_pokedex_number(pokedex_number):
    print(pokedex_number)
    df = pd.read_sql_query("select pokedex_number, name, type1, type2 from pokemons where pokedex_number = ?;",
                           params={pokedex_number},
                           index_col='pokedex_number',
                           con=get_db_connection())
    return df.to_json(orient='table')


if __name__ == "__main__":
    app.run(debug=True)
