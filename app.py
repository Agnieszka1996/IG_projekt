from flask import Flask, render_template, request, redirect, url_for
from form import *
from game import Game, Player
from collections import OrderedDict

app = Flask(__name__)
app.secret_key = 'asdfasdfasdfaskjdlhflwgejnlhus'

@app.route("/start_gra", methods=['POST', "GET"])
def start_gry():

   global gra
   gra = ''
   gra = Game()
   gra.start_gry()
   return redirect(
      url_for('gra'))


@app.route("/gra", methods=['POST', "GET"])
def gra():

   karty_gracza = ['BA', 'ka', 'wa', 'se']
   karty_gracza = gra.gracze[gra.turn].karty_gracza
   form = WybierzKarte()
   print(form.validate_on_submit())
   if form.validate_on_submit():
      return f"{form.karta.data}"
   return render_template("gra.html", karty_gracza=karty_gracza, form=form)

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000, debug=True)



#brakuje nam:
#TODO:
# sprawdznie czy karta moze poleciec na srodek
# gra z komputerem
# koniec gry, startowanie od nowa
# forma z lista wybieralna
# forma z dzialajacym POST