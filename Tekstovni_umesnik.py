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



def zacetek():
    stevilo = len(m.Igralci)
    m.delitev_kart()
    igra = [m.Igralci[0],0]
    for oseba in m.Igralci:
        igra = izbira_igre(igra, oseba)
    return igra

Andrej = m.Igralec("Andrej")
Maja = m.Igralec("Maja")
Anze = m.Igralec("Anze")
Mitja = m.Igralec("Mitja")