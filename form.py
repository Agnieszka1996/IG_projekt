from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class WybierzKarte(FlaskForm):
    """wybor karty """

    karta = StringField("Karta")
    potwierdz = SubmitField("potweirdz wybor")