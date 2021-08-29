import model as m

def izbira_igre(prejsnja, igralec):
    izbrana = int(input(f'Katero igro izberes, {igralec}? ')) # Prikaz
    if izbrana == 0:
        return prejsnja
    vrsta_igre = [igralec, izbrana]
    if izbrana in {0, 1, 2, 3} and m.mocnejsa_izbira(prejsnja, vrsta_igre) == vrsta_igre and (izbrana != 1 or m.Igralci.index(igralec) == (len(m.Igralci) - 1)):
        return vrsta_igre
    else:
        print('To ni dovoljen odgovor.') # Prikaz
        return izbira_igre(prejsnja, igralec)

def rufanje_kralja(igra):
    if m.ima_rufanje(igra[1]):
        n = m.karta_v_stevilko(input('V katerem kralju gres igrat?')) # Input
        for oseba in m.Igralci:
            if (22 + n * 8) in oseba.roka:
                return oseba
        return igra[0]
    else:
        return None

def odstrani_karte(igra): # SPREMENI V SPLETNEM VMESNIKU, DOVOLI SAMO LEGALNE IZBIRE IN PAZI DA PRETVORIS IZ KARTE V POZICIJO PRAVILNO IN NAJ ZALOZI KOKR JE TREBA, NE VEDNO 2 SPREMENI KOKR STA SE VCERI Z LUKATOM POGOVARJALA, DEJ TOK INPUTOV KOKR JE SEL IGRAT
    prva = int(input('Polozi prvo karto.'))
    if m.legaln_polog(igra, prva) == True:
        igra[0].vzame_karto(prva)
        igra[0].pobrane.append(prva)
        if m.tip_karte(prva) == "Tarok":
            pass # POKAZI TAROK
    else:
        pass # POSKRBI DA LAHKO SAMO LEGALNE IZBERE
    druga = int(input('Polozi drugo karto.'))
    if m.legaln_polog(igra, druga) == True:
        igra[0].vzame_karto(druga)
        igra[0].pobrane.append(druga)
        if m.tip_karte(druga) == "Tarok":
            pass # POKAZI TAROK
    else:
        pass # POSKRBI DA LAHKO SAMO LEGALNE IZBERE

def igra_taroka(rufer):
    print('USPESEK!!!!!!!')

def prikaz_kart(o=None): # ZACASNA FUNKCIJA
    if o in m.Igralci:
        print(f'{o}:')
        print(o.roka)
    else:
        for x in m.Igralci:
            print(f'{x}:')
            print(x.roka)

def konec_igre(): # PRESTEJ TOCKE, JIH ZAPISI, POKAZI KDO JE ZMAGAL, PELJI NA MAIN SCREEN
    print('USPEH')

def igra_taroka(zacne, krog=1):
    if krog <= (54 - 6) // len(m.Igralci):
        Red = m.vrstni_red(zacne)
        for oseba in Red:
            prikaz_kart(oseba)
            izbira = int(input(f'{oseba}, igraj karto'))
            veljavna = False
            while veljavna != True:
                if Red.index(oseba) == 0:
                    veljavna = True
                    prva_karta = izbira
                    oseba.igra(izbira)
                    print(f'{oseba} je igral/a: {izbira}')
                elif m.legalna_izbira(prva_karta, oseba, izbira):
                    veljavna = True
                    oseba.igra(izbira)
                    print(f'{oseba} je igral/a: {izbira}')
                else:
                    print('To ni veljavna poteza')
        zmagovalec = m.zmagovalni_igralec()
        pobrane = ''
        ind = 0
        for o in m.Igralci:
            pobrane += str(m.Kup[o])
            ind += 1
            if ind < len(m.Igralci):
                pobrane += ', '
        zmagovalec.pobere()
        print(f'zmagal/a je {zmagovalec}, pobral/a je {pobrane}')
        return igra_taroka(zmagovalec, krog + 1)
    else:
        return konec_igre()


def zacetek():
    m.delitev_kart()
    prikaz_kart() # PRIKAZI KARTE
    igra = [m.Igralci[0],0]
    for oseba in m.Igralci:
        igra = izbira_igre(igra, oseba)
    rufer = igra[0]
    # rufer.rufan = True
    porufan = rufanje_kralja(igra)
    if porufan != None:
        porufan.rufan = True
    moznosti = m.prikaz_talona(igra)
    print(moznosti) # Prikaz
    izbira_talona = input('Pred tabo je talon, izberi karte.') # Input
    rufer.doda_karte(m.del_talona(m.delitev_talona(igra),int(izbira_talona) - 1))
    m.spremeni_talon(igra, izbira_talona)
    odstrani_karte(igra)
    # Napovedi()
    return igra_taroka(rufer)
    


Andrej = m.Igralec("Andrej")
Maja = m.Igralec("Maja")
Anze = m.Igralec("Anze")
Mitja = m.Igralec("Mitja")