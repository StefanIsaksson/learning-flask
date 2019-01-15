# REST-API using Flask, Pandas and SQLite

## API

|Service                          |Type  |Description                                             |
|---------------------------------|------|--------------------------------------------------------
|/generations/                    |GET   |Lists pokemon generations                               |
|/generations/<generation_number> |GET   |List of pokemons for given generation                   |
|/pokemons/<pokedex_number>       |GET   |Pokemon information, e.g. attack and defense            |
|/pokemons_stat/<pokedex_number>  |GET   |Pokemon information with extra stats, e.g ranking       |
|/pokemons/                       |GET   |List of all pokemons                                    |
|/pokemons/                       |POST  |Adds a pokemon                                          |
|/pokemons/<pokedex_number>       |DELETE|Deletes a pokemon                                       |
|/pokemons/<pokedex_number>       |PUT   |Updates a pokemon                                       |

## Requires Flask and Pandas
`pip install Flask`

`pip install Pandas`

`pip install flask-cors`