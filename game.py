import random


class Game:
    # jakie atrybuty przyjmuje klasa
    # i jakie metody sa mozliwe

    def __init__(self):
        self.karty = ['by', 'ko', 'pu', 'le', 'na', 'py', 'ma', 'gi', 'ki', 'sza', 'li', 'fa', 'my', 'że', 'cza',
                      'tka', 'mi', 'nie', 'ni', 'cha', 'wo', 'la', 'ka', 'lu', 'ga', 'mu', 'sy', 'pa', 'ty', 'wy',
                      'by', 'ry', 'da', 'to', 'ra', 'fu', 'dy', 'chy', 'ru', 'ku', 'wa', 'dy', 'ta', 'ny', 'po', 'ła',
                      'do', 'ba', 'no', 'sa']
        self.karty_gracza = 6
        self.turn = 1
        self.wartownik = ''
        self.gracze = []
        self.koniec_gry = None

    def __str__(self):
        return f" {self.karty}"

    def init_game(self, tryb_gry='cpu'):
        random.shuffle(self.karty)
        self.wartownik = self.karty[-1]
        self.karty.pop()
        self.lista_graczy = self.rozdaj_karty()

    def start_gry(self, sylaba, tryb_gry='cpu'):
        self.ruch(sylaba)
        if self.czy_zakonczyc_gre():
            return True
        self.zmiana_gracza()


    def ruch(self, sylaba):
        if self.turn == 0:
            # self.ruch_cpu() # losowe ruchy z tych kart co ma w rece
            self.ruch_gracza(sylaba)
        elif self.turn == 1:
            self.ruch_gracza(sylaba)

    def sprawdz_poprawnosc_slowa(self, wybrana_karta):
        if len(self.wartownik + wybrana_karta) >= 4:
            return True
        else:
            return False

    def sprawdzanie_slowa_sjp(self, wybrana_karta):
        pass



    def ruch_gracza(self, sylaba=None):
        print(self.gracze)
        print(self.gracze[self.turn].karty_gracza)
        # sylaba = input('wybierz karte ktora chcesz zagrac')
        if sylaba:
            wybrana_karta = self.gracze[self.turn].wyloz_karte(
                sylaba)  # id albo pelna wartosc zwraca(return) wartosc karty np 'ba'
            if self.sprawdz_poprawnosc_slowa(wybrana_karta):
                self.wartownik = wybrana_karta
                self.gracze[self.turn].odrzuc_karte(wybrana_karta)
            else:
                self.gracze[self.turn].pobierz_karte(self.karty[-1])
                self.karty.pop()
        else:
            self.gracze[self.turn].pobierz_karte(self.karty[-1])
            self.karty.pop()

    def zmiana_gracza(self):
        self.turn = (self.turn + 1) % 2

    def ruch_cpu(self):
        pass

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
        if len(self.gracze[self.turn].karty_gracza) == 0:
            self.koniec_gry = self.turn
            return True


class Player:
    id = 0

    # def __init__(self, id):
    #     self.id = id

    def __init__(self, rozdane_karty):
        self.karty_gracza = rozdane_karty

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
# gra.start_gry()