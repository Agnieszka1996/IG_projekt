import random
from slownik import slownik_

class Game:
    # jakie atrybuty przyjmuje klasa
    # i jakie metody sa mozliwe

    def __init__(self, gracz_1, gracz_2='komputer', tryb_gry='gracze'):
        self.karty = ['by', 'ko', 'pu', 'le', 'na', 'py', 'ma', 'gi', 'ki', 'sza', 'li', 'fa', 'my', 'że', 'cza',
                      'tka', 'mi', 'nie', 'ni', 'cha', 'wo', 'la', 'ka', 'lu', 'ga', 'mu', 'sy', 'pa', 'ty', 'wy',
                      'ry', 'da', 'to', 'ra', 'fu', 'dy', 'chy', 'ru', 'ku', 'wa', 'ta', 'ny', 'po', 'ła',
                      'do', 'ba', 'no', 'sa']
        # self.karty=  ['by', 'ko', 'pu', 'le', 'na', 'py', 'ma', 'gi', 'ki', 'sza', 'li', 'fa', 'my', 'że', 'cza']
        self.karty_gracza = 6
        self.turn = 1
        self.wartownik = ''
        self.wartownik_przed_ruchem = ''
        self.gracze = []
        self.koniec_gry = None
        self.slownik = slownik_
        self.imiona_graczy = [gracz_2, gracz_1]
        self.tryb_gry = tryb_gry

    def wybierz_tryb_gry(self, value):
        self.tryb_gry = value

    def __str__(self):
        return f" {self.karty}"

    def init_game(self, tryb_gry='cpu'):
        random.shuffle(self.karty)
        self.wartownik = self.karty[-1]
        self.karty.pop()
        self.lista_graczy = self.rozdaj_karty()
        self.wartownik_przed_ruchem = self.wartownik

    def start_gry(self, sylaba=None, tryb_gry='gracz'):
        self.ruch(sylaba, tryb_gry)
        if self.czy_zakonczyc_gre():
            return True
        self.zmiana_gracza()


    def ruch(self, sylaba=None,  tryb_gry='gracz'):
        if tryb_gry != 'gracz':
            if self.turn == 0:
                self.ruch_cpu() # losowe ruchy z tych kart co ma w rece
        else:
            if self.turn == 0:
                self.ruch_gracza(sylaba)
        if self.turn == 1:
            self.ruch_gracza(sylaba)

    def sprawdz_poprawnosc_slowa(self, wybrana_karta):
        if len(self.wartownik + wybrana_karta) >= 4:
            return True
        else:
            return False

    def sprawdzanie_slowa_sjp(self, wybrana_karta):
        sprawdzane_slowo = self.wartownik + wybrana_karta
        print(sprawdzane_slowo)
        if sprawdzane_slowo in self.slownik:
            self.dobre_slowo = sprawdzane_slowo
            return True
        else:
            return False


    def ruch_gracza(self, sylaba=None):
        print(self.gracze)
        print(self.gracze[self.turn].karty_gracza)
        # sylaba = input('wybierz karte ktora chcesz zagrac')
        if sylaba:
            wybrana_karta = self.gracze[self.turn].wyloz_karte(
                sylaba)  # id albo pelna wartosc zwraca(return) wartosc karty np 'ba'
            self.wartownik_przed_ruchem = self.wartownik
            if self.sprawdzanie_slowa_sjp(wybrana_karta):
                self.wartownik = wybrana_karta
                self.gracze[self.turn].odrzuc_karte(wybrana_karta)
                self.gracze[self.turn].punkty += 1
            else:
                self.wyciagnij_karte()
        else:
            self.wyciagnij_karte()

    def zmiana_gracza(self):
        self.turn = (self.turn + 1) % 2

    def ruch_cpu(self):
        print(self.gracze)
        print(self.gracze[self.turn].karty_gracza)
        karty_gracza = self.gracze[self.turn].karty_gracza[:]
        karty_gracza.append('pass')
        print(karty_gracza)
        losuj = random.choice(karty_gracza)
        if losuj == 'pass':
            sylaba = None
        else:
            sylaba = losuj

        print(self.gracze)
        print(self.gracze[self.turn].karty_gracza)
        # sylaba = input('wybierz karte ktora chcesz zagrac')
        if sylaba:
            wybrana_karta = self.gracze[self.turn].wyloz_karte(
                sylaba)  # id albo pelna wartosc zwraca(return) wartosc karty np 'ba'
            self.wartownik_przed_ruchem = self.wartownik
            if self.sprawdzanie_slowa_sjp(wybrana_karta):
                self.wartownik = wybrana_karta
                self.gracze[self.turn].odrzuc_karte(wybrana_karta)
                self.gracze[self.turn].punkty += 1
            else:
                self.wyciagnij_karte()
        else:
            self.wyciagnij_karte()

    def rozdaj_karty(self):
        for _ in range(2):
            temp_lista = []
            for __ in range(6):
                print(temp_lista)
                temp_lista.append(self.karty[-1])
                self.karty.pop()
            gracz = Player(temp_lista)
            self.gracze.append(gracz)

    def czy_zakonczyc_gre(self):
        print('liczba kart:', len(self.gracze[0].karty_gracza))
        print('liczba kart:', len(self.gracze[1].karty_gracza))

        for player_number in range(2):
            if len(self.gracze[player_number].karty_gracza) == 0:
                self.koniec_gry = True
                return True

    def wyciagnij_karte(self):
        try:
            self.gracze[self.turn].pobierz_karte(self.karty[-1])
            self.karty.pop()
        except:
            pass

class Player:
    def __init__(self, rozdane_karty):
        self.karty_gracza = rozdane_karty
        self.punkty = 0

    def odrzuc_karte(self, wybrana_karta):
        self.karty_gracza.remove(wybrana_karta)

    def wyloz_karte(self, sylaba):
        for pojedyncza_karta in self.karty_gracza:
            if pojedyncza_karta == sylaba:
                return sylaba
        raise AssertionError('W kartach gracza nie ma takiej karty.')

    def pobierz_karte(self, karta):
        self.karty_gracza.append(karta)

# gra = Game()
# gra.karty