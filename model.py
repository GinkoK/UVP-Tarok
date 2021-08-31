import json
import random

Talon = []      # Talon je seznam nastavljen pred zacetkom igre
Kup = {}        # Slovar kart in igralcev ki so jih igrali, vsak krog se resetira na prazen slovar
Igralci = []    # Seznam igralcev, v vrstnem redu
Napovedi = []

class Igralec:
    def __init__(self, ime):
        self.roka = []                  # Seznam kart, t.j. stevilk od 1 do 54, ki jih igralec drzi v roki.
        self.ime = ime                  # Ime igralca je niz, sluzi le za prikaz in shranjevanje podatkov, v igri se ne uporablja.
        self.pobrane = []
        self.rufan = False
        self.kralj = 0
        self.ima_monda = False      # Na koncu se sprehodi cez vse pobrane v korakih po 4 ali 3 ce imajo monda in skisa in ne palcke in odstej tocke temu igralcu
        self.ima_skisa = False
        self.vrsta_igre = 0      # Podobno kot zgoraj ampak za celo trulo
        self.pobran_pagat = False
        self.pobran_kralj = False
        Igralci.append(self)

    def __repr__(self):
        return self.ime
        
    
    def vzame_karto(self, karta):
        self.roka.remove(karta)

    def doda_karte(self, karte):
        self.roka.extend(karte)
    
    def igra(self, karta):
        self.vzame_karto(karta)
        Kup[self] = karta

    def pobere(self):
        global Kup
        for x in Kup.values():
            self.pobrane.append(x)
        Kup = {}

    def pobere_talon(self):
        global Talon
        self.pobrane.extend(Talon)
        Talon = []


# Funkcije namenjene sami igri

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

def zmagovalni_igralec():       # Preveri karte iz Kupa
    karte = []      # Optimiziraj s tem da preveris ce je bila vsaj ena od teh kart igrana
    for z in Igralci:
        karte.append(Kup[z])
    if 1 in karte and 21 in karte and 22 in karte:
        zmagovalka = 1
    else:
        zmagovalka = Kup[Igralci[0]]
        for x in Igralci:
            zmagovalka = primerjaj_karti(zmagovalka, Kup[x])
    for y in Igralci:
        if Kup[y] == zmagovalka:
            return y


    # Funkcije namenjene sami igri

def vrstni_red(zacne):
    n = len(Igralci)
    indeks = Igralci.index(zacne) + 1
    Vrstni_red = [zacne]
    for i in range(n-1):
        Vrstni_red.append(Igralci[(indeks + i) % n])
    return Vrstni_red

def legalna_izbira(prva, oseba, izbira):        # ZACASNA FUNKCIJA, DOPOLNI KASNEJE
    return True


# Funkcije namenjene zacetku igre.

    # Funkcije za razdeliti karte med igralce.

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

    # Funkcije za prikaz in deljenje talona.

def delitev_talona(igra):       # ZACASNA FUNKCIJA, dopolni ko bos dodal ostale igre!!!!!
    if igra[1] == 1:
        return 3
    if igra[1] == 2:
        return 2
    if igra[1] == 3:
        return 1

