#!/usr/bin/python3

import guizero
import pandas as pd

from tkinter import *
from PIL import Image, ImageTk



class App(Frame):
    """Basic tk app that will contain our pokedex"""

    def __init__(self, master):
        super(App, self).__init__(master)
        self._data = pd.read_csv("./pokemon.csv").fillna(" ")
        self._pokeID = 0
        # Dict of Regions, mapped to values in dataframe
        self._region_map = {1: 'Kanto', 2: 'Johto', 3: 'Hoenn',
                            4: 'Sinnoh', 5: 'Unova', 6: 'Kalos', 7: 'Alola'}
        self._image_path = './images/'
        self._welcome_img =self.load_image('pokemon_logo.jpg')
        # PIL requires to keep a record of object
        # use `.paste()` method to replace image
        self._img = ImageTk.PhotoImage(self._welcome_img)
        self.grid()
        self.create_widgets()
        #self._image.paste(self._welcome_img, bbox=None)
        self._im = self.canvas.create_image(0,0, image=self._img, anchor='nw')

    def create_widgets(self):
        """ Creates all internal aspects of the app"""

        # Welcome label
        Label(self, text = "Welcome to the Pokédex!").grid(row = 0, column = 0,
        columnspan = 2, sticky = W)

        # Create canvas for displaying pokemon images
        self.canvas = Canvas(self, width = 500, height = 300)
        self.canvas.grid(row = 1, column = 0,
        columnspan = 5, sticky = W)

        # Create a search box for users to search through the Pokédex
        Label(self, text = "Search:").grid(row = 2, column = 0, sticky = W)
        self.search_ent = Entry(self)
        self.search_ent.grid(row = 2, column = 1, sticky = W)

        Button(self, text = "Go!",
        command = self.search_poke).grid(row = 2, column = 2, sticky = W)

        # Create output boxes that display the Pokémon's data
        Label(self, text = "ID:").grid(row = 3, column = 0, sticky = W)
        self.id_disp = Text(self, width = 20, height = 2, wrap = WORD)
        self.id_disp.grid(row = 3, column = 1, sticky = W)

        Label(self, text = "Name:").grid(row = 3, column = 2, sticky = W)
        self.name_disp = Text(self, width = 20, height = 2, wrap = WORD)
        self.name_disp.grid(row = 3, column = 3, sticky = W)

        Label(self, text = "Region:").grid(row = 4, column = 0, sticky = W)
        self.region_disp = Text(self, width = 20, height = 2, wrap = WORD)
        self.region_disp.grid(row = 4, column = 1, sticky = W)

        Label(self, text = "Pri Type:").grid(row = 5, column = 0, sticky = W)
        self.pritype_disp = Text(self, width = 20, height = 2, wrap = WORD)
        self.pritype_disp.grid(row = 5, column = 1, sticky = W)

        Label(self, text = "Sec Type:").grid(row = 5, column = 2, sticky = W)
        self.sectype_disp = Text(self, width = 20, height = 2, wrap = WORD)
        self.sectype_disp.grid(row = 5, column = 3, sticky = W)

        # Create navigation buttons to go forward and backward through Pokédex
        Button(self, text = "Prev",
        command = self.prev_poke).grid(row = 6, column = 1, sticky = W)

        Button(self, text = "Next",
        command = self.next_poke).grid(row = 6, column = 2, stick = W)

    def fetch_id(self, query):
        """queries the pandas dataframe using ID, returns a series with data"""
        # Search between max and min values of pokedex, allows for future expansion
        if self._data.id.min() <= query <= self._data.id.max():
            return self._data.query('id == "{}"'.format(query)).values[0]
        else:
            message = 'ID number does not exist'
            return [0, message]

    def fetch_name(self, query):
        """queries the pandas dataframe by name, returns a series with data"""
        try:    # Search for name, partial or otherwise
            # Get series with true or false values
            search_res = self._data.species.str.contains(query.lower())
            # Isolate the true values and convert index to ID
            poss_res = search_res[(search_res == True)].index +1
            if len(poss_res) > 0:
                return self.fetch_id(poss_res[0])
            else:
                message = 'Pokemon not found'
                return [0, message]
        except TypeError:   # Give up looking
            message = 'Pokemon not found'
            return [0, message]

    def load_image(self, image):
        """Use PIL to load an image that Tk will use."""
        try:    # Use name from dataframe to look for image
            image_file = self._image_path+image
            img = Image.open(image_file)
            img.resize((500, 300))
            return img
        except FileNotFoundError:   # If not found, just show pokemon logo
            return self._welcome_img

    def search_poke(self):
        """Passes value of search_ent to fetch_poke() to perform search"""
        query = self.search_ent.get()
        try:    # Convert string to number, if able
            query = int(query)
            print("Searching by ID")
            pokemon = self.fetch_id(query)
        except ValueError:
            print("Searching by name, not ID")
            pokemon = self.fetch_name(query)
        self._pokeID = pokemon[0]
        self.update(pokemon)

    def prev_poke(self):
        """ Passes current _pokeID-1 to fetch_poke to retrieve previous data"""
        pokemon = self.fetch_id(self._pokeID - 1)
        self._pokeID = pokemon[0]
        self.update(pokemon)

    def next_poke(self):
        """ Passes current _pokeID+1 to fetch_poke to retrieve next data"""
        pokemon = self.fetch_id(self._pokeID + 1)
        self._pokeID = pokemon[0]
        self.update(pokemon)

    def update(self, data):
        """Updates the GUI with new information."""

        # Clear all text boxes
        self.id_disp.delete(0.0, END)
        self.name_disp.delete(0.0, END)
        self.region_disp.delete(0.0, END)
        self.pritype_disp.delete(0.0, END)
        self.sectype_disp.delete(0.0, END)

        # If Pokémon is found, show data
        if int(self._pokeID) != 0:
            self.id_disp.insert(0.0, data[0])
            self.name_disp.insert(0.0, data[1].title())
            self.region_disp.insert(0.0, self._region_map[data[2]])
            self.pritype_disp.insert(0.0, data[6].capitalize())
            self.sectype_disp.insert(0.0, data[7].capitalize())
            img = self.load_image(data[1]+'.jpg')
            self._img.paste(img)

        # If not, display message
        else:
            self.name_disp.insert(0.0, data[1])
            self._img.paste(self._welcome_img)

def main():
    root = Tk()
    root.title("Pokédex")
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()
