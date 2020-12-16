from Database import Database


if __name__ == "__main__":
    bdd_start = Database()
    bdd_start.intro()
    Gui = GuiApp()
    Gui.welcome()
    Gui.run()