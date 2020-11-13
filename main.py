from pieceDict import piece
from bs4 import BeautifulSoup
import requests

def main():
    self = True
    userInput = input("\n \n \n Bienvenu dans le Amazon Scrapper. "
                      "\n Pour afficher les produits tapez '/produits' "
                      "\n Pour afficher les détails tapez '/leproduit' "
                      "\n Pour ajouter un produit à la liste '/leNouveauProduit \n ")
    while self == True:
        try:
            if userInput == "/produits":
                print("\n\nListe des produits :")

                products()
                break;


            elif userInput == "/leproduit":
                print("\n\n Le produits")

            elif userInput == "/leNouveauProduit":
                print("\n\n Le Nouveau produit")

            elif userInput == "/help":
                input("Liste des commandes : "
                      "\n Pour afficher les produits tapez '/produits' "
                      "\n Pour afficher les détails tapez '/leproduit' "
                      "\n Pour ajouter un produit à la liste '/leNouveauProduit ")
                break;


            elif userInput == 'stop':
                self == False
                break;

            else:

                productsDetails(userInput)


        except:
            print('Veuillez respecter la syntaxe')
            main()

def products():

    for key,value in piece.items():
        print(key, ' -> Son url : ', value)

    main();

def productsDetails(product):

    for key, value in piece.items():
        if product == key:
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/58.0.3029.110 Safari/537.36'}
            page = requests.get(value, headers=header)
            soup = BeautifulSoup(page.content, "html.parser")
            price = soup.find(id="priceblock_ourprice").get_text()
            print(price)
    main()



if __name__ == "__main__":
    main()






