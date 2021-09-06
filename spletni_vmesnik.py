import bottle
import model as m
import json

DATOTEKA = "podatki.json"
PISKOTEK_UPORABNISKO_IME = "uporabnisko_ime"
SKRIVNOST = "Zakaj je tvoja palacinka slana?"

def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie(
        PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST
    )
    if uporabnisko_ime:
        return m.Igralec.preberi_iz_datoteke(uporabnisko_ime)

#Andrej = m.Igralec("Adrej", 1)
#Maja = m.Igralec("Maja", 1)
#Anze = m.Igralec("Anze", 1)
#Mitja = m.Igralec("Mitja", 1)

#m.Igralci.append(Andrej)
#m.Igralci.append(Maja)
#m.Igralci.append(Anze)
#m.Igralci.append(Mitja)



def zacetek_igre():
	m.resetiraj()
	m.delitev_kart()
	m.zapis_kart()
	m.Trenutni_igralec = m.Igralci[0]

    		


@bottle.get("/")
def zacetna_stran():
	return bottle.template("osnovni_zaslon.html", uporabnik=trenutni_uporabnik())

@bottle.get("/prijava/")
def prijava():
	return bottle.template("prijava.html", uporabnik=trenutni_uporabnik(), napaka = None)

@bottle.post("/prijava/")
def prijava_post():
	uporabnikso_ime = bottle.request.forms.getunicode("uporabnisko_ime")
	geslo = bottle.request.forms.getunicode("geslo")
	if not uporabnikso_ime:
		return bottle.template("prijava.html", napaka="Vnesi uporabniško ime!", uporabnik=trenutni_uporabnik())
	if not geslo:
		return bottle.template("prijava.html", napaka="Vnesi geslo!", uporabnik=trenutni_uporabnik())
	try:
		m.Igralec.prijava(uporabnikso_ime, geslo)
		bottle.response.set_cookie(
			PISKOTEK_UPORABNISKO_IME, uporabnikso_ime, path="/", secret=SKRIVNOST
		)
		bottle.redirect("/")
	except ValueError as e:
		return bottle.template(
			"prijava.html", napaka=e.args[0], uporabnik=trenutni_uporabnik()
		)

@bottle.get("/registracija/")
def registracija():
	return bottle.template("registracija.html", uporabnik=trenutni_uporabnik(), napaka = None)

@bottle.post("/registracija/")
def registracija_post():
	uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
	geslo_1 = bottle.request.forms.getunicode("geslo1")
	geslo_2 = bottle.request.forms.getunicode("geslo2")
	if not uporabnisko_ime:
		return bottle.template("registracija.html", napaka="Vnesi uporabniško ime!", uporabnik=trenutni_uporabnik())
	if not geslo_1:
		return bottle.template("registracija.html", napaka="Vnesi geslo!", uporabnik=trenutni_uporabnik())
	if geslo_1 != geslo_2:
		return bottle.template("registracija.html", napaka="Gesli se ne ujemata!", uporabnik=trenutni_uporabnik())
	try:
		m.Igralec.registracija(uporabnisko_ime, geslo_1)
		bottle.response.set_cookie(PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST)
		bottle.redirect("/")
	except ValueError as e:
		return bottle.template("registracija.html", napaka=e.args[0], uporabnik=trenutni_uporabnik())

@bottle.get("/odjava/")
def odjava():
	bottle.response.delete_cookie(PISKOTEK_UPORABNISKO_IME, path="/")
	bottle.redirect("/")

@bottle.get("/tocke/")
def tocke():
	slovar_tock = {}
	with open(DATOTEKA, 'r') as dat:
		slovar_vseh = json.load(dat)
	for x in slovar_vseh:
		slovar_tock[x] = slovar_vseh[x]["tocke"]
	return bottle.template("tocke.html", uporabnik=trenutni_uporabnik().ime, tocke = slovar_tock)

@bottle.get("/potek/")
def potek():
	if len(m.Igralci) == 4 and m.Trenutni_igralec == None:		
		zacetek_igre()
	return bottle.template("igra.html", uporabnik=trenutni_uporabnik())


@bottle.get("/igra/")
def igra():
	m.Igralci.append(trenutni_uporabnik())
	m.shrani_stevilo()
	bottle.redirect("/potek/")
	

@bottle.get("/potek/<ime_dat:path>")
def server_static(ime_dat):
	return bottle.static_file(ime_dat, root='')

@bottle.post("/potek/")
def igranje_kart():
	if m.Trenutni_igralec.ime == trenutni_uporabnik().ime:
		if bottle.request.forms.get('igra') != None:
			izbira = int(bottle.request.forms['igra'])
			if m.izbrana_igra == []:
				m.izbrana_igra = [m.Trenutni_igralec, izbira]
				m.naslednji_izbira()
			elif izbira != 0:
				if m.mocnejsa_izbira(m.izbrana_igra, [m.Trenutni_igralec, izbira]):
					m.izbrana_igra = [m.Trenutni_igralec, izbira]
					m.naslednji_izbira()
			else:
				m.naslednji_izbira()
			bottle.redirect("/potek/")

		if bottle.request.forms.get('talon') != None:
			izb_talon = m.popravljen_talon(bottle.request.forms['talon'])
			print(izb_talon)
			m.dodelitev_talona(izb_talon)

		if bottle.request.forms.get('kralj') != None:
			izb_kralj = int(bottle.request.forms['kralj'])
			konig = (22 + izb_kralj * 8)
			m.Trenutni_igralec.kralj = konig
			for oseba in m.Igralci:
				if konig in oseba.roka:
					oseba.kralj = konig
					oseba.rufan = True
			m.zapis_v_json("kralj", m.tip_karte(konig))
			m.izbor_talona()

		if bottle.request.forms.get('karta') != None:
			karta = int(bottle.request.forms['karta'])
			print(karta)
			if m.igra_se_je_zacela():
				if m.Vrstni_red.index(m.Trenutni_igralec) == 0:
					m.Trenutni_igralec.igra(karta)
					m.Prva = karta
					m.poteza()
					bottle.redirect("/potek/")
				elif m.legalna_izbira(m.Prva, m.Trenutni_igralec, karta):
					m.Trenutni_igralec.igra(karta)
					m.poteza()
					bottle.redirect("/potek/")
				else:
					pass #error
			else:
				if m.legaln_polog(m.izbrana_igra, karta):
					m.polozi_karte(karta)
					bottle.redirect("/potek/")
				else:
					#error
					pass
		bottle.redirect("/potek/")
	#else:
		#pass #nisi na vrsti

bottle.run(debug=True, reloader=True) # Izklopi debug in reloader na koncu

