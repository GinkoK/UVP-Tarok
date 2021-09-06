import model as m

def izbira_igre(prejsnja, igralec):
    izbrana = int(input(f'Katero igro izberes, {igralec}? ')) # Prikaz
    if izbrana == 0:
        return prejsnja
    vrsta_igre = [igralec, izbrana]
    if m.mocnejsa_izbira(prejsnja, vrsta_igre) == vrsta_igre and (izbrana != 1 or m.Igralci.index(igralec) == (len(m.Igralci) - 1)):
        return vrsta_igre
    else:
        print('To ni dovoljen odgovor.') # Prikaz
        return izbira_igre(prejsnja, igralec)






def rufanje_kralja(igra):
    if m.ima_rufanje(igra):
        n = m.karta_v_stevilko(input('V katerem kralju gres igrat?')) # Input
        kralj = (22 + n * 8)
        igra[0].kralj = kralj
        for oseba in m.Igralci:
            if kralj in oseba.roka:
                oseba.kralj = kralj
                return oseba
        return igra[0]
    else:
        return None





def odstrani_karte(igra): # SPREMENI V SPLETNEM VMESNIKU, DOVOLI SAMO LEGALNE IZBIRE IN PAZI DA PRETVORIS IZ KARTE V POZICIJO PRAVILNO
    for x in range(m.stevilo_zalozenih(igra)):
        if x == 0:
            print('Polozi karte')
        prva = int(input())
        if m.legaln_polog(igra, prva) == True:
            igra[0].vzame_karto(prva)
            igra[0].pobrane.append(prva)
            if m.tip_karte(prva) == "Tarok":
                pass # POKAZI TAROK
        else:
            pass # POSKRBI DA LAHKO SAMO LEGALNE IZBERE







def prikaz_kart(o=None): # ZACASNA FUNKCIJA
    if o in m.Igralci:
        print(f'{o}:')
        print(o.roka)
    else:
        for x in m.Igralci:
            print(f'{x}:')
            print(x.roka)




def konec_igre(): # PRESTEJ TOCKE, JIH ZAPISI, POKAZI KDO JE ZMAGAL, PELJI NA MAIN SCREEN
    sestevek = 0
    if m.preveri_valat():
        sestevek = 250 * m.napovedan_bonus('valat')
    m.dodeli_talon()
    rezultat = m.tocke()[0]
    tocke = m.tocke()[1]
    if rezultat:
        sestevek += m.vrednost_igre()
    else:
        sestevek -= m.vrednost_igre()
    if m.igra_ima_tocke():
        if rezultat:
            sestevek += (tocke - 35)
        else:
            sestevek -= (35 - tocke)
    sestevek = m.bonusi(sestevek)
    # Skisfang in Mondfang direkt odstej
    return sestevek
    # Reset
    # Display tock in zmage
    # Zapis v datoteko
    # Main menu






def igra_taroka(zacne, krog=1):
    if krog <= (54 - 6) // len(m.Igralci):
        Red = m.vrstni_red(zacne)
        for oseba in Red:
            prikaz_kart(oseba)
            veljavna = False
            i = 0 #ZA POSKUS SAMO
            while veljavna != True:
                # izbira = int(input(f'{oseba}, igraj karto'))
                izbira = oseba.roka[i] #ZA POSKUS SAMO
                i += 1 #ZA POSKUS SAMO
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
        if krog == (54 - 6) // len(m.Igralci):
            if 1 in m.Kup:
                zmagovalec.pobran_pagat = True
            kralj = 0
            for oseba in m.Igralci:
                if oseba.kralj != 0:
                    kralj = oseba.kralj
            if kralj in m.Kup:
                zmagovalec.pobran_kralj = True
        zmagovalec.pobere()
        print(f'zmagal/a je {zmagovalec}, pobral/a je {pobrane}')
        return igra_taroka(zmagovalec, krog + 1)
    else:
        return konec_igre()


def zacetek():
    # Resetiraj vse
    m.delitev_kart()
    prikaz_kart() # PRIKAZI KARTE
    igra = [m.Igralci[0],0]
    for oseba in m.Igralci:
        igra = izbira_igre(igra, oseba)
    rufer = igra[0]
    rufer.vrsta_igre = igra[1]
    rufer.rufan = True
    porufan = rufanje_kralja(igra)
    if porufan != None:
        porufan.rufan = True

    if m.igra_ima_talon(igra):
        moznosti = m.prikaz_talona(igra)
        print(moznosti) # Prikaz
        izbira_talona = input('Pred tabo je talon, izberi karte.') # Input
        rufer.doda_karte(m.del_talona(m.stevilo_zalozenih(igra),int(izbira_talona) - 1))
        m.spremeni_talon(igra, izbira_talona)
        odstrani_karte(igra)
        # Napovedi()
    m.preveri_fang()
    return igra_taroka(rufer)
    


Andrej = m.Igralec("Andrej")
Maja = m.Igralec("Maja")
Anze = m.Igralec("Anze")
Mitja = m.Igralec("Mitja")