#!/usr/bin/python3

import guizero
import pandas as pd

from tkinter import *
from PIL import ImageTk



class App(Frame):
    """Basic tk app that will contain our pokedex"""

    def __init__(self, master):
        super(App, self).__init__(master)
        self._data = pd.read_csv("./pokemon.csv")
        self._pokeID = IntVar()
        self._pokeID.set(0)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """ Creates all internal aspects of the app"""

        # Welcome label
        Label(self, text = "Welcome to the Pokédex!").grid(row = 0, column = 0,
        columnspan = 2, sticky = W)

        # Create a search box for users to search through the Pokédex
        Label(self, text = "Search:").grid(row = 1, column = 0, sticky = W)
        self.search_ent = Entry(self)
        self.search_ent.grid(row = 1, column = 1, sticky = W)

        Button(self, text = "Go!",
        command = self.search_poke).grid(row = 1, column = 2, sticky = W)

        # Create output boxes that display the Pokémon's data
        Label(self, text = "ID:").grid(row = 2, column = 0, sticky = W)
        self.id_disp = Text(self, wrap = WORD)
        self.id_disp.grid(row = 2, column = 1, sticky = W)

        Label(self, text = "Name:").grid(row = 2, column = 2, sticky = W)
        self.name_disp = Text(self, wrap = WORD)
        self.name_disp.grid(row = 2, column = 3, sticky = W)

        Label(self, text = "Region:").grid(row = 3, column = 0, sticky = W)
        self.region_disp = Text(self, wrap = WORD)
        self.region_disp.grid(row = 3, column = 1, sticky = W)

        Label(self, text = "Pri Type:").grid(row = 4, column = 0, sticky = W)
        self.pritype_disp = Text(self, wrap = WORD)
        self.pritype_disp.grid(row = 4, column = 1, sticky = W)

        Label(self, text = "Sec Type:").grid(row = 4, column = 2, sticky = W)
        self.sectype_disp = Text(self, wrap = WORD)
        self.sectype_disp.grid(row = 4, column = 3, sticky = W)

        # Create navigation buttons to go forward and backward through Pokédex
        Button(self, text = "Prev",
        command = self.prev_poke).grid(row = 5, column = 1, sticky = W)

        Button(self, text = "Next",
        command = self.next_poke).grid(row = 5, column = 2, stick = W)

    def fetch_poke(self, query):
        """queries the pandas dataframe using name, returns a series with data"""
        try:
            if type(query) == int:
                return self._data.query('id == "{}"'.format(query)).values[0]
            else:
                return self._data.query('species == "{}"'.format(query)).values[0]
        except (IndexError, ValueError):
            message = "I'm sorry, I cannot find that Pokémon."
                return [0, message]

    def search_poke(self):
        """Passes value of search_ent to fetch_poke() to perform search"""
        pokemon = self.fetch_poke(self.search_ent)
        self._pokeID = pokemon[0]
        self.update(pokemon)

    def prev_poke(self):
        """ Passes current _pokeID-1 to fetch_poke to retrieve previous data"""
        pokemon = self.fetch_poke(self._pokeID - 1)
        self._pokeID = pokemon[0]
        self.update(pokemon)

    def next_poke(self):
        """ Passes current _pokeID+1 to fetch_poke to retrieve next data"""
        pokemon = self.fetch_poke(self._pokeID + 1)
        self._pokeID = pokemon[0]
        self.update(pokemon)
