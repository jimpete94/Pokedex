#!/usr/bin/python3

import pandas as pd
from time import sleep

pokelist = pd.read_csv('./pokemon.csv')





def fetch_poke(query):
    """queries the pandas dataframe using name, returns a series with data"""
    try:
        if type(query) == int:
            return pokelist.query('id == "{}"'.format(query)).values[0]
        else:
            return pokelist.query('species == "{}"'.format(query)).values[0]
    except (IndexError, ValueError):
        print("I'm sorry, I cannot find that Pokémon.")
        return [0]

def main():

    id = 0
    choice = 1

    print("Welcome to PokéText, the text based Pokédex!")

    while choice != '0':
        print("""
                1 - Search PokéText
                2 - Previous Pokémon
                3 - Next Pokémon
                0 - Exit PokéText
                """)

        choice = input("\n\tChoice: ")

        if choice == '1':
            q = input("\n\t Search by Name or ID: ").lower()
            pokemon = fetch_poke(q)
            id = pokemon[0]
        elif choice == '2':
            pokemon = fetch_poke(id-1)
            id = pokemon[0]
        elif choice == '3':
            pokemon = fetch_poke(id+1)
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
