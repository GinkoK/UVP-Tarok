import json
import random
import hashlib

Talon = []      # Talon je seznam nastavljen pred zacetkom igre
Kup = {}        # Slovar kart in igralcev ki so jih igrali, vsak krog se resetira na prazen slovar
Igralci = []    # Seznam igralcev, v vrstnem redu
Napovedi = []
Trenutni_igralec = None
izbrana_igra = []
Vrstni_red = []
Prva = 0

DATOTEKA = "podatki.json"
DAT_IGRALCI = "cakajoci.txt"
DAT_IGRA = "igra.json"

class Igralec:
    def __init__(self, ime, zasifrirano_geslo):
        self.zasifrirano_geslo = zasifrirano_geslo
        self.tocke = 0
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


    def v_slovar(self):
        return {
            "uporabnisko_ime": self.ime,
            "zasifrirano_geslo": self.zasifrirano_geslo,
            "tocke": self.tocke
        }

    @staticmethod
    def registracija(uporabnisko_ime, geslo_v_cistopisu):

        if Igralec.preberi_iz_datoteke(uporabnisko_ime) != None:
            raise ValueError("Uporabniško ime že obstaja!")
        else:
            zasifrirano_geslo = Igralec.zasifriraj_geslo(geslo_v_cistopisu)
            uporabnik = Igralec(uporabnisko_ime, zasifrirano_geslo)
            uporabnik.shrani_v_datoteko()
            return uporabnik

    @staticmethod
    def iz_slovarja(slovar):
        uporabnisko_ime = slovar["uporabnisko_ime"]
        zasifrirano_geslo = slovar["zasifrirano_geslo"]
        tocke = slovar["tocke"]
        uporabnik = Igralec(uporabnisko_ime, zasifrirano_geslo)
        uporabnik.tocke = tocke
        return uporabnik

    def shrani_v_datoteko(self):
        with open(DATOTEKA, 'r') as dat:
            slovar_vseh = json.load(dat)
        with open(DATOTEKA, 'w') as dat:
            slovar = self.v_slovar()
            slovar_vseh[self.ime] = slovar
            json.dump(slovar_vseh, dat)

    @staticmethod
    def preberi_iz_datoteke(uporabnisko_ime):
        try:
            with open(DATOTEKA) as dat:
                slovar_vseh = json.load(dat)
                if uporabnisko_ime in slovar_vseh:
                    slovar = slovar_vseh[uporabnisko_ime]
                    return Igralec.iz_slovarja(slovar)
                else:
                    return None
        except FileNotFoundError:
            return None

    def zasifriraj_geslo(geslo_v_cistopisu, sol=None):
        if sol is None:
            sol = str(random.getrandbits(32))
        posoljeno_geslo = sol + geslo_v_cistopisu
        h = hashlib.blake2b()
        h.update(posoljeno_geslo.encode(encoding="utf-8"))
        return f"{sol}${h.hexdigest()}"

    def preveri_geslo(self, geslo_v_cistopisu):
        sol = self.zasifrirano_geslo.split("$")[0]
        return self.zasifrirano_geslo == Igralec.zasifriraj_geslo(geslo_v_cistopisu, sol)

    @staticmethod
    def prijava(uporabnisko_ime, geslo_v_cistopisu):
        uporabnik = Igralec.preberi_iz_datoteke(uporabnisko_ime)
        if uporabnik is None:
            raise ValueError("Uporabniško ime ne obstaja!")
        elif uporabnik.preveri_geslo(geslo_v_cistopisu):
            return uporabnik        
        else:
            raise ValueError("Geslo je napačno!")



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

def zmagovalni_igralec(): 
    karte = []
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

def legalna_izbira(prva, oseba, izbira):
    if tip_karte(izbira) == tip_karte(prva):
        return True
    if tip_karte(izbira) == "Tarok":
        for x in oseba.roka:
            if tip_karte(x) == tip_karte(prva):
                return False
        return True
    else:
        for x in oseba.roka:
            if tip_karte(x) == tip_karte(prva) or tip_karte(x) == "Tarok":
                return False
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

def prikaz_talona(igra):        # SAMO ZA TEKSTOVNI VMESNIK
    presek_talona = stevilo_zalozenih(igra)
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


def talon_prevzem(rufer, n, k):
    for oseba in Igralci:
        if oseba != rufer and oseba.rufan != 1:
            oseba.pobere_talon()
            break

def legaln_polog(igra, karta):
    if karta not in [1, 21, 22, 30, 38, 46, 54]:
        if tip_karte(karta) == "Tarok":
            for x in igra[0].roka:
                if x != "Tarok" or x % 8 != 6:
                    return False
            return True
        else:
            return True
    else:
        return False

