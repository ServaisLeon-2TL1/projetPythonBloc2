# coding: utf-8

import mysql.connector
from pyfiglet import Figlet

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
    :type command: dict
    :return connector: retourne la connexion
    :return cursor: retourne le curseur

    """
    def __init__(self):
        self.__host = "localhost"
        self.__user = "root"
        self.__passwd = ""
        self.__db = "amazon"
        self.__connector = ""
        self.__cursor = ""
        self.__title = "Amazon Scrapp"
        self.__welcome = "Bienvenue dans l'Amazon Scrapp !"
        self.__help = "Pour la liste des commandes tapez : ?"
        self.__command = {
            "?": "Affiche toute les commandes",
            "produits": "Liste tout les produits",
            "catégories":"liste les catégories",
            "nouvelle catégorie":"Permet de créer une nouvelle catégories",
            "supprimer catégorie":"Permet de supprimer une catégories",
            "supprimer produit":"Permet de supprimer un produit"
        }


    def start(self):
        try:
            self.__connector = mysql.connector.connect(host=self.__host, user=self.__user, passwd=self.__passwd, db=self.__db)
        except mysql.connector.Error as error:
            print("Impossible de se connecter à la base de données: {}".format(error))


    def select_product(self):
        try:
            cursor = self.__connector.cursor()
            product = cursor.execute("""SELECT * from produits """)
            rows = cursor.fetchall()
            print(type(rows))
            for row in rows:
                print("Id = ", row[0], )
                print("Nom = ", row[1])
                print("Url = ", row[2])
                print("Catégorie  = ", row[3], "\n")
        except mysql.connector.Error as error:
            print("Pas de produit : {}" .format(error))


    def select_categories(self):
        try:
            cursor = self.__connector.cursor()
            product = cursor.execute("""SELECT * from catégories """)
            rows = cursor.fetchall()
            print(type(rows))
            for row in rows:
                print("Id = ", row[0], )
                print("Catégorie  = ", row[1], "\n")
        except mysql.connector.Error as error:
            print("Pas de catégorie : {}".format(error))


    def new_product(self,nom,url,cat):
        cursor = self.__connector.cursor()
        insert_tuple = (nom,url,cat)
        insert_query = """INSERT INTO produits (Nom, Url, Catégorie) 
                            VALUES (%s, %s, %s)"""
        try:
            insert = cursor.execute(insert_query,insert_tuple)
            self.__connector.commit()
            print('Produit bien enregisté !')
        except mysql.connector.Error as error:
            print("le produit n'a pas été enregistré : {}" .format(error))


    def update_product(self,id,nom,url,cat):
        cursor = self.__connector.cursor()
        insert_tuple = (nom, url, cat,id)
        insert_query = """UPDATE produits SET Nom = %s, Url = %s, Catégorie = %s WHERE Id = %s"""
        try:
            insert = cursor.execute(insert_query,insert_tuple)
            self.__connector.commit()
            print('Produit mis à jour !')
        except mysql.connector.Error as error:
            print("le produit n'a pas été mis à jour : {}" .format(error))



    def new_categories(self,nom):
        cursor = self.__connector.cursor()
        insert_tuple = (nom)
        insert_query = """INSERT INTO catégories (Cat_Nom) 
                            VALUES (%s)"""
        try:
            insert = cursor.execute(insert_query,(insert_tuple,))
            self.__connector.commit()
            print('Catégorie bien enregisté !')
        except mysql.connector.Error as error:
            print("La catégorie n'a pas été enregistré : {}" .format(error))


    def delete_categories(self,id):
        cursor = self.__connector.cursor()
        delete_tuple = (id)
        delete_query = "DELETE FROM catégories WHERE Cat_Id = %s"
        try:
            delete = cursor.execute(delete_query, (delete_tuple,))
            self.__connector.commit()
            print('Catégorie bien supprimé !')
        except mysql.connector.Error as error:
            print("La catégorie n'a pas été supprimé : {}".format(error))


    def delete_product(self,id):
        cursor = self.__connector.cursor()
        delete_tuple = (id)
        delete_query = "DELETE FROM produits WHERE Id = %s"
        try:
            delete = cursor.execute(delete_query, (delete_tuple,))
            self.__connector.commit()
            print('Produit bien supprimé !')
        except mysql.connector.Error as error:
            print("Le produit n'a pas été supprimé : {}".format(error))


    def intro(self):
        drawing = Figlet(font='slant')
        print(drawing.renderText(self.__title))


    def welcome(self):
        print(self.__welcome)
        print(self.__help)


    def list_command(self):
        for key, value in self.__command.items():
            print(key, '=>', value)


    def command(self):
        user_input = input()
        if user_input == '?':
            self.list_command()
        elif user_input == 'produits':
            self.select_product()
        elif user_input == 'catégories':
            self.select_categories()
        elif user_input == 'nouvelle catégorie':
            new_name = input('Entrez le nom de la nouvelle catégorie')
            self.new_categories(new_name)
        elif user_input == 'supprimer catégorie':
            cat_id = input("Entrez l'id de la catégorie à supprimer")
            self.delete_categories(cat_id)
        elif user_input == 'supprimer produit':
            prod_id = input("Entrez l'id du produit à supprimer")
            self.delete_product(prod_id)
        else:
            print("La commande saisi n'existe pas.")


    def get_connector(self):
        return self.__connector


    def get_cursor(self):
        self.__cursor = self.__connector.cursor()
        return self.__cursor