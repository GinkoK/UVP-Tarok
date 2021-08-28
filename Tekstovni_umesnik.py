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

def odstrani_karte(igra): # SPREMENI V SPLETNEM VMESNIKU, DOVOLI SAMO LEGALNE IZBIRE IN PAZI DA PRETVORIS IZ KARTE V POZICIJO PRAVILNO
    prva = int(input('Polozi prvo karto.'))
    if m.legaln_polog(igra, prva) == True:
        igra[0].roka.remove(prva)
        igra[0].pobrane.append(prva)
        if m.tip_karte(prva) == "Tarok":
            pass # POKAZI TAROK
    else:
        pass # POSKRBI DA LAHKO SAMO LEGALNE IZBERE
    druga = int(input('Polozi drugo karto.'))
    if m.legaln_polog(igra, druga) == True:
        igra[0].roka.remove(druga)
        igra[0].pobrane.append(druga)
        if m.tip_karte(druga) == "Tarok":
            pass # POKAZI TAROK
    else:
        pass # POSKRBI DA LAHKO SAMO LEGALNE IZBERE

def igra_taroka(rufer):
    print('USPESEK!!!!!!!')

def prikaz_kart(): # ZACASNA FUNKCIJA
    for x in m.Igralci:
        print(f'{x}:')
        print(x.roka)

def zacetek():
    m.delitev_kart()
    prikaz_kart() # PRIKAZI KARTE
    igra = [m.Igralci[0],0]
    for oseba in m.Igralci:
        igra = izbira_igre(igra, oseba)
    rufer = igra[0]
    porufan = rufanje_kralja(igra)
    porufan.rufan = True
    moznosti = m.prikaz_talona(igra)
    print(moznosti) # Prikaz
    izbira_talona = input('Pred tabo je talon, izberi karte.') # Input
    rufer.doda_karte(m.del_talona(m.delitev_talona(igra),int(izbira_talona) - 1))
    m.spremeni_talon(igra, izbira_talona)
    odstrani_karte(igra)
    igra_taroka(rufer)
    


Andrej = m.Igralec("Andrej")
Maja = m.Igralec("Maja")
Anze = m.Igralec("Anze")
Mitja = m.Igralec("Mitja")