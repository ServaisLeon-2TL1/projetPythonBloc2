# coding: utf-8
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '700')
Config.write()

class MainWindow(Screen):
    pass


class MenuWindow(Screen):
    pass

class NewProductWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass



kv = Builder.load_file("intro.kv")


class AmazonScrappApp(App):

    def build(self):
        return kv


AmazonScrappApp().run()