def preveri_fang():
    for oseba in Igralci:
        if 21 in oseba.roka:
            oseba.ima_monda = True
        if 22 in oseba.roka:
            oseba.ima_monda = True

    # Funkcije za izbiro igre na zacetku

def prioritetni_igralec(prvi, drugi):
    for x in Igralci:
        if x.ime == drugi.ime:
            indeks_drugega = Igralci.index(x)
        if x.ime == prvi.ime:
            indeks_prvega = Igralci.index(x)
    if indeks_drugega == (len(Igralci) - 1):
        return True
    else:
        if indeks_prvega < indeks_drugega:
            return False
        else:
            return True


def mocnejsa_izbira(prva, druga):      # prva in druga sta seznama igralca in igre (npr. [Andrej, 2]), funkcije najde kdo ima prednost za izbiro igre na zacetku
    if prva[1] == 0:
        return True
    elif druga[1] == 0:
        return False
    elif prva[1] > druga[1]:
        return False
    elif druga[1] > prva[1]:
        return True
    elif prioritetni_igralec(prva[0], druga[0]):
        return True
    else:
        return False

def igra_ima_talon(igra):
    if igra[1] >= 1 and igra[1] <= 6:
        return True
    else:
        return False

    # Funkcije za rufanje kralja

def ima_rufanje(igra):
    if igra[1] in [1, 2, 3]: 
        return True
    else:
        return False

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


def tockovanje():
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
            return 10 * izbira
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
    karte = []
    if vrednost == False:
        karte.extend(Talon)
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
    return sestevek + bon(True)- bon(False)

def resetiraj():
    global Talon, Kup, Napovedi, Trenutni_igralec, izbrana_igra, Vrstni_red, Prva
    Talon = []
    Kup = {}
    Napovedi = []
    Trenutni_igralec = None
    izbrana_igra = []
    Vrstni_red = []
    Prva = 0
    for oseba in Igralci:
        oseba.roka = []                  # Seznam kart, t.j. stevilk od 1 do 54, ki jih igralec drzi v roki.
        oseba.pobrane = []
        oseba.rufan = False
        oseba.kralj = 0
        oseba.ima_monda = False
        oseba.ima_skisa = False
        oseba.vrsta_igre = 0
        oseba.pobran_pagat = False
        oseba.pobran_kralj = False
    



# IZOGIBANJE BOTTLA PREK JSONA Z JAVASCRIPTOM

def shrani_stevilo():
    with open(DAT_IGRALCI, 'w') as dat:
        info = str(len(Igralci))
        dat.write(info)
    print(Igralci)

def zapis_kart():
    with open(DAT_IGRA, 'w') as dat:
        slovar = {}
        slovar["trenutni"] = Igralci[0].ime
        for oseba in Igralci:
            slovar[oseba.ime] = oseba.roka
        slovar["rufanje"] = False
        slovar["talon"] = False
        slovar["zalaganje"] = False
        slovar["polozene"] = False
        slovar["zacetek"] = False
        slovar["krog"] = 0
        slovar["konec"] = False
        slovar["obvezen"] = Igralci[len(Igralci)-1].ime
        slovar["trenutna_igra"] = False
        slovar["izbira"] = False
        slovar["odstranjene"] = []
        slovar["kup"] = []
        slovar["rezultat"] = False
        slovar["tocke"] = 0
        slovar["kralj"] = False
        json.dump(slovar, dat)

def zapis_v_json(atribut, sprememba):
    with open(DAT_IGRA, 'r') as dat:
        trenutni = json.load(dat)
    with open(DAT_IGRA, 'w') as dat:
        trenutni[atribut] = sprememba
        json.dump(trenutni, dat)

def ime_igre(num):
    stevilo = int(num)
    if stevilo == 0:
        return "Nič"
    if stevilo == 1:
        return "Tri"
    if stevilo == 2:
        return "Dva"
    if stevilo == 3:
        return "Ena"
    if stevilo == 4:
        return "Solo tri"
    if stevilo == 5:
        return "Solo dva"
    if stevilo == 6:
        return "Solo ena"

def naslednji_izbira():
    global Trenutni_igralec, izbrana_igra
    indeks = (Igralci.index(Trenutni_igralec) + 1) % (len(Igralci))
    Trenutni_igralec = Igralci[indeks]
    if Trenutni_igralec.ime == Igralci[0].ime:
        if izbrana_igra[1] == 0:
            izbrana_igra[1] = 1
            izbrana_igra[0] = Igralci[len(Igralci)-1]
        rufer = izbrana_igra[0]
        rufer.vrsta_igre = izbrana_igra[1]
        rufer.rufan = True
        if ima_rufanje(izbrana_igra):
            zapis_v_json("rufanje", True)
        else:
            izbor_talona()
        Trenutni_igralec = rufer
    zapis_v_json("trenutna_igra", [izbrana_igra[0].ime, ime_igre(izbrana_igra[1])])
    zapis_v_json("trenutni", Trenutni_igralec.ime)

