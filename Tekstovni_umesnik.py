import model as m

def izbira_igre(prejsnja, igralec):
    izbrana = int(input(f'Katero igro izberes, {igralec}? '))
    if izbrana == 0:
        return prejsnja
    vrsta_igre = [igralec, izbrana]
    if izbrana in {0, 1, 2, 3} and m.mocnejsa_izbira(prejsnja, vrsta_igre) == vrsta_igre and (izbrana != 1 or m.Igralci.index(igralec) == (len(m.Igralci) - 1)):
        return vrsta_igre
    else:
        print('To ni dovoljen odgovor.')
        return izbira_igre(prejsnja, igralec)

def prikaz_talona(igra):
    presek_talona = m.delitev_talona(igra[1])
    prikaz_talona = ''
    for k in range(6 // presek_talona):
        por = m.del_talona(presek_talona, k)
        for j in range(presek_talona):
            prikaz_talona += str(por[j])
            if j != (presek_talona - 1):
                prikaz_talona += ', '
        if k != ((6 // presek_talona) -1):
            prikaz_talona += ';   '
    return prikaz_talona

def zacetek():
    stevilo_igralcev = len(m.Igralci)
    m.delitev_kart()
    igra = [m.Igralci[0],0]
    for oseba in m.Igralci:
        igra = izbira_igre(igra, oseba)
    moznosti = prikaz_talona(igra)
    print(moznosti)
    izbira_talona = input('Pred tabo je talon, izberi karte.')
    


Andrej = m.Igralec("Andrej")
Maja = m.Igralec("Maja")
Anze = m.Igralec("Anze")
Mitja = m.Igralec("Mitja")