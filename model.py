import json
import random

Talon = []      # Talon je seznam nastavljen pred zacetkom igre
Kup = {}        # Slovar kart in igralcev ki so jih igrali, vsak krog se resetira na prazen slovar
Igralci = []    # Seznam igralcev, v vrstnem redu
Porufani = None

class Igralec:
    def __init__(self, ime):
        self.roka = []                  # Seznam kart, t.j. stevilk od 1 do 54, ki jih igralec drzi v roki.
        self.ime = ime                  # Ime igralca je niz, sluzi le za prikaz in shranjevanje podatkov, v igri se ne uporablja.
        self.pobrane = []
        Igralci.append(self)

    def __repr__(self):
        return self.ime
        
    
    def vzame_karto(self, stevilka):
        del self.roka[stevilka]

    def doda_karte(self, karte):
        self.roka.extend(karte)
    
    def igra(self, karta):
        igrana = self.roka[karta]
        self.vzame_karto(karta)
        Kup[self] = igrana

    def pobere(self):
        global Kup
        for x in Kup.values():
            self.pobrane.append(x)
        Kup = {}

    def pobere_talon(self):
        global Talon
        self.pobrane.extend(Talon)
        Talon = []



def igralecVR(n):
    return Igralci[n]




# Funkcije ki so namenjene dolocanju zmagovlca kroga.

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




# Funkcije namenjene zacetku igre.

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

def del_talona(n, k):       # n je stevilo delov talona, k je izbran del
    return Talon[k*n: (k+1)*n]

def ostali_talon(n, k):
    global Talon
    for j in del_talona(n,k):
        Talon.remove(j)
    return Talon
        
def talon_igra(rufer, n, k, kralj):
    rufer.doda_karte(del_talona(n,k))
    for oseba in Igralci:
        if oseba != rufer and kralj not in oseba.roka:
            oseba.pobere_talon()
            break

def prioritetni_igralec(prvi, drugi):
    if Igralci.index(drugi) == (len(Igralci) - 1):
        return drugi
    else:
        if Igralci.index(prvi) < Igralci.index(drugi):
            return prvi
        else:
            return drugi


def mocnejsa_izbira(prva, druga):      # prva in druga sta seznama igralca in igre (npr. [Andrej, 2])
    if prva[1] == 0:
        return druga
    elif druga[1] == 0:
        return prva
    elif prva[1] > druga[1]:        # Igre grejo po vrsti od najsibkejse do najmocnejse: 0 ni igra, 1 je tri, 2 je dva, 1 je tri, ...
        return prva
    elif druga[1] > prva[1]:
        return druga
    elif prioritetni_igralec(prva[0], druga[0]) == prva[0]:
        return prva
    else:
        return druga




























