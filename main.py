from Database import Database


if __name__ == "__main__":
    bdd_start = Database()
    bdd_start.start()
    bdd_start.intro()
    bdd_start.welcome()
    while True:
        bdd_start.command()