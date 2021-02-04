from flask import Flask, render_template, request, redirect, url_for, flash
from form import *
from game import *
# from game import Game, Player
from collections import OrderedDict

app = Flask(__name__)
app.secret_key = 'asdfasdfasdfaskjdlhflwgejnlhus'

@app.route("/")
def wybierz_tryb_gry():
    return render_template("index.html")

@app.route("/formularz/<tryb_gry>", methods=['POST', "GET"])
def wypelnij_formularz(tryb_gry):
    global gracz_1
    global gracz_2
    form_cpu = ImieGracza()
    form_gracze = ImionaGraczy()
    if form_gracze.validate_on_submit() and form_gracze.potwierdz_vs_gracz.data:
        gracz_1 = form_gracze.gracz_1.data
        gracz_2 = form_gracze.gracz_2.data
        return redirect(url_for('start_gry', tryb_gry='gracze'))
    if form_cpu.validate_on_submit():
        gracz_1 = form_cpu.gracz.data
        gracz_2 = None
        return redirect(url_for('start_gry', tryb_gry='cpu'))
    return render_template("formularz.html", form_cpu = form_cpu, form_gracze = form_gracze, tryb_gry=tryb_gry)

@app.route("/start_gra/<tryb_gry>", methods=['POST', "GET"])
def start_gry(tryb_gry):

   global gra, gracz_1,gracz_2
   if gracz_2:
       gra = Game(gracz_1=gracz_1, gracz_2= gracz_2, tryb_gry = tryb_gry)
   else:
       gra = Game(gracz_1=gracz_1, tryb_gry = tryb_gry)
   gra.init_game()

   if tryb_gry != 'gracze':
       return redirect(
           url_for('gra_z_cpu'))
   return redirect(
      url_for('gra'))


@app.route("/gra", methods=['POST', "GET"])
def gra():
    global gra
    if not gra or gra.tryb_gry != 'gracze':
        return redirect(url_for('wybierz_tryb_gry'))
    karty_gracza = [gra.gracze[0].karty_gracza, gra.gracze[1].karty_gracza]
    punkty = gra.gracze[gra.turn].punkty
    form = WybierzKarte()
    wartownik = gra.wartownik
    print(gra.wartownik_przed_ruchem, 'przed ruchem', 'po ruchu', gra.wartownik)
    if gra.wartownik != gra.wartownik_przed_ruchem:
        ulozone_slowo = gra.wartownik_przed_ruchem + gra.wartownik
        print('nasze nowe slowo to:', gra.wartownik_przed_ruchem+gra.wartownik)
    else:
        ulozone_slowo = None


    # choice_form = ChooseCard(gra.gracze[gra.turn].karty_gracza)
    if form.validate_on_submit():
        gra.start_gry(form.karta.data)
        if gra.koniec_gry:
            return render_template("koniec_gry.html", wygrany_gracz = gra.turn, gracze = gra.imiona_graczy)
        return redirect(url_for("gra"))
    return render_template("gra.html", karty_gracza = karty_gracza, wartownik = wartownik, form=form, ruch_gracza = gra.turn, gracze = gra.imiona_graczy, tryb_gry=gra.tryb_gry, ulozone_slowo = ulozone_slowo, punkty = punkty, licza_kart_na_stosie = len(gra.karty))

@app.route("/gra_z_cpu", methods=['POST', "GET"])
def gra_z_cpu():
    global gra

    if not gra or gra.tryb_gry != 'cpu':
        return redirect(url_for('wybierz_tryb_gry'))

    if gra.wartownik != gra.wartownik_przed_ruchem:
        print('nasze nowe slowo to:', gra.wartownik_przed_ruchem+gra.wartownik)

    if gra.turn == 0:
        gra.start_gry(tryb_gry='cpu')
        gra.czy_zakonczyc_gre()
        if gra.koniec_gry:
            return redirect(url_for('zakoncz_gre'))
        print("karty cpu: ", gra.gracze[0].karty_gracza)
        return redirect(url_for('gra_z_cpu'))

    punkty = gra.gracze[gra.turn].punkty
    print(gra.wartownik_przed_ruchem, 'przed ruchem', 'po ruchu', gra.wartownik)
    karty_gracza = [gra.gracze[0].karty_gracza, gra.gracze[1].karty_gracza]
    form = WybierzKarte()
    wartownik = gra.wartownik
    if gra.wartownik != gra.wartownik_przed_ruchem:
        ulozone_slowo = gra.wartownik_przed_ruchem + gra.wartownik
        print('nasze nowe slowo to:', gra.wartownik_przed_ruchem+gra.wartownik)
    else:
        ulozone_slowo = None
    # choice_form = ChooseCard(gra.gracze[gra.turn].karty_gracza)
    if form.validate_on_submit():
        gra.start_gry(form.karta.data, tryb_gry='cpu')
        if gra.koniec_gry:
            return render_template("koniec_gry.html", wygrany_gracz = gra.turn, gracze = gra.imiona_graczy)
        return redirect(url_for("gra_z_cpu"))
    return render_template("gra.html", karty_gracza = karty_gracza, wartownik = wartownik, form=form, ruch_gracza = gra.turn, gracze = gra.imiona_graczy, tryb_gry='cpu', ulozone_slowo = ulozone_slowo, punkty = punkty, punkty_cpu = gra.gracze[0].punkty, licza_kart_na_stosie = len(gra.karty))

@app.route('/wyloz_karte/<tryb_gry>/<karta>')
def wyloz_karte(tryb_gry, karta):
    global gra
    if karta not in gra.gracze[gra.turn].karty_gracza:
        flash('W Twoich kartach nie ma takiej sylaby – za karę dobierasz kartę!')
        # flash(f'{gra.imiona_graczy[gra.turn]}, w Twoich kartach nie ma takiej sylaby – za karę dobierasz kartę!')
    try:
        gra.ruch_gracza(karta)
        gra.czy_zakonczyc_gre()
        if gra.koniec_gry:
            return redirect(url_for('zakoncz_gre'))

        gra.zmiana_gracza()
        if tryb_gry == 'cpu':
            return redirect(url_for('gra_z_cpu'))
        return redirect(url_for('gra'))
    except AssertionError as e:
        return redirect(url_for('pobierz_karte', tryb_gry=tryb_gry))


@app.route('/pobierz_karte/<tryb_gry>')
def pobierz_karte(tryb_gry):
    global gra
    gra.ruch_gracza()
    gra.zmiana_gracza()
    if tryb_gry != 'gracze':
        return redirect(
            url_for('gra_z_cpu'))
    return redirect(
        url_for('gra'))

@app.route('/koniec_gry')
def zakoncz_gre():
    global gra
    wygrany = gra.imiona_graczy[gra.turn],
    punkty_wygranego = gra.gracze[gra.turn].punkty,
    przegrany = gra.imiona_graczy[(gra.turn + 1) % 2],
    punkty_przegranego = gra.gracze[(gra.turn + 1) % 2].punkty,
    koniec_gry = gra.koniec_gry
    gra = None
    return render_template('koniec_gry.html', wygrany = wygrany[0], punkty_wygranego = punkty_wygranego[0], przegrany = przegrany[0], punkty_przegranego = punkty_przegranego[0],
                               koniec_gry = koniec_gry)

if __name__ == "__main__":
    app.debug =True
    app.run(host="0.0.0.0", port=5121, debug=True)