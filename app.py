from flask import Flask, render_template, request, redirect, url_for, flash
from form import *
from game import Game, Player
from collections import OrderedDict

app = Flask(__name__)
app.secret_key = 'asdfasdfasdfaskjdlhflwgejnlhus'

@app.route("/start_gra", methods=['POST', "GET"])

# global lista_slow
# # lista_slow = wczytaj_slowa



def start_gry():

   global gra
   gra = Game()
   gra.init_game()
   # gra.start_gry()
   return redirect(
      url_for('gra'))


@app.route("/gra", methods=['POST', "GET"])
def gra():
    global gra
    karty_gracza = [gra.gracze[0].karty_gracza, gra.gracze[1].karty_gracza]
    form = WybierzKarte()
    wartownik = gra.wartownik
    # choice_form = ChooseCard(gra.gracze[gra.turn].karty_gracza)
    if form.validate_on_submit():
        gra.start_gry(form.karta.data)
        if gra.koniec_gry:
            return render_template("koniec_gry.html", wygrany_gracz = gra.turn, gracze= ['Agnieszka', 'Pawel'])
        return redirect(url_for("gra"))
        # return redirect(url_for("koniec_gry"))
    return render_template("gra.html", karty_gracza = karty_gracza, wartownik = wartownik, form=form, ruch_gracza = gra.turn, gracze= ['Agnieszka', 'Pawel'])

@app.route('/wyloz_karte/<karta>')
def wyloz_karte(karta):
    global gra
    print(gra.turn)
    if karta not in gra.gracze[gra.turn].karty_gracza:
        flash(f"{gra.imiona_graczy[gra.turn]}, W Twoich kartach nie ma takiej sylaby i musiales dobrac karte za to!")
    try:
        gra.ruch_gracza(karta)
        gra.zmiana_gracza()
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