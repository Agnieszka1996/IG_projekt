from flask import Flask, render_template, request, redirect, url_for, flash
from form import *
from game import Game, Player
from collections import OrderedDict

app = Flask(__name__)
app.secret_key = 'asdfasdfasdfaskjdlhflwgejnlhus'

@app.route("/")
def wybierz_tryb_gry():
    return render_template("index.html")



@app.route("/start_gra/<tryb_gry>", methods=['POST', "GET"])
def start_gry(tryb_gry):

   global gra
   gra = Game()
   gra.init_game()
   # gra.start_gry()
   if tryb_gry != 'gracz':
       return redirect(
           url_for('gra_z_cpu'))
   return redirect(
      url_for('gra'))


@app.route("/gra", methods=['POST', "GET"])
def gra():
    global gra
    karty_gracza = [gra.gracze[0].karty_gracza, gra.gracze[1].karty_gracza]
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
            return render_template("koniec_gry.html", wygrany_gracz = gra.turn, gracze= ['Agnieszka', 'Pawel'])
        return redirect(url_for("gra"))
        # return redirect(url_for("koniec_gry"))
    return render_template("gra.html", karty_gracza = karty_gracza, wartownik = wartownik, form=form, ruch_gracza = gra.turn, gracze= ['Agnieszka', 'Pawel'], tryb_gry='gracz', ulozone_slowo = ulozone_slowo)

@app.route("/gra_z_cpu", methods=['POST', "GET"])
def gra_z_cpu():
    global gra
    print(gra.wartownik_przed_ruchem, 'przed ruchem', 'po ruchu', gra.wartownik)

    if gra.wartownik != gra.wartownik_przed_ruchem:
        print('nasze nowe slowo to:', gra.wartownik_przed_ruchem+gra.wartownik)

    if gra.turn == 0:
        gra.start_gry(tryb_gry='cpu')
        print("karty cpu: ",gra.gracze[0].karty_gracza)
        redirect(url_for('gra_z_cpu'))


    #kto ma ruch
    # jak cpu
    #to ma sie ruszyc
    # i wygenerowac forme
    # a jak my to to co  nizej
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
        #gra.start_gry(tryb_gry='cpu')
        print('here')
        if gra.koniec_gry:
            return render_template("koniec_gry.html", wygrany_gracz = gra.turn, gracze= ['Agnieszka', 'Pawel'])
        print('redi')
        return redirect(url_for("gra_z_cpu"))
        # return redirect(url_for("koniec_gry"))
    return render_template("gra.html", karty_gracza = karty_gracza, wartownik = wartownik, form=form, ruch_gracza = gra.turn, gracze= ['Agnieszka', 'Pawel'], tryb_gry='cpu', ulozone_slowo = ulozone_slowo)

@app.route('/wyloz_karte/<tryb_gry>/<karta>')
def wyloz_karte(tryb_gry, karta):
    global gra
    print(gra.turn)
    if karta not in gra.gracze[gra.turn].karty_gracza:
        flash(f"{gra.imiona_graczy[gra.turn]}, W Twoich kartach nie ma takiej sylaby i musiales dobrac karte za to!")
    try:
        gra.ruch_gracza(karta)
        gra.zmiana_gracza()
        if tryb_gry == 'cpu':
            return redirect(url_for('gra_z_cpu'))
        return redirect(url_for('gra'))
    except AssertionError as e:
        return redirect(url_for('pobierz_karte'))


@app.route('/pobierz_karte')
def pobierz_karte():
    # uzycie globalnej zmiennej gra
    # uzyc naszego obiektu:
    # w zaleznosci kto ma ruch, to dobiera karte
    # i na koncu w return daje redirect(url_for('gra'))
    global gra
    print(gra.turn)
    gra.ruch_gracza()
    gra.zmiana_gracza()
    return redirect(url_for('gra'))

if __name__ == "__main__":
    app.debug =True
    app.run(host="0.0.0.0", port=5000, debug=True)



#brakuje nam:
#TODO:
# sprawdznie czy karta moze poleciec na srodek
# gra z komputerem # losowa karta z reki, 2. wybor trybu gry
#