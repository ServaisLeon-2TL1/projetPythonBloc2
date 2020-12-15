from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from BddConnection import BddConnection
from kivy.lang import Builder
from functools import partial
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.lang import Builder
import mysql.connector
from datetime import datetime
import sched, time
from bs4 import BeautifulSoup
from pyfiglet import Figlet
import re
import validators
import numpy as np
import requests
import matplotlib.pyplot as plt
from kivy.clock import Clock

s = sched.scheduler(time.time, time.sleep)

Window.clearcolor = (0.1, 0.5, 0.6, 1)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', '1500')
Config.set('graphics', 'height', '700')
Config.write()


class MainScreen(Screen):
    first_btn_press = True

    def show_buttons(self, btn):
        print(btn.value)
        self.manager.ids.test.ids.grid.add_widget(Label(text="", size_hint_x=(.1)))
        self.manager.ids.test.ids.grid.add_widget(Label(text="", size_hint_x=(.1)))
        self.manager.ids.test.ids.grid.add_widget(Label(text="", size_hint_x=(.1)))
        self.manager.ids.test.ids.grid.add_widget(Label(text="", size_hint_x=(.1)))
        self.manager.ids.test.ids.grid.add_widget(Label(text=" ", size_hint_x=(.1)))
        self.manager.ids.test.ids.grid.add_widget(Label(text=" ", size_hint_x=(.1)))

        self.manager.ids.test.ids.grid.add_widget(Label(text="ID", size_hint_x=(.1)))
        self.manager.ids.test.ids.grid.add_widget(Label(text="Nom", size_hint_x=(.1)))
        self.manager.ids.test.ids.grid.add_widget(Label(text="Catégories", size_hint_x=(.1)))
        self.manager.ids.test.ids.grid.add_widget(Label(text="Prix", size_hint_x=(.1)))
        self.manager.ids.test.ids.grid.add_widget(Label(text="Url", size_hint_x=(.1)))
        self.manager.ids.test.ids.grid.add_widget(Label(text="Supprimer", size_hint_x=(.1)))
        try:
            conn = BddConnection.start()
            cursor = conn.cursor()
            product = cursor.execute("""SELECT * from produits """)
            rows = cursor.fetchall()
            for row in rows:
                self.manager.ids.test.ids.grid.add_widget(Label(text=str(row[0]), size_hint_x=.1))
                self.manager.ids.test.ids.grid.add_widget(Label(text=str(row[1]), size_hint_x=.2))
                self.manager.ids.test.ids.grid.add_widget(Label(text=str(row[3]), size_hint_x=.2))
                self.manager.ids.test.ids.grid.add_widget(Label(text=str(row[4]), size_hint_x=.1))
                self.manager.ids.test.ids.grid.add_widget(Button(text=str("Voir l'url"), value=row[2], size_hint_x=.1,
                                                                 on_press=lambda x, n=row[2]: self.popup(n),
                                                                 size_hint=(0.0, 0.1)))
                self.manager.ids.test.ids.grid.add_widget(Button(text=str("Supprimer"), value=row[2], size_hint_x=.1,
                                                                 on_press=lambda x, n=row[0]: BddConnection.delete_product(n),
                                                                 size_hint=(0.0, 0.1),background_color=(1.0, 0.0, 0.0, 1.0)))


        except mysql.connector.Error as error:
            print("Pas de produit : {}".format(error))

    @staticmethod
    def popup(url):
        popup = Popup(title='Url', content=Label(text=str(url)), height=100,
                      size_hint_y=None)
        popup.open()

    def callbackStart(self):
        Clock.schedule_interval(GraphScreen1().graph_data, 60)


class NewProductWindow(Screen):
    def spinner(self):
        return BddConnection.get_cat_name()

    def new_product(self, nom, url, cat):
        if nom == "":
            print("Le nom est vide")
        elif url == "":
            print("L'url est vide")
        else:
            try:
                price = BddConnection.get_by_url(url)
                print(price)
                BddConnection.new_product(nom, url, cat, price)
            except:
                print("L'enregistrement n'a pas été effectuée")


class NewCatWindow(Screen):
    def return_cat(self, categorie):
        if categorie:
            nom_cat = str(categorie)
            print(nom_cat)
            BddConnection.new_categories(nom_cat)


class MenuScreen(Screen):
    pass


class TestScreen(Screen):
    pass


class AnotherScreen(Screen):
    pass


