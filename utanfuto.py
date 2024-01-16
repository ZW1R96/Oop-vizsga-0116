from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Union

class Utanfuto(ABC):                                        #absztrakt osztaly
    def __init__(self, tipus: str, ar: int, terhelhetoseg: int):      #használok type hinting-et
        self.tipus = tipus
        self.ar = ar
        self.terhelhetoseg = terhelhetoseg

    @abstractmethod                                        #absztrakt metódus
    def kiiro_info(self) -> str:
        pass

class PonyvasUtanfuto(Utanfuto):
    def kiiro_info(self) -> str:
        return f"{self.tipus} - Terhelhetőség: {self.terhelhetoseg} kg, Ár: {self.ar} HUF"

class AutoszallitoUtanfuto(Utanfuto):
    def kiiro_info(self) -> str:
        return f"{self.tipus} - Terhelhetőség: {self.terhelhetoseg} kg, Ár: {self.ar} HUF"

class FekezettUtanfuto(Utanfuto):
    def kiiro_info(self) -> str:
        return f"{self.tipus} - Terhelhetőség: {self.terhelhetoseg} kg, Ár: {self.ar} HUF"

class Kolcsonzo:
    def __init__(self, nev: str):
        self._nev = nev                                        #non-public attribútum
        self.utanfutok: List[Utanfuto] = []
        self.kolcsonzesek: List[dict] = []

    def tesztadatok_betoltese(self) -> None:                    #tesztadatok betöltése
        ponyvas_utanfuto = PonyvasUtanfuto("Ponyvás utánfutó", 5000, 1000)
        autoszallito_utanfuto = AutoszallitoUtanfuto("Autószállító utánfutó", 6000, 1500)
        fekezett_utanfuto = FekezettUtanfuto("Fékezett utánfutó", 4500, 1200)

        self.utanfuto_hozzaadas(ponyvas_utanfuto)
        self.utanfuto_hozzaadas(autoszallito_utanfuto)
        self.utanfuto_hozzaadas(fekezett_utanfuto)

        kezdo_datum = datetime.now() + timedelta(days=1)         #a példakölcsönzések holnapiak, hogy lehessen törölni őket
        self.utanfuto_kolcsonzes(0, kezdo_datum)
        self.utanfuto_kolcsonzes(1, kezdo_datum)
        self.utanfuto_kolcsonzes(2, kezdo_datum)

    def utanfuto_hozzaadas(self, utanfuto: Utanfuto) -> None:
        self.utanfutok.append(utanfuto)

    def utanfuto_kolcsonzes(self, utanfuto_index: int, kolcsonzes_datum: datetime) -> Union[str, None]:
        if 0 <= utanfuto_index < len(self.utanfutok):
            utanfuto = self.utanfutok[utanfuto_index]
            if kolcsonzes_datum >= datetime.now():
                kolcsonzes_ara = utanfuto.ar
                kolcsonzes = {"utanfuto": utanfuto, "datum": kolcsonzes_datum, "koltseg": kolcsonzes_ara}   #dictionary
                self.kolcsonzesek.append(kolcsonzes)
                return f"A kölcsönzés sikeres. Fizetendő: {kolcsonzes_ara} HUF"
            else:
                return "Érvénytelen kölcsönzési dátum. Csak a jövőbeli dátumok érvényesek."
        else:
            return "Nincs ilyen utánfutó."                          #ugyanaz az utánfutó típus többször is kölcsönözhető ugyanarra a napra, hiszen több utánfutója is van a kölcsönzőnek, nem csak 1-1 mindegyikből

    def kolcsonzes_megszuntetes(self, kolcsonzes_index: int) -> Union[str, None]:
        if 0 <= kolcsonzes_index < len(self.kolcsonzesek):
            kolcsonzes = self.kolcsonzesek[kolcsonzes_index]
            if kolcsonzes['datum'] > datetime.now():
                self.kolcsonzesek.pop(kolcsonzes_index)
                return f"Kölcsönzés sikeresen megszüntetve. Visszatérítés: {kolcsonzes['koltseg']} HUF"
            else:
                return "Az aznapi kölcsönzéseket nem lehet megszüntetni."
        else:
            return "Nincs ilyen kölcsönzés."

    def kolcsonzesek_listazasa(self) -> str:
        if not self.kolcsonzesek:
            return "Jelenleg nincsenek kölcsönzések."
        kolcsonzes_lista = "\n".join([f"{index+1}. {kolcsonzes['utanfuto'].tipus} - {kolcsonzes['datum'].strftime('%Y-%m-%d')} - {kolcsonzes['koltseg']} HUF"
                                for index, kolcsonzes in enumerate(self.kolcsonzesek)])
        return f"\nJelenlegi kölcsönzések:\n{kolcsonzes_lista}"

    @property                                                      #property decorator a getter elé
    def nev(self) -> str:
        return self._nev

def felhasznaloi_interakcio() -> None:
    kolcsonzo = Kolcsonzo("Repülő szőnyeg")
    kolcsonzo.tesztadatok_betoltese()

    print(f"____________________________________________\nÜdvözöl a {kolcsonzo.nev} utánfutó-kölcsönző!")

    while True:
        print("\nVálassz egy lehetőséget:")
        print("1. Utánfutó kölcsönzése")
        print("2. Kölcsönzés megszüntetése")
        print("3. Kölcsönzések listázása")
        print("4. Kilépés")

        valasztas = input("Választás (1/2/3/4): ")

        if valasztas == "1":
            print("\nElérhető utánfutók:")
            for i, ut in enumerate(kolcsonzo.utanfutok):
                print(f"{i+1}. {ut.kiiro_info()}")
            ut_index = int(input("Válassz egy utánfutót: ")) - 1
            kolcsonzes_datum = datetime.strptime(input("Add meg a kölcsönzés dátumát (YYYY-MM-DD): "), "%Y-%m-%d")
            print(kolcsonzo.utanfuto_kolcsonzes(ut_index, kolcsonzes_datum))

        elif valasztas == "2":
            if kolcsonzo.kolcsonzesek:
                print(kolcsonzo.kolcsonzesek_listazasa())
                kolcsonzes_index = int(input("Válassz egy kölcsönzést a megszüntetéshez: ")) - 1
                print(kolcsonzo.kolcsonzes_megszuntetes(kolcsonzes_index))
            else:
                print("Jelenleg nincsenek kölcsönzések.")

        elif valasztas == "3":
            print(kolcsonzo.kolcsonzesek_listazasa())

        elif valasztas == "4":
            print("Köszönjük, hogy használtad a szolgáltatásunkat. Vezess óvatosan.")
            break

        else:
            print("Érvénytelen választás. Válassz újra.")

if __name__ == "__main__":
    felhasznaloi_interakcio()
