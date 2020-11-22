from Database import Database


if __name__ == "__main__":
    bdd_start = Database()
    bdd_start.start()
    bdd_start.get_connector()
    bdd_start.get_cursor()
    bdd_start.select_product()
    bdd_start.new_product('Gigabyte GeForce GTX 1050 Ti','https://www.amazon.fr/Gigabyte-GeForce-Windforce-Carte-Graphique/dp/B01MEHGRMS/ref=sr_1_1?dchild=1&m=AY7ZJCEPH3NOJ&marketplaceID=A13V1IB3VIYZZH&qid=1606066491&s=merchant-items&sr=1-1','Carte graphique')
    bdd_start.delete_product('4')
    bdd_start.select_categories()
    bdd_start.new_categories('Led')
    bdd_start.delete_categories('7')
    bdd_start.update_product('1','AMD','ok','Carte')