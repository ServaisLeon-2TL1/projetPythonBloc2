from kivy.uix.screenmanager import ScreenManager, Screen
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
import numpy as np
import requests
import matplotlib.pyplot as plt


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

        self.manager.ids.test.ids.grid.add_widget(Label(text="ID", size_hint_x=(.1)))
        self.manager.ids.test.ids.grid.add_widget(Label(text="Nom", size_hint_x=(.1)))
        self.manager.ids.test.ids.grid.add_widget(Label(text="Catégories", size_hint_x=(.1)))
        self.manager.ids.test.ids.grid.add_widget(Label(text="Prix", size_hint_x=(.1)))
        self.manager.ids.test.ids.grid.add_widget(Label(text="Url", size_hint_x=(.1)))
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
                                                                 on_press=lambda x: print(self.Button.value),
                                                                 size_hint=(0.0, 0.3)))


        except mysql.connector.Error as error:
            print("Pas de produit : {}".format(error))

    def popup(self, url):
        print(url.value)
        # popup = Popup(title='Test popup', content=Label(text=str(url)),
        # auto_dismiss=False)
        # popup.open()


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


    def graph_data(sc):
        global new_price, timestampStr
        url_valid = "https://www.amazon.fr/dp/B074JCXNLF/ref=sspa_dk_detail_0?psc=1&pd_rd_i=B074JCXNLF&pd_rd_w=Uusxk&pf_rd_p=6eaac53c-8072-49a8-9401-5813fe195aad&pd_rd_wg=4eiNm&pf_rd_r=7FCG57B4PTW6WWNTX5SX&pd_rd_r=643eb9a9-014f-4aca-9d42-bb9a82d02a06&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyTko5MDVZVUNMTkkxJmVuY3J5cHRlZElkPUEwMTY2NDUzWTFEMk82OU9FSFI4JmVuY3J5cHRlZEFkSWQ9QTAxNDA0NTMxRDRRS0ZZWlVaTVlEJndpZGdldE5hbWU9c3BfZGV0YWlsJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=="
        try:
            page = requests.get(url_valid, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/58.0.3029.110 Safari/537.36'})
            soup = BeautifulSoup(page.content, "html.parser")
            price_euro = soup.find(id="priceblock_ourprice").get_text()

            while price_euro is None:
                graph_data(sc)
            trim = re.compile(r'[^\d.,]+')
            price_coma = trim.sub('', price_euro)
            new_price = float(price_coma.replace(',', '.'))
            print(new_price)
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%Y-%m-%d")
            s.enter(60, 1, graph_data, (sc,))
        except Exception as error:
            print("L'url n'est pas valide {}".format(error))
        conn = start()
        cursor = conn.cursor()
        insert_tuple = (new_price, timestampStr)
        insert_query = """INSERT INTO graph (prix,date) 
                                    VALUES (%s, %s)"""
        try:
            insert = cursor.execute(insert_query, insert_tuple)
            conn.commit()
            print('Données bien enregisté !')
        except mysql.connector.Error as error:
            print("Les Données n'a pas été enregistré : {}".format(error))
        s.enter(60, 1, graph_data, (sc,))
        s.run()


class GraphScreen2(Screen):
    pass


class GraphScreen3(Screen):
    pass


kv = Builder.load_file("intro.kv")


class CoolApp(App):
    def build(self):
        return kv
