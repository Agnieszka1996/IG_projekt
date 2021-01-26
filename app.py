from flask import Flask, render_template, request, redirect, url_for
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
    print(gra)
    print(gra.gracze)
    karty_gracza_1 = gra.gracze[0].karty_gracza
    karty_gracza_2 = gra.gracze[1].karty_gracza
    form = WybierzKarte()
    wartownik = gra.wartownik
    print(form.validate_on_submit())
    print(form.potwierdz.data,form.karta.data)
    # choice_form = ChooseCard(gra.gracze[gra.turn].karty_gracza)
    if form.validate_on_submit():
        gra.start_gry(form.karta.data)
        if gra.koniec_gry:
            return render_template("koniec_gry.jinja2", wygrany_gracz = gra.turn, gracze= ['Agnieszka', 'Pawel'])
        return redirect(url_for("gra"))
        # return redirect(url_for("koniec_gry"))
    return render_template("gra.jinja2", karty_gracza_1=karty_gracza_1, karty_gracza_2=karty_gracza_2, wartownik = wartownik, form=form)

@app.route('/pobierz_karte/<str>')
def pobierz_karte(self, karta):
    karty_gracza_1 = gra.gracze[0].karty_gracza
    karty_gracza_2 = gra.gracze[1].karty_gracza
    form = WybierzKarte()
    self.karty_gracza.append(karta)
    return render_template("gra.jinja2", karty_gracza_1=karty_gracza_1, karty_gracza_2=karty_gracza_2, form=form)

if __name__ == "__main__":
    app.debug =True
    app.run(host="0.0.0.0", port=5000, debug=True)



#brakuje nam:
#TODO:
# sprawdznie czy karta moze poleciec na srodek
# gra z komputerem # losowa karta z reki, 2. wybor trybu gry
#