class GraphScreen1(Screen):

    @staticmethod
    def graph():
        price_list = []
        date_list = []
        try:
            conn = BddConnection.start()
            cursor = conn.cursor()
            product = cursor.execute("""SELECT * from graph """)
            rows = cursor.fetchall()
            for row in rows:
                price_list.append(row[1])
                date_list.append(row[2])
        except mysql.connector.Error as error:
            print("Pas de donnée : {}".format(error))
        height = price_list
        bars = date_list
        y_pos = np.arange(len(bars))
        plt.figure(figsize=(22, 7))
        plt.bar(y_pos, height)
        plt.title('Graphique 1')
        plt.xlabel('Dates')
        plt.ylabel('Prix')
        plt.yticks(rotation=45)
        plt.xticks(y_pos, bars)
        plt.show()


    @staticmethod
    def graph_data(u):

        f = open("graph1.txt", "r")
        url_valid = str(f.read())
        print(url_valid)

        try:
            page = requests.get(url_valid, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/58.0.3029.110 Safari/537.36'})
            soup = BeautifulSoup(page.content, "html.parser")
            price_euro = soup.find(id="priceblock_ourprice").get_text()

            trim = re.compile(r'[^\d.,]+')
            price_coma = trim.sub('', price_euro)
            new_price = float(price_coma.replace(',', '.'))
            print(new_price)
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%Y-%m-%d")

        except Exception as error:
            print("L'url n'est pas valide {}".format(error))

        try:
            conn = BddConnection.start()
            cursor = conn.cursor()
            insert_tuple = (new_price, timestampStr)
            insert_query = """INSERT INTO graph (prix,date) VALUES (%s, %s)"""
            insert = cursor.execute(insert_query, insert_tuple)
            conn.commit()
            print('Données bien enregisté !')
        except mysql.connector.Error as error:
            print("Les données n'ont pas été enregistrer : {}".format(error))


    def new_graph_data(self, url):
        s = sched.scheduler(time.time, time.sleep)
        url_valid = validators.url(url)
        if url_valid:
            f = open("graph1.txt", "w")
            f.write(str(url))
            f.close()
            self.empty_table()
        else:
            popup = Popup(title='Erreur', content=Label(text="Url invalide"), height=100,
                          size_hint_y=None)
            popup.open()


    def empty_table(self):
        try:
            conn = BddConnection.start()
            cursor = conn.cursor()
            insert_query = """TRUNCATE TABLE graph"""
            insert = cursor.execute(insert_query)
            conn.commit()
            print('Table vidée !')
        except mysql.connector.Error as error:
            print("La table n'a pas été vidée: {}".format(error))


    def start_recup(self):
        print("Début de la récupération...")
        self.timer = Clock.schedule_interval(self.graph_data, 60)
        print(self.timer)

    def stop_recup(self):
        self.timer.cancel()
        print("Fin de la récupération")
        Clock.unschedule(self.timer)
        print(self.timer)


class GraphScreen2(Screen):
    @staticmethod
    def graph():
        price_list = []
        date_list = []
        try:
            conn = BddConnection.start()
            cursor = conn.cursor()
            product = cursor.execute("""SELECT * from graph2 """)
            rows = cursor.fetchall()
            for row in rows:
                price_list.append(row[1])
                date_list.append(row[2])
        except mysql.connector.Error as error:
            print("Pas de donnée : {}".format(error))
        height = price_list
        bars = date_list
        y_pos = np.arange(len(bars))
        plt.figure(figsize=(22, 7))
        plt.bar(y_pos, height)
        plt.title('Graphique 2')
        plt.xlabel('Dates')
        plt.ylabel('Prix')
        plt.yticks(rotation=45)
        plt.xticks(y_pos, bars)
        plt.show()

    @staticmethod
    def graph_data(u):

        f = open("graph2.txt", "r")
        url_valid = str(f.read())
        print(url_valid)

        try:
            page = requests.get(url_valid, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/58.0.3029.110 Safari/537.36'})
            soup = BeautifulSoup(page.content, "html.parser")
            price_euro = soup.find(id="priceblock_ourprice").get_text()

            trim = re.compile(r'[^\d.,]+')
            price_coma = trim.sub('', price_euro)
            new_price = float(price_coma.replace(',', '.'))
            print(new_price)
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%Y-%m-%d")

        except Exception as error:
            print("L'url n'est pas valide {}".format(error))

        try:
            conn = BddConnection.start()
            cursor = conn.cursor()
            insert_tuple = (new_price, timestampStr)
            insert_query = """INSERT INTO graph2 (prix,date) VALUES (%s, %s)"""
            insert = cursor.execute(insert_query, insert_tuple)
            conn.commit()
            print('Données bien enregisté !')
        except mysql.connector.Error as error:
            print("Les données n'ont pas été enregistrer : {}".format(error))

    def new_graph_data(self, url):
        s = sched.scheduler(time.time, time.sleep)
        url_valid = validators.url(url)
        if url_valid:
            f = open("graph2.txt", "w")
            f.write(str(url))
            f.close()
            self.empty_table()
        else:
            popup = Popup(title='Erreur', content=Label(text="Url invalide"), height=100,
                          size_hint_y=None)
            popup.open()

    def empty_table(self):
        try:
            conn = BddConnection.start()
            cursor = conn.cursor()
            insert_query = """TRUNCATE TABLE graph2"""
            insert = cursor.execute(insert_query)
            conn.commit()
            print('Table vidée !')
        except mysql.connector.Error as error:
            print("La table n'a pas été vidée: {}".format(error))

    def start_recup(self):
        print("Début de la récupération...")
        self.timer = Clock.schedule_interval(self.graph_data, 60)
        print(self.timer)

    def stop_recup(self):
        self.timer.cancel()
        print("Fin de la récupération")
        Clock.unschedule(self.timer)
        print(self.timer)


class GraphScreen3(Screen):
    @staticmethod
    def graph():
        price_list = []
        date_list = []
        try:
            conn = BddConnection.start()
            cursor = conn.cursor()
            product = cursor.execute("""SELECT * from graph3 """)
            rows = cursor.fetchall()
            for row in rows:
                price_list.append(row[1])
                date_list.append(row[2])
        except mysql.connector.Error as error:
            print("Pas de donnée : {}".format(error))
        height = price_list
        bars = date_list
        y_pos = np.arange(len(bars))
        plt.figure(figsize=(22, 7))
        plt.bar(y_pos, height)
        plt.title('Graphique 3')
        plt.xlabel('Dates')
        plt.ylabel('Prix')
        plt.yticks(rotation=45)
        plt.xticks(y_pos, bars)
        plt.show()

    @staticmethod
    def graph_data(u):

        f = open("graph3.txt", "r")
        url_valid = str(f.read())
        print(url_valid)

        try:
            page = requests.get(url_valid, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/58.0.3029.110 Safari/537.36'})
            soup = BeautifulSoup(page.content, "html.parser")
            price_euro = soup.find(id="priceblock_ourprice").get_text()

            trim = re.compile(r'[^\d.,]+')
            price_coma = trim.sub('', price_euro)
            new_price = float(price_coma.replace(',', '.'))
            print(new_price)
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%Y-%m-%d")

        except Exception as error:
            print("L'url n'est pas valide {}".format(error))

        try:
            conn = BddConnection.start()
            cursor = conn.cursor()
            insert_tuple = (new_price, timestampStr)
            insert_query = """INSERT INTO graph3 (prix,date) VALUES (%s, %s)"""
            insert = cursor.execute(insert_query, insert_tuple)
            conn.commit()
            print('Données bien enregisté !')
        except mysql.connector.Error as error:
            print("Les données n'ont pas été enregistrer : {}".format(error))

    def new_graph_data(self, url):
        s = sched.scheduler(time.time, time.sleep)
        url_valid = validators.url(url)
        if url_valid:
            f = open("graph3.txt", "w")
            f.write(str(url))
            f.close()
            self.empty_table()
        else:
            popup = Popup(title='Erreur', content=Label(text="Url invalide"), height=100,
                          size_hint_y=None)
            popup.open()

    def empty_table(self):
        try:
            conn = BddConnection.start()
            cursor = conn.cursor()
            insert_query = """TRUNCATE TABLE graph2"""
            insert = cursor.execute(insert_query)
            conn.commit()
            print('Table vidée !')
        except mysql.connector.Error as error:
            print("La table n'a pas été vidée: {}".format(error))

    def start_recup(self):
        print("Début de la récupération...")
        self.timer = Clock.schedule_interval(self.graph_data, 60)
        print(self.timer)

    def stop_recup(self):
        self.timer.cancel()
        print("Fin de la récupération")
        Clock.unschedule(self.timer)
        print(self.timer)


kv = Builder.load_file("intro.kv")


class CoolApp(App):

    def build(self):
        return kv


if __name__ == '__main__':
    CoolApp().run()
