import validators
from pyfiglet import Figlet
from bs4 import BeautifulSoup
import mysql.connector
import requests
import re


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

    """

    @staticmethod
    def start():
        """
            Connecte l'application à la base de données
            :return: Renvoie le connecteur de la base de donnée
        """
        try:
            connector = mysql.connector.connect(host="localhost", user="root", passwd="", db="amazon")
            return connector
        except mysql.connector.Error as error:
            print("Impossible de se connecter à la base de données: {}".format(error))


    @staticmethod
    def select_product():
        """
             Récupère tout les produits enregistrés dans la base de données et les affiches en console
            :return: Renvoie la liste contenant les données
        """
        try:
            conn = BddConnection.start()
            cursor = conn.cursor()
            product = cursor.execute("""SELECT * from produits """)
            rows = cursor.fetchall()
            for row in rows:
                print("Id = ", row[0])
                print("Nom = ", row[1])
                print("Url = ", row[2])
                print("Catégorie  = ", row[3])
                print("Prix = ", row[4], "\n")
            return rows
        except mysql.connector.Error as error:
            print("Pas de produit : {}".format(error))

    @staticmethod
    def get_cat_name():
        """
            Récupère toute les catégories de la base de données
            :return: Renvoie la liste contenant les données
        """
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
        """
            Récupère toute les infos sur les catégories enregistrés dans la base de données
            :return: Renvoie la liste contenant les données
        """
        try:
            conn = BddConnection.start()
            cursor = conn.cursor()
            cat = cursor.execute("""SELECT * from catégories """)
            rows = cursor.fetchall()
            for row in rows:
                print("Id = ", row[0], )
                print("Catégorie  = ", row[1], "\n")
            return rows
        except mysql.connector.Error as error:
            print("Pas de catégorie : {}".format(error))

    @staticmethod
    def new_product(nom, url, cat, prix):
        """
            Récupère toute les infos sur les catégories enregistrés dans la base de données
            :return: Renvoie la liste contenant les données
        """
        conn = BddConnection.start()
        cursor = conn.cursor()
        insert_tuple = (nom, url, cat, prix)
        print(insert_tuple)
        insert_query = """INSERT INTO produits (Nom, Url, Catégorie, prix) 
                            VALUES (%s, %s, %s, %s)"""
        try:
            insert = cursor.execute(insert_query, insert_tuple)
            conn.commit()
            print('Produit bien enregistré !')

        except mysql.connector.Error as error:
            print("le produit n'a pas été enregistré : {}".format(error))


    @staticmethod
    def update_product(id, nom, url, cat, prix):

        """
            Permet de modifier un produit
            :param id: L'id du produit
            :param nom: Nom du produit
            :param url: L'url du produit
            :param cat: La Catégorie du produit
            :param prix: Le prix du produit récupéré automatiquement

        """
        conn = BddConnection.start()
        cursor = conn.cursor()
        insert_tuple = (nom, url, cat, prix, id)
        insert_query = """UPDATE produits SET Nom = %s, Url = %s, Catégorie = %s, prix = %s WHERE Id = %s"""
        try:
            insert = cursor.execute(insert_query, insert_tuple)
            conn.commit()
            print('Produit mis à jour !')
        except mysql.connector.Error as error:
            print("le produit n'a pas été mis à jour : {}".format(error))


    @staticmethod
    def update_cat(id, nom):
        """
            Permet de modifier une catégorie
            :param id: L'id de la catégorie
            :param nom: Le Nom de la catégorie
        """
        conn = BddConnection.start()
        cursor = conn.cursor()
        insert_tuple = (nom, id)
        insert_query = """UPDATE catégories SET Cat_nom = %s WHERE Cat_id = %s"""
        try:
            insert = cursor.execute(insert_query, insert_tuple)
            conn.commit()
            print('Catégorie mise à jour !')
        except mysql.connector.Error as error:
            print("La catégorie n'a pas été mise à jour : {}".format(error))


    @staticmethod
    def new_categories(nom):
        """
            Permet de créer une nouvelle catégorie
            :param nom: Le Nom de la catégorie
        """
        if type(nom) == str:
            conn = BddConnection.start()
            cursor = conn.cursor()
            insert_tuple = (nom)
            insert_query = """INSERT INTO catégories (Cat_Nom) 
                                VALUES (%s)"""
            try:
                insert = cursor.execute(insert_query, (insert_tuple,))
                conn.commit()
                print('Catégorie bien enregisté !')
                return True
            except mysql.connector.Error as error:
                print("La catégorie n'a pas été enregistré : {}".format(error))
                return error
        else:
            print("La catégorie ne doit peut être qu'une chaîne de caractère")

    @staticmethod
    def delete_categories(id):
        """
            Permet de supprimer une catégorie
            :param id: L'id de la catégorie
        """
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
        """
            Permet de supprimer un produit
            :param id: L'id du produit
        """
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
        """
            Affiche le titre avec un design particulier
        """
        drawing = Figlet(font='slant')
        print(drawing.renderText("Amazon Scrapp"))


    @staticmethod
    def list_command():
        """
            Stock et affiche la liste des commandes
        """
        command = {
            "?": "Affiche toute les commandes",
            "produits": "Liste tout les produits",
            "catégories": "liste les catégories",
            "nouvelle catégorie": "Permet de créer une nouvelle catégories",
            "nouveau produit": "Permet de créer une nouveau produit",
            "supprimer catégorie": "Permet de supprimer une catégories",
            "supprimer produit": "Permet de supprimer un produit",
            "modifier produit": "Permet de modifier un produit existant",
            "modifier catégorie": "Permet de modifier une catégorie existante",
            "q": "Permet de quitter l'application"
        }
        for key, value in command.items():
            print(key, '=>', value)


    @staticmethod
    def get_by_url(new_url):
        """
            Vérifie l'authenticité d'un url et récupère son prix
            :param new_url: Nouvel url transmit par l'utilisateur
        """
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

    @staticmethod
    def command():
        """
            Permet de répondre au commande de l'utilisateur
        """
        while True:
            user_input = input()
            if user_input == '?':
                list_command()
            elif user_input == 'produits':
                select_product()
            elif user_input == 'catégories':
                select_categories()
            elif user_input == 'nouveau produit':
                new_name = input("Entrez le nom du produit\n")
                new_cat = input("Entrez la catégorie du produit\n")
                new_url = input("Entrez l'url amazon du produit\n")
                new_price = self.get_by_url(new_url)
                new_product(new_name, new_url, new_cat, new_price)
            elif user_input == 'nouvelle catégorie':
                new_name = input('Entrez le nom de la nouvelle catégorie\n')
                new_categories(new_name)
            elif user_input == 'supprimer catégorie':
                cat_id = input("Entrez l'id de la catégorie à supprimer\n")
                delete_categories(cat_id)
            elif user_input == 'prix':
                get_product()
            elif user_input == 'supprimer produit':
                prod_id = input("Entrez l'id du produit à supprimer\n")
                delete_product(prod_id)
            elif user_input == 'modifier produit':
                prod_id = input("Entrez l'id du produit à modifier\n")
                prod_nom = input("Entrez le nom du produit à modifier\n")
                prod_cat = input("Entrez la catégorie du produit à modifier\n")
                prod_url = input("Entrez l'url amazon du produit à modifier\n")
                new_price = self.get_by_url(prod_url)
                update_product(prod_id, prod_nom, prod_url, prod_cat, new_price)
            elif user_input == 'modifier catégorie':
                cat_id = input("Entrez l'id de la catégorie à modifier\n")
                cat_nom = input("Entrez le nom de la catégorie à modifier\n")
                update_cat(cat_id, cat_nom)
            elif user_input == 'q':
                quit()
            else:
                print("La commande saisi n'existe pas.")