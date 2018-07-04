import json


class Listino:

    def __init__(self):
        self.listino_prezzi = {}
        self.listino_ingredienti = {}

        with open('listino.json', 'r') as listino_json:
            self.listino_prezzi = json.load(listino_json)

        with open('ingredienti.json', 'r') as ingredienti_json:
            self.listino_ingredienti = json.load(ingredienti_json)

    def get_listino(self):
        return self.listino_prezzi

    def get_price(self, pizza_name):
        if pizza_name in self.listino_prezzi.keys():
            return self.listino_prezzi[pizza_name]
        else:
            return '?.??'

    def get_ingrediente(self, pizza_name):
        if pizza_name in self.listino_ingredienti.keys():
            return self.listino_ingredienti[pizza_name]
        else:
            return ''
