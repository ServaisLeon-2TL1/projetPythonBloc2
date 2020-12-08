import validators
from pyfiglet import Figlet
from bs4 import BeautifulSoup
import mysql.connector
import requests


class Database:
    """
    Exécute différents Query
    :type host: string
    :type user: string
    :type passwd: string
    :type db: string
    :type connector: string
    :type cursor: string
    :type title: string
    :type welcome: string
    :type help: string
    :type header: dict
    :type command: dict
    :return connector: retourne la connexion
    :return cursor: retourne le curseur

    """

    def __init__(self):

        self.__header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.36'}
        self.__title = "Amazon Scrapp"
        self.__welcome = "Bienvenue dans l'Amazon Scrapp !"
        self.__help = "Pour la liste des commandes tapez : ?"
        self.__command = {
            "?": "Affiche toute les commandes",
            "produits": "Liste tout les produits",
            "catégories": "liste les catégories",
            "nouvelle catégorie": "Permet de créer une nouvelle catégories",
            "supprimer catégorie": "Permet de supprimer une catégories",
            "supprimer produit": "Permet de supprimer un produit"
        }

    @staticmethod
    def start():
        try:
            connector = mysql.connector.connect(host="localhost", user="root", passwd="", db="amazon")
            return connector
        except mysql.connector.Error as error:
            print("Impossible de se connecter à la base de données: {}".format(error))

    @staticmethod
    def select_product():
        try:
            conn = BddConnection.start()
            cursor = conn.cursor()
            product = cursor.execute("""SELECT * from produits """)
            rows = cursor.fetchall()
            for row in rows:
                print("Id = ", row[0], )
                print("Nom = ", row[1])
                print("Url = ", row[2])
                print("Catégorie  = ", row[3], "\n"),
        except mysql.connector.Error as error:
            print("Pas de produit : {}".format(error))

    @staticmethod
    def get_cat_name():
        try:
            conn = BddConnection.start()
            cursor = conn.cursor()
            cat = cursor.execute("""SELECT Cat_nom from catégories """)
            rows = cursor.fetchall()
            cat_list = []
            for row in rows:
                cat_list.append(row[0])
            return cat_list
        except mysql.connector.Error as error:
            print("Pas de catégorie : {}".format(error))

    @staticmethod
    def select_categories():
        try:
            conn = BddConnection.start()
            cursor = conn.cursor()
            cat = cursor.execute("""SELECT * from catégories """)
            row1 = cursor.fetchall()
            for row in row1:
                print("Id = ", row[0], )
                print("Catégorie  = ", row[1], "\n")

        except mysql.connector.Error as error:
            print("Pas de catégorie : {}".format(error))

    @staticmethod
    def new_product(nom, url, cat, prix):
        conn = BddConnection.start()
        cursor = conn.cursor()
        insert_tuple = (nom, url, cat, prix)
        print(insert_tuple)
        insert_query = """INSERT INTO produits (Nom, Url, Catégorie, prix) 
                            VALUES (%s, %s, %s, %s)"""
        try:
            insert = cursor.execute(insert_query, insert_tuple)
            conn.commit()
            print('Produit bien enregisté !')
        except mysql.connector.Error as error:
            print("le produit n'a pas été enregistré : {}".format(error))

    @staticmethod
    def update_product(id, nom, url, cat):
        conn = BddConnection.start()
        cursor = conn.cursor()
        insert_tuple = (nom, url, cat, id)
        insert_query = """UPDATE produits SET Nom = %s, Url = %s, Catégorie = %s WHERE Id = %s"""
        try:
            insert = cursor.execute(insert_query, insert_tuple)
            conn.commit()
            print('Produit mis à jour !')
        except mysql.connector.Error as error:
            print("le produit n'a pas été mis à jour : {}".format(error))

    @staticmethod
    def new_categories(nom):
        conn = BddConnection.start()
        cursor = conn.cursor()
        insert_tuple = (nom)
        insert_query = """INSERT INTO catégories (Cat_Nom) 
                            VALUES (%s)"""
        try:
            insert = cursor.execute(insert_query, (insert_tuple,))
            conn.commit()
            print('Catégorie bien enregisté !')
        except mysql.connector.Error as error:
            print("La catégorie n'a pas été enregistré : {}".format(error))

    @staticmethod
    def delete_categories(id):
        conn = BddConnection.start()
        cursor = conn.cursor()
        delete_tuple = (id)
        delete_query = "DELETE FROM catégories WHERE Cat_Id = %s"
        try:
            delete = cursor.execute(delete_query, (delete_tuple,))
            conn.commit()
            print('Catégorie bien supprimé !')
        except mysql.connector.Error as error:
            print("La catégorie n'a pas été supprimé : {}".format(error))

    @staticmethod
    def delete_product(id):
        conn = BddConnection.start()
        cursor = conn.cursor()
        delete_tuple = (id)
        delete_query = "DELETE FROM produits WHERE Id = %s"
        try:
            delete = cursor.execute(delete_query, (delete_tuple,))
            conn.commit()
            print('Produit bien supprimé !')
        except mysql.connector.Error as error:
            print("Le produit n'a pas été supprimé : {}".format(error))

    @staticmethod
    def intro():
        drawing = Figlet(font='slant')
        print(drawing.renderText("Amazon Scrapp"))

    @staticmethod
    def welcome():
        print("Bienvenue dans l'Amazon Scrapp !")
        print("Pour la liste des commandes tapez : ?")

    def list_command(self):
        for key, value in self.__command.items():
            print(key, '=>', value)

    @staticmethod
    def get_by_url(new_url):
        url_valid = validators.url(new_url)
        if url_valid:
            try:
                page = requests.get(new_url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/58.0.3029.110 Safari/537.36'})
                soup = BeautifulSoup(page.content, "html.parser")
                price_euro = soup.find(id="priceblock_ourprice").get_text()
                while price_euro is None:
                    BddConnection.get_by_url(new_url)
                trim = re.compile(r'[^\d.,]+')
                price_coma = trim.sub('', price_euro)
                new_price = float(price_coma.replace(',', '.'))
                return new_price
            except:
                print("L'url n'est pas valide")
        else:
            print("Ce n'est pas un URl valide")

    def command(self):
        user_input = input()
        if user_input == '?':
            self.list_command()
        elif user_input == 'produits':
            self.select_product()
        elif user_input == 'catégories':
            self.select_categories()
        elif user_input == 'nouveau produit':
            new_name = input("Entrez le nom du produit\n")
            new_cat = input("Entrez la catégorie du produit\n")
            new_url = input("Entrez l'url amazon du produit\n")
            new_price = self.get_by_url(new_url)
            self.new_product(new_name, new_url, new_cat, new_price)
        elif user_input == 'nouvelle catégorie':
            new_name = input('Entrez le nom de la nouvelle catégorie\n')
            self.new_categories(new_name)
        elif user_input == 'supprimer catégorie':
            cat_id = input("Entrez l'id de la catégorie à supprimer\n")
            self.delete_categories(cat_id)
        elif user_input == 'prix':
            self.get_product()
        elif user_input == 'supprimer produit':
            prod_id = input("Entrez l'id du produit à supprimer\n")
            self.delete_product(prod_id)
        else:
            print("La commande saisi n'existe pas.")

    def get_connector(self):
        return self.__connector

    def get_cursor(self):
        self.__cursor = self.__connector.cursor()
        return self.__cursor
