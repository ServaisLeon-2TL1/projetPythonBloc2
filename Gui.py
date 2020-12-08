# coding: utf-8
import kivy
from kivy.app import App
from BddConnection import BddConnection
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

Window.clearcolor = (0.1, 0.5, 0.6, 1)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '700')
Config.write()


class MainWindow(Screen):
    pass


class MenuWindow(Screen):
    pass


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


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("intro.kv")


class AmazonScrappApp(App):

    def build(self):
        return kv