def izbor_talona():
    if True: #igra_ima_talon():
        delitev = stevilo_zalozenih(izbrana_igra)
        delitev_talona = []
        for k in range(6 // delitev):
            delitev_talona.append(del_talona(delitev, k))
        zapis_v_json("talon", delitev_talona)
    
def dodelitev_talona(izbira):
    print(Trenutni_igralec.roka)
    izbran_talon = del_talona(stevilo_zalozenih(izbrana_igra),int(izbira))
    Trenutni_igralec.doda_karte(izbran_talon)
    print(Trenutni_igralec.roka)
    spremeni_talon(izbrana_igra, izbira)
    zapis_v_json("zalaganje", stevilo_zalozenih(izbrana_igra))
    zapis_v_json("izbira", izbran_talon)

def polozi_karte(karta):
    global Trenutni_igralec
    Trenutni_igralec.roka.remove(karta)
    with open(DAT_IGRA, 'r') as dat:
        podatki = json.load(dat)
        odstranjene = podatki["odstranjene"]
    odstranjene.append(karta)
    zapis_v_json("odstranjene", odstranjene)
    if len(Trenutni_igralec.roka) == ((54 - 6) // len(Igralci)):
        zapis_v_json(Trenutni_igralec.ime, Trenutni_igralec.roka)
        #zapis_v_json("polozene", True)
        Trenutni_igralec = Igralci[len(Igralci)-1]
        zapis_v_json("zacetek", True)
        zacetek_kroga()

def dodaj_napovedi(napovedi):
    global Trenutni_igralec, Napovedi
    Napovedi = napovedi
    Trenutni_igralec = Igralci[len(Igralci)-1] #Spremeni za ostale vrste igre
    preveri_fang()
    zapis_v_json("zacetek", True)
    zacetek_kroga()

def zacetek_kroga():
    global Vrstni_red
    Vrstni_red = vrstni_red(Trenutni_igralec)
    zapis_v_json("trenutni", Trenutni_igralec.ime)
    with open(DAT_IGRA, 'r') as dat:
        podatki = json.load(dat)
        krog = podatki["krog"]
    if krog == ((54 - 6) // len(Igralci)):
        return konec_igre()
    else:
        krog += 1
        zapis_v_json("krog", krog)

def poteza():
    global Trenutni_igralec
    igrane_karte = []
    print(Kup)
    for x in Kup:
        igrane_karte.append(Kup[x])
    print(igrane_karte)
    zapis_v_json("kup", igrane_karte)
    zapis_v_json(Trenutni_igralec.ime, Trenutni_igralec.roka)
    indeks = Vrstni_red.index(Trenutni_igralec)
    if indeks == (len(Igralci) - 1):
        zmagovalec = zmagovalni_igralec()
        zmagovalec.pobere()
        Trenutni_igralec = zmagovalec
        return zacetek_kroga()
    else:
        Trenutni_igralec = Vrstni_red[indeks+1]
        zapis_v_json("trenutni", Trenutni_igralec.ime)

def popravljen_talon(num):
    stevilka = int(num)
    n = int(izbrana_igra[1])
    if n == 1 or n == 4:
        if stevilka == 0 or stevilka == 1 or stevilka == 2:
            return 0
        else:
            return 1
    if n == 2 or n == 5:
        if stevilka == 0 or stevilka == 1:
            return 0
        elif stevilka == 2 or stevilka == 3:
            return 1
        else:
            return 2
    else:
        return stevilka

def igra_se_je_zacela():
    with open(DAT_IGRA, 'r') as dat:
        podatki = json.load(dat)
        zacela = podatki["zacetek"]
    return zacela

def konec_igre():
    global Igralci
    zapis_v_json("konec", True)
    sestevek = 0
    if preveri_valat():
        sestevek = 250 * napovedan_bonus('valat')
    dodeli_talon()
    rezultat = tockovanje()[0]
    tocke = tockovanje()[1]
    if rezultat:
        sestevek += vrednost_igre()
    else:
        sestevek -= vrednost_igre()
    if igra_ima_tocke():
        if rezultat:
            sestevek += (tocke - 35)
        else:
            sestevek -= (35 - tocke)
    sestevek = bonusi(sestevek)
    zapis_v_json("rezultat", rezultat)
    zapis_v_json("tocke", sestevek)
    Igralci = []
