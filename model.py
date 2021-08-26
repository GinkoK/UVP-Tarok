import json
import random

Talon = []      # Talon je seznam nastavljen pred zacetkom igre
Kup = {}        # Slovar kart in igralcev ki so jih igrali, vsak krog se resetira na prazen slovar
Igralci = []    # Seznam igralcev, v vrstnem redu

# Seznami kart:

class Igralec:
    def __init__(self, lastne_karte, ime):
        self.roka = lastne_karte        # Seznam kart, t.j. stevilk od 1 do 54, ki jih igralec drzi v roki. Spreminja se le s fukncijima vzemi_karto in dodaj_karto.
        self.ime = ime                  # Ime igralca je niz, sluzi le za prikaz in shranjevanje podatkov, v igri se ne uporablja.
        self.pobrane = []
        Igralci.append(self)

    def __repr__(self):
        return self.ime
    
    def vzame_karto(self, stevilka):
        del self.roka[stevilka]

    def doda_karto(self, karta):
        self.roka.append(karta)
    
    def igra(self, karta):
        igrana = self.roka[karta]
        self.vzame_karto(karta)
        Kup[self] = igrana

    def pobere(self):
        global Kup
        for x in Kup.values():
            self.pobrane.append(x)
        Kup = {}

def igralecVR(n):     # Vrne n-tega igralca
    return Igralci[n]

def tip_karte(karta):
    if karta <= 22:
        return "Tarok"
    if karta >= 23 and karta <= 30:
        return "Src"
    if karta >= 31 and karta <= 38:
        return "Kara"
    if karta >= 39 and karta <= 46:
        return "Pik"
    if karta >= 47 and karta <= 54:
        return "Kriz"

def primerjaj_karti(karta1, karta2):
    if tip_karte(karta2) == "Tarok":
        if tip_karte(karta1) == "Tarok":
            if karta1 > karta2:
                return karta1
            else:
                return karta2
        else:
            return karta2
    elif tip_karte(karta1) == "Tarok":
        return karta1
    elif tip_karte(karta2) != tip_karte(karta1):
        return karta1
    else:
        if karta1 > karta2:
            return karta1
        else:
            return karta2

def zmagovalni_igralec():
    karte = []      # Optimiziraj s tem da preveris ce je bila vsaj ena od teh kart igrana
    for z in Igralci:
        karte.append(Kup[z])
    if 1 in karte and 21 in karte and 22 in karte:
        zmagovalka = 1
    else:
        zmagovalka = Kup[igralecVR(0)]
        for x in Igralci:
            zmagovalka = primerjaj_karti(zmagovalka, Kup[x])
    for y in Igralci:
        if Kup[y] == zmagovalka:
            return y

def delitev_kart():
    global Talon
    vse_karte = [n for n in range(1, 55)]
    random.shuffle(vse_karte)
    i = 0
    kolicina = (54 - 6) // len(Igralci)
    for oseba in Igralci:
        oseba.roka = vse_karte[kolicina*i: kolicina*(i+1)]
        i += 1
    Talon = vse_karte[-6:]



        
































Mitja = Igralec([1, 20, 14, 27, 33, 36, 38], "Mitja")
Andrej = Igralec([21, 12, 15, 28, 26, 54, 7], "Andrej")
Maja = Igralec([22, 5, 6, 18, 34, 39], "Maja")