# REST-API using Flask, Pandas and SQLite

## API

|Service                          |Type  |Description                                             |
|---------------------------------|------|--------------------------------------------------------
|/generations/                    |GET   |Lists pokemon generations                               |
|/generations/<generation_number> |GET   |List of pokemons for given generation                   |
|/pokemons/<pokedex_number>       |GET   |Pokemon information, e.g. attack and defense            |
|/pokemons/                       |POST  |Adds a pokemon                                          |

## Requires Flask and Pandas
`pip install Flask`

`pip install Pandas`