def prikaz_talona(igra):        # ZACASNA FUNKCIJA
    presek_talona = delitev_talona(igra)
    prikaz_talona = ''
    for k in range(6 // presek_talona):
        por = del_talona(presek_talona, k)
        for j in range(presek_talona):
            prikaz_talona += str(por[j])
            if j != (presek_talona - 1):
                prikaz_talona += ', '
        if k != ((6 // presek_talona) -1):
            prikaz_talona += ';   '
    return prikaz_talona

def del_talona(n, k):       # n je stevilo delov talona, k je izbran del
    return Talon[k*n: (k+1)*n]

def ostali_talon(n, k):
    global Talon
    for j in del_talona(n,k):
        Talon.remove(j)
    return Talon

def spremeni_talon(igra, k):
    global Talon
    nov_talon = []
    for j in range(igra[1]):
        if j != k:
            nov_talon.extend(del_talona(igra[1], j))
    Talon = nov_talon


def talon_prevzem(rufer, n, k): # NA KONCU NAJ UGOTOVI A JE VALAT AL SE JE ZARUFU IN POBRAL KRALJA, DRUGACE DOBI NASPROTNIK VALATA
    for oseba in Igralci:
        if oseba != rufer and oseba.rufan != 1:
            oseba.pobere_talon()
            break

def stevilo_zalozenih(igra):
    izbira = igra[1]
    if izbira == 1 or izbira == 4:
        return 3
    if izbira == 2 or izbira == 5:
        return 2
    if izbira == 3 or izbira == 6:
        return 1
    else:
        return 0

def legaln_polog(igra, karta): # NAPISI DEJANSKO FUNKCIJO
    return True



    # Funkcije za izbiro igre na zacetku

def prioritetni_igralec(prvi, drugi):
    if Igralci.index(drugi) == (len(Igralci) - 1):
        return drugi
    else:
        if Igralci.index(prvi) < Igralci.index(drugi):
            return prvi
        else:
            return drugi


def mocnejsa_izbira(prva, druga):      # prva in druga sta seznama igralca in igre (npr. [Andrej, 2]), funkcije najde kdo ima prednost za izbiro igre na zacetku
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



    # Funkcije za rufanje kralja

def ima_rufanje(igra):      # Zacasna funkcija, dopolni za vse igre!!!!!!
    if len(Igralci) == 4: 
        return True
    else:
        return False

def karta_v_stevilko(ime):      # Zacasna funkcija, izbrisi pol
    if ime.lower() == "src":
        return 1
    if ime.lower() == "kara":
        return 2
    if ime.lower() == "pik":
        return 3
    if ime.lower() == "kriz":
        return 4
    

# Konec igre

def vrednost_karte(karta):
    if karta == 1 or karta == 21 or karta == 22:
        return 5
    elif karta < 21:
        return 1
    elif karta % 8 >= 3 and karta % 8 <= 6:
        return (karta % 8) - 1
    else:
        return 1


def tocke():
    tocke = 0
    karte_za_stet = []
    for oseba in Igralci:
        if oseba.rufan == 1:
            karte_za_stet.extend(oseba.pobrane)
    for karta in karte_za_stet:
        tocke += vrednost_karte(karta)
    tocke = tocke - (2 * (len(karte_za_stet) // 3))
    if len(karte_za_stet) % 3 != 0:
        tocke = tocke - 1
    if tocke > 35 or (tocke == 35 and len(karte_za_stet) % 3 > 0):
        zmaga = True
    else:
        zmaga = False
    return [zmaga, 5*round(tocke/5)]

def napovedan_bonus(napoved):
    if napoved in Napovedi:
        return 2
    else:
        return 1

def vrednost_igre():
    for oseba in Igralci:
        izbira = oseba.vrsta_igre
        if izbira != 0:
            if izbira == 1: # Tri
                return 10 * napovedan_bonus(izbira)
            if izbira == 2: # Dva
                return 20 * napovedan_bonus(izbira)
            if izbira == 3: # Ena
                return 30 * napovedan_bonus(izbira)
            if izbira == 4: # Solo tri
                return 40 * napovedan_bonus(izbira)
            if izbira == 5: # Solo dva
                return 50 * napovedan_bonus(izbira)
            if izbira == 6: # Solo ena
                return 60 * napovedan_bonus(izbira)
            if izbira == 7: # Solo brez
                return 70 * napovedan_bonus(izbira)
            if izbira == 8: # Berac
                return 80 * napovedan_bonus(izbira)
    return 0

def igra_ima_tocke():
    for oseba in Igralci:
        izbira = oseba.vrsta_igre
        if izbira != 0:
            if izbira <= 6:
                return True
            else:
                return False
    return False

def preveri_valat():
    karte = []
    for oseba in Igralci:
        if oseba.rufan == False:
            karte += oseba.pobrane
    if len(karte) == 0:
        return True
    else:
        return False
def dodeli_talon():
    global Talon
    kartarji = []
    if len(Igralci) == 3:
        pass
    for oseba in Igralci:
        if oseba.rufan == True:
            kartarji.append(oseba)
            kralj = oseba.kralj
    if (len(kartarji) == 1 and kralj in kartarji[0].pobrane) or preveri_valat():
        kartarji[0].pobrane.extend(Talon)
        Talon = []

def bon(vrednost):
    karte = Talon
    sestevek = 0
    pagat = 0
    ultimo = 0
    for oseba in Igralci:
        if oseba.rufan == vrednost:
            karte.extend(oseba.pobrane)
            if oseba.pobran_pagat:
                pagat = True
            if oseba.pobran_kralj:
                ultimo = True
    if 1 in karte and 21 in karte and 22 in karte:
        sestevek += 10 * napovedan_bonus('trula')
    if 30 in karte and 38 in karte and 46 in karte and 54 in karte:
        sestevek += 10 * napovedan_bonus('kralji')
    if pagat:
        sestevek += 25 * napovedan_bonus('pagat ultimo')
    if ultimo:
        sestevek += 10 * napovedan_bonus('kralj ultimo')
    return sestevek

def bonusi(sestevek):
    sestevek + bon(True)- bon(False)
    return sestevek













