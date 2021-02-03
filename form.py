from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class WybierzKarte(FlaskForm):
    """wybor karty """

    karta = StringField("Karta")
    potwierdz = SubmitField("Potwierdź wybór")


class ImieGracza(FlaskForm):
    """ nadanie imion graczowi """
    gracz = StringField("Karta")
    potwierdz_vs_cpu = SubmitField("Potwierdź wybór")


class ImionaGraczy(FlaskForm):
    """nadanie imion gracza"""
    gracz_1 = StringField("Karta")
    gracz_2 = StringField("Karta")
    potwierdz_vs_gracz = SubmitField("Potwierdź wybór")