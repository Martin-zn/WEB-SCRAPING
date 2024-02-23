import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.portalinmobiliario.com/arriendo/departamento/rm-metropolitana/la-florida/metro-mirador"
counter = 0
Names = []
Prices = []
Atributtes = []
atributtesOrdenados = []
links = []
links.append(url)
#=====================Chat GPT  INICIO===================================
def dividir_en_grupos(lista, tamaño_grupo):
    grupos = []
    for i in range(0, len(lista), tamaño_grupo):
        grupo = lista[i:i + tamaño_grupo]
        grupos.append(grupo)
    return grupos

def formar_strings(lista):
    strings = []
    for grupo in lista:
        string = ','.join(grupo)
        strings.append(string)
    return strings
#=====================Chat GPT  FIN===================================
try:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    while counter < 3:

        link = soup.find("li", class_ = "andes-pagination__button andes-pagination__button--next")
        i = link.find("a", class_ = "andes-pagination__link")
        l = i.get("href")
        print(l)
        links.append(l)
        counter += 1
        url = l
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
except ValueError:
     print("No hay mas paginas")


for i in links:
    print(i)

for i in links:

    r = requests.get(i)
    soup = BeautifulSoup(r.text, "html.parser")


    #util = soup.find("section", class_ = "ui-search-results")
    util = soup.find("ol")


    #Veamos los nombres
    names = util.find_all("div", class_ = "ui-search-item__title-label-grid")
    for i in names:
        Names.append(i.text)

    #Obtengo los valores
    prices = util.find_all("span", class_ = "andes-money-amount__fraction")
    for i in prices:
        Prices.append(i.text)


    #Obtengo los atributos 
    atributtes = util.find_all("li", class_ = "ui-search-card-attributes__attribute")
    for i in atributtes:
        atributtesOrdenados.append(i.text)
    grupos = dividir_en_grupos(atributtesOrdenados, 3)
    Atributtes = formar_strings(grupos)

    print(len(Names))
    print(len(Prices))
    print(len(Atributtes))




#DataFrame

df = pd.DataFrame({"Name":Names, "Prices":Prices, "Dormitorios,Baños,Metros": Atributtes})
print(df)


df.to_csv("pagina3.csv")


