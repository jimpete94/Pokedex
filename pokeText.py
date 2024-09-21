#!/usr/bin/python3

import pandas as pd
from time import sleep

pokelist = pd.read_csv('./pokemon.csv').fillna(" ")


'''
def fetch_poke(query):
    """queries the pandas dataframe using name, returns a series with data"""
    try:
        if type(int(query)) == int:
            query = int(query)
            return pokelist.query('id == @query').values[0]
        else:
            return pokelist.query("species == @query").values[0]
    except (IndexError, ValueError):
        print("I'm sorry, I cannot find that Pokémon.")
        return [0]
'''

def process_search(query):
    # Determine if search value is int or str
    try:
        query = int(query)
        return fetch_id(query)
    except ValueError:
        return fetch_name(query)

def fetch_name(query):
    """queries the pandas dataframe by name, returns a PokeID"""
    try:    
        # Search for name, partial or otherwise
        # Get series with true or false values dependant on the presence of the query in the dataframe
        search_res = pokelist.species.str.contains(query.lower())
        # Isolate the true values and convert to ID
        poss_res = search_res[(search_res == True)].index +1
        if len(poss_res) > 0:
            return fetch_id(poss_res[0])
        else:
            print("Pokémon not found")
            return [0]
    except TypeError:   # Give up Looking
        print("Pokémon not found")
        return [0]

def fetch_id(query):
    """queries the pandas dataframe using ID, returns a series with data"""
    # Search between max and min values of pokedex, allows for future expansion
    if pokelist.id.min() <= query <= pokelist.id.max():
        return pokelist.query('id == @query').values[0]
    else:
        print("Pokémon not found")
        return [0]

def main():

    id = 0
    choice = 1

    print("Welcome to PokéText, the text based Pokédex!")

    while choice != '0':
        print("""
                1 - Search Pokédex
                2 - Previous Pokémon
                3 - Next Pokémon
                0 - Exit PokéText
                """)

        choice = input("\n\tChoice: ")

        if choice == '1':
            q = input("\n\t Search by Name or ID: ").lower()
            pokemon = process_search(q)
            id = pokemon[0]
        elif choice == '2':
            pokemon = fetch_id(id-1)
            id = pokemon[0]
        elif choice == '3':
            pokemon = fetch_id(id+1)
            id = pokemon[0]
        elif choice == '0':
            break
        else:
            print("Invalid Option")

        if int(id) > 0:
            print("""
                    ID:\t\t{}
                    Name:\t{}
                    Region:\t{}
                    Pri Type:\t{}
                    Sec Type:\t{}
                    \n
                    """.format(pokemon[0], pokemon[1].capitalize(), pokemon[2],
                    pokemon[6].capitalize(), pokemon[7].capitalize()))
        sleep(5)

        print("\nPlease make another selection.\n")

    print("Thank you for using the PokéText, please come back soon!")
    sleep(5)

if __name__ == '__main__':
    main()
