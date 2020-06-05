#!/usr/bin/env python
# -*- coding: utf-8 -*

from flask import Flask, render_template, request, redirect
from random import randint
import json, requests
from bs4 import BeautifulSoup
 
# Recupere l'api
params = {
          "ApiKey": "8dcc58aa-8b62-403a-bb24-4424b5001e20",
          "SearchRequest": {
            "Keyword": "Jeu ps4",
            "Pagination": {
              "ItemsPerPage": 10,
              "PageNumber": 1
            },
            "Filters": {
              "Price": {
                "Min": 0,
                "Max": 0
              },
              "Navigation": "Jeux Vidéo",
              "IncludeMarketPlace": "false"
            }
          }
        }
    
 
url = "https://api.cdiscount.com/OpenApi/json/Search"
    
nombrealea = randint(0,9)    
r = requests.post(url, data=json.dumps(params))
r = r.json()
r = r['Products'][nombrealea]
print(r)
prixproduit = float(r['BestOffer']['SalePrice'])
prixproduit = int(round(prixproduit))
print(prixproduit)

 

# initialisation des variables
prix = 0
resultat = ["", "Le prix est plus élévé", "Le prix est plus petit", "Bravo vous avez trouvé le bon prix!!!"]
debutResultat = resultat[0]
testPrixTableau = [0]
resultatTableau = [""]
nombreDeTest = 0
nombreDeTestTableau = [0]


# flask
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
  if request.method == "POST":
    global prix, debutResultat, resultatTableau, testPrixTableau, nombreDeTest, nombreDeTestTableau
    prix = request.form['Prix']
    print(prix)
    prix = int(prix)
    if prix == prixproduit:
      debutResultat = resultat[3]
      nombreDeTest = nombreDeTest + 1
    elif prix < prixproduit:
      debutResultat = resultat[1]
      resultatTableau = [debutResultat] + resultatTableau
      testPrixTableau = [prix] + testPrixTableau
      nombreDeTest = nombreDeTest + 1
      nombreDeTestTableau = [nombreDeTest] + nombreDeTestTableau
    elif prix > prixproduit:
      debutResultat = resultat[2]
      resultatTableau = [debutResultat] + resultatTableau
      testPrixTableau = [prix] + testPrixTableau
      nombreDeTest = nombreDeTest + 1
      nombreDeTestTableau = [nombreDeTest] + nombreDeTestTableau

    return redirect(request.url)

  return render_template("Index.html", prix=prix, r=r, debutResultat=debutResultat, resultatTableau=resultatTableau, testPrixTableau=testPrixTableau, nombreDeTest=nombreDeTest, nombreDeTestTableau=nombreDeTestTableau)



if __name__ == "__main__":
    app.run()






