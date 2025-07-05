.. _rozdzial_3:

#################################
Projekt i Implementacja Bazy Danych
#################################

W niniejszym rozdziale przedstawiono kompletny projekt bazy danych "Sklep". Proces został podzielony na trzy kluczowe etapy: od ogólnego modelu koncepcyjnego, przez szczegółowy model logiczny, aż po model fizyczny w postaci schematu SQL i kodu generatora.

Model Koncepcyjny
=================

Model koncepcyjny definiuje kluczowe byty biznesowe oraz fundamentalne relacje między nimi. Stanowi on wysokopoziomową mapę systemu, która identyfikuje główne obiekty i ich wzajemne powiązania.

.. figure:: /_static/model_konceptualny.png
   :alt: Diagram koncepcyjny bazy danych.
   :align: center
   :width: 90%

   **Rysunek 1: Model koncepcyjny.** Widoczne są główne encje: Klient, Zamówienie, Produkt, Kategoria, Dostawca oraz Pozycje Zamówienia, a także powiązania między nimi, takie jak "składa", "zawiera" czy "dostarcza".

Model Logiczny
==============

Model logiczny jest uszczegółowieniem modelu koncepcyjnego. Definiuje on strukturę tabel, atrybuty (kolumny) dla każdej z nich oraz klucze główne (PK) i obce (FK), które zapewniają integralność relacyjną. Jest on niezależny od konkretnego systemu zarządzania bazą danych.

.. figure:: /_static/model_logiczny.png
   :alt: Diagram logiczny bazy danych.
   :align: center
   :width: 100%

   **Rysunek 2: Model logiczny.** Szczegółowo przedstawia strukturę każdej tabeli, w tym nazwy pól, ich typy generyczne oraz powiązania zrealizowane za pomocą kluczy obcych.

Model Fizyczny (Schemat SQL)
============================

Model fizyczny to konkretna implementacja modelu logicznego w wybranym systemie DBMS (w tym przypadku PostgreSQL i SQLite). Definiuje on precyzyjne typy danych (np. `VARCHAR(100)`, `NUMERIC(10,2)`), indeksy i inne elementy specyficzne dla danej technologii. Poniżej przedstawiono schemat dla bazy PostgreSQL.

.. code-block:: sql
   :caption: Fizyczny schemat bazy danych dla PostgreSQL
   :name: schema-postgres-sql
   :linenos:

    CREATE TABLE Kategorie (
        kategoria_id SERIAL PRIMARY KEY,
        nazwa_kategorii VARCHAR(100) NOT NULL,
        opis TEXT
    );
    CREATE TABLE Dostawcy (
        dostawca_id SERIAL PRIMARY KEY,
        nazwa_firmy VARCHAR(255) NOT NULL,
        telefon VARCHAR(20),
        email VARCHAR(255)
    );
    CREATE TABLE Klienci (
        klient_id SERIAL PRIMARY KEY,
        imie VARCHAR(100) NOT NULL,
        nazwisko VARCHAR(100) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE
    );
    CREATE TABLE Produkty (
        produkt_id SERIAL PRIMARY KEY,
        nazwa_produktu VARCHAR(255) NOT NULL,
        cena NUMERIC(10, 2) NOT NULL,
        stan_magazynowy INT NOT NULL,
        kategoria_id INT REFERENCES Kategorie(kategoria_id),
        dostawca_id INT REFERENCES Dostawcy(dostawca_id)
    );
    CREATE TABLE Zamowienia (
        zamowienie_id SERIAL PRIMARY KEY,
        klient_id INT NOT NULL REFERENCES Klienci(klient_id),
        data_zamowienia TIMESTAMP NOT NULL,
        status VARCHAR(50) NOT NULL
    );
    CREATE TABLE PozycjeZamowienia (
        pozycja_id SERIAL PRIMARY KEY,
        zamowienie_id INT REFERENCES Zamowienia(zamowienie_id),
        produkt_id INT REFERENCES Produkty(produkt_id),
        ilosc INT NOT NULL,
        cena DECIMAL(10, 2) NOT NULL
    );

Opis Tabel
==========

Poniżej znajduje się szczegółowy opis przeznaczenia każdej z tabel.

Klienci
-------
Przechowuje informacje o klientach sklepu.
  - ``klient_id`` (PK): Unikalny identyfikator klienta.
  - ``imie``, ``nazwisko``: Dane osobowe.
  - ``email`` (UNIQUE): Unikalny adres email służący do kontaktu i logowania.

Kategorie
---------
Słownik kategorii, do których przypisane są produkty.
  - ``kategoria_id`` (PK): Unikalny identyfikator kategorii.
  - ``nazwa_kategorii``: Nazwa, np. "Nabiał", "Pieczywo".
  - ``opis``: Dodatkowy opis kategorii.

Dostawcy
--------
Tabela przechowująca dane o dostawcach towaru.
  - ``dostawca_id`` (PK): Unikalny identyfikator dostawcy.
  - ``nazwa_firmy``, ``telefon``, ``email``: Dane kontaktowe dostawcy.

Produkty
--------
Główna tabela z informacjami o wszystkich produktach dostępnych w sklepie.
  - ``produkt_id`` (PK): Unikalny identyfikator produktu.
  - ``nazwa_produktu``, ``cena``: Podstawowe informacje o produkcie.
  - ``stan_magazynowy``: Liczba dostępnych sztuk.
  - ``kategoria_id`` (FK): Klucz obcy łączący z tabelą ``Kategorie``.
  - ``dostawca_id`` (FK): Klucz obcy łączący z tabelą ``Dostawcy``.

Zamowienia
----------
Przechowuje informacje o zamówieniach złożonych przez klientów.
  - ``zamowienie_id`` (PK): Unikalny identyfikator zamówienia.
  - ``klient_id`` (FK): Klucz obcy wskazujący, który klient złożył zamówienie.
  - ``data_zamowienia``: Data i godzina złożenia zamówienia.
  - ``status``: Aktualny status, np. "Złożone", "Wysłane", "Anulowane".

PozycjeZamowienia
-----------------
Tabela asocjacyjna (łącząca) zamówienia z produktami. Określa, jakie produkty i w jakiej ilości znalazły się w danym zamówieniu.
  - ``pozycja_id`` (PK): Unikalny identyfikator pozycji.
  - ``zamowienie_id`` (FK): Klucz obcy łączący z tabelą ``Zamowienia``.
  - ``produkt_id`` (FK): Klucz obcy łączący z tabelą ``Produkty``.
  - ``ilosc``: Liczba sztuk danego produktu w zamówieniu.
  - ``cena``: Cena produktu w momencie zakupu (zapisana, aby uniknąć problemów przy zmianie ceny produktu w przyszłości).

Kod Źródłowy Generatora Bazy Danych
=====================================

Pełna implementacja, wraz z logiką do generowania danych testowych, znajduje się w poniższym skrypcie. Został on użyty do automatycznego stworzenia schematów dla SQLite i PostgreSQL oraz wypełnienia ich danymi.

.. code-block:: python
   :caption: generator_bazy_danych.py
   :name: generator-bazy-danych-py
   :linenos:

   """
   Generator Bazy Danych "Sklep"

   Moduł ten dostarcza kompletne rozwiązanie do automatycznego tworzenia
   i wypełniania danymi testowymi bazy danych dla dwóch różnych systemów:
   SQLite oraz PostgreSQL.

   Został zaprojektowany z myślą o braku zewnętrznych zależności, co gwarantuje
   jego działanie w każdym standardowym środowisku Python 3.
   """
   import sqlite3
   import random
   import os
   from datetime import datetime, timedelta

   # --- Konfiguracja parametrów skryptu ---
   DB_NAME_SQLITE = "sklep.db"
   OUTPUT_SQL_POSTGRES = "sklep_postgres.sql"

   # Liczba rekordów do wygenerowania
   NUM_KLIENCI = 50
   NUM_PRODUKTY = 100
   NUM_ZAMOWIENIA = 150

   # --- Statyczne dane jako źródło dla generatora ---
   IMIONA_M = ['Jan', 'Piotr', 'Krzysztof', 'Andrzej', 'Tomasz', 'Paweł', 'Marcin', 'Michał']
   IMIONA_K = ['Anna', 'Katarzyna', 'Maria', 'Małgorzata', 'Agnieszka', 'Barbara', 'Ewa', 'Elżbieta']
   NAZWISKA = ['Nowak', 'Kowalski', 'Wiśniewski', 'Wójcik', 'Kowalczyk', 'Kamiński', 'Lewandowski', 'Zieliński']
   CZESCI_PRODUKTU_1 = ['Chleb', 'Ser', 'Mleko', 'Jogurt', 'Szynka', 'Sok', 'Woda', 'Masło', 'Jajka', 'Makaron']
   CZESCI_PRODUKTU_2 = ['wiejski', 'naturalny', 'świeży', 'tradycyjny', 'ekologiczny', 'pełnoziarnisty', 'owocowy', 'gazowana']

   KATEGORIE = [
       (1, 'Pieczywo', 'Świeże chleby, bułki i wyroby cukiernicze.'),
       (2, 'Nabiał', 'Mleko, sery, jogurty i inne produkty mleczne.'),
       (3, 'Napoje', 'Soki, wody mineralne i napoje gazowane.'),
       (4, 'Produkty sypkie', 'Mąka, cukier, ryż, makarony.')
   ]
   DOSTAWCY = [
       (1, 'Piekarnia "Złoty Kłos"', '111-222-333', 'kontakt@zlotyklos.pl'),
       (2, 'Mleczarnia "Łąka"', '444-555-666', 'biuro@mleczarnia-laka.com'),
       (3, 'Hurtownia "Napojex"', '777-888-999', 'zamowienia@napojex.pl'),
       (4, 'Rolnik "EkoZbiory"', '123-456-789', 'rolnik@ekozbiory.pl')
   ]

   # --- Definicje schematów SQL ---
   SCHEMA_SQLITE = """
   CREATE TABLE Kategorie (
       kategoria_id INTEGER PRIMARY KEY,
       nazwa_kategorii TEXT NOT NULL,
       opis TEXT
   );
   CREATE TABLE Dostawcy (
       dostawca_id INTEGER PRIMARY KEY,
       nazwa_firmy TEXT NOT NULL,
       telefon TEXT,
       email TEXT
   );
   CREATE TABLE Klienci (
       klient_id INTEGER PRIMARY KEY AUTOINCREMENT,
       imie TEXT NOT NULL,
       nazwisko TEXT NOT NULL,
       email TEXT NOT NULL UNIQUE
   );
   CREATE TABLE Produkty (
       produkt_id INTEGER PRIMARY KEY AUTOINCREMENT,
       nazwa_produktu TEXT NOT NULL,
       cena REAL NOT NULL,
       stan_magazynowy INTEGER NOT NULL,
       kategoria_id INTEGER,
       dostawca_id INTEGER,
       FOREIGN KEY (kategoria_id) REFERENCES Kategorie(kategoria_id),
       FOREIGN KEY (dostawca_id) REFERENCES Dostawcy(dostawca_id)
   );
   CREATE TABLE Zamowienia (
       zamowienie_id INTEGER PRIMARY KEY AUTOINCREMENT,
       klient_id INTEGER NOT NULL,
       data_zamowienia DATETIME NOT NULL,
       status TEXT NOT NULL,
       FOREIGN KEY (klient_id) REFERENCES Klienci(klient_id)
   );
   CREATE TABLE PozycjeZamowienia (
       pozycja_id INTEGER PRIMARY KEY AUTOINCREMENT,
       zamowienie_id INTEGER NOT NULL,
       produkt_id INTEGER NOT NULL,
       ilosc INTEGER NOT NULL,
       cena REAL NOT NULL,
       FOREIGN KEY (zamowienie_id) REFERENCES Zamowienia(zamowienie_id),
       FOREIGN KEY (produkt_id) REFERENCES Produkty(produkt_id)
   );
   """

   SCHEMA_POSTGRES = """
   DROP TABLE IF EXISTS PozycjeZamowienia, Zamowienia, Produkty, Klienci, Dostawcy, Kategorie CASCADE;
   CREATE TABLE Kategorie (
       kategoria_id SERIAL PRIMARY KEY,
       nazwa_kategorii VARCHAR(100) NOT NULL,
       opis TEXT
   );
   CREATE TABLE Dostawcy (
       dostawca_id SERIAL PRIMARY KEY,
       nazwa_firmy VARCHAR(255) NOT NULL,
       telefon VARCHAR(20),
       email VARCHAR(255)
   );
   CREATE TABLE Klienci (
       klient_id SERIAL PRIMARY KEY,
       imie VARCHAR(100) NOT NULL,
       nazwisko VARCHAR(100) NOT NULL,
       email VARCHAR(255) NOT NULL UNIQUE
   );
   CREATE TABLE Produkty (
       produkt_id SERIAL PRIMARY KEY,
       nazwa_produktu VARCHAR(255) NOT NULL,
       cena NUMERIC(10, 2) NOT NULL,
       stan_magazynowy INT NOT NULL,
       kategoria_id INT REFERENCES Kategorie(kategoria_id),
       dostawca_id INT REFERENCES Dostawcy(dostawca_id)
   );
   CREATE TABLE Zamowienia (
       zamowienie_id SERIAL PRIMARY KEY,
       klient_id INT NOT NULL REFERENCES Klienci(klient_id),
       data_zamowienia TIMESTAMP NOT NULL,
       status VARCHAR(50) NOT NULL
   );
   CREATE TABLE PozycjeZamowienia (
       pozycja_id SERIAL PRIMARY KEY,
       zamowienie_id INT REFERENCES Zamowienia(zamowienie_id),
       produkt_id INT REFERENCES Produkty(produkt_id),
       ilosc INT NOT NULL,
       cena DECIMAL(10, 2) NOT NULL
   );
   """

   def generuj_dane():
       """
       Przygotowuje w pamięci kompletny zestaw danych testowych.

       Funkcja tworzy spójny zestaw list z danymi dla klientów, produktów,
       zamówień oraz pozycji zamówień. Respektuje przy tym zdefiniowane
       relacje i losowo generuje powiązania.

       :returns: Słownik zawierający listy krotek dla każdej tabeli.
                 Klucze: 'klienci', 'produkty', 'zamowienia', 'pozycje_zamowien'.
       :rtype: dict
       """
       klienci = []
       for i in range(NUM_KLIENCI):
           imie = random.choice(IMIONA_M + IMIONA_K)
           nazwisko = random.choice(NAZWISKA)
           email = f"{imie.lower()}.{nazwisko.lower()}{i}@example.com"
           klienci.append((i + 1, imie, nazwisko, email))

       produkty = []
       for i in range(NUM_PRODUKTY):
           nazwa = f"{random.choice(CZESCI_PRODUKTU_1)} {random.choice(CZESCI_PRODUKTU_2)}"
           cena = round(random.uniform(2.5, 50.0), 2)
           stan = random.randint(0, 200)
           kat_id = random.choice(KATEGORIE)[0]
           dos_id = random.choice(DOSTAWCY)[0]
           produkty.append((i + 1, nazwa, cena, stan, kat_id, dos_id))

       zamowienia = []
       statusy = ['Złożone', 'Wysłane', 'Dostarczone', 'Anulowane']
       for i in range(NUM_ZAMOWIENIA):
           klient_id = random.randint(1, NUM_KLIENCI)
           data = datetime.now() - timedelta(days=random.randint(0, 365))
           status = random.choice(statusy)
           zamowienia.append((i + 1, klient_id, data, status))
           
       pozycje_zamowien = []
       pozycja_id_counter = 1
       for zamowienie in zamowienia:
           zamowienie_id = zamowienie[0]
           for _ in range(random.randint(1, 5)):
               produkt = random.choice(produkty)
               produkt_id = produkt[0]
               cena_w_chwili_zakupu = produkt[2] 
               ilosc = random.randint(1, 10)
               pozycje_zamowien.append((pozycja_id_counter, zamowienie_id, produkt_id, ilosc, cena_w_chwili_zakupu))
               pozycja_id_counter += 1
               
       return {
           'klienci': klienci, 
           'produkty': produkty, 
           'zamowienia': zamowienia,
           'pozycje_zamowien': pozycje_zamowien
       }

   def stworz_baze_sqlite(dane):
       """
       Tworzy i wypełnia bazę danych SQLite na podstawie dostarczonych danych.

       Funkcja usuwa istniejący plik bazy, tworzy nową strukturę
       zgodnie ze schematem i wstawia dane za pomocą operacji masowych.

       :param dict dane: Słownik z danymi, wynik działania funkcji :func:`generuj_dane`.
       """
       if os.path.exists(DB_NAME_SQLITE):
           os.remove(DB_NAME_SQLITE)
       
       conn = sqlite3.connect(DB_NAME_SQLITE)
       cursor = conn.cursor()
       
       cursor.executescript(SCHEMA_SQLITE)
       cursor.executemany("INSERT INTO Kategorie VALUES (?, ?, ?)", KATEGORIE)
       cursor.executemany("INSERT INTO Dostawcy VALUES (?, ?, ?, ?)", DOSTAWCY)
       cursor.executemany("INSERT INTO Klienci (klient_id, imie, nazwisko, email) VALUES (?, ?, ?, ?)", dane['klienci'])
       cursor.executemany("INSERT INTO Produkty (produkt_id, nazwa_produktu, cena, stan_magazynowy, kategoria_id, dostawca_id) VALUES (?, ?, ?, ?, ?, ?)", dane['produkty'])
       cursor.executemany("INSERT INTO Zamowienia (zamowienie_id, klient_id, data_zamowienia, status) VALUES (?, ?, ?, ?)", dane['zamowienia'])
       cursor.executemany("INSERT INTO PozycjeZamowienia (pozycja_id, zamowienie_id, produkt_id, ilosc, cena) VALUES (?, ?, ?, ?, ?)", dane['pozycje_zamowien'])
       
       conn.commit()
       conn.close()
       print(f"Baza SQLite '{DB_NAME_SQLITE}' została utworzona pomyślnie.")

   def stworz_skrypt_postgres(dane):
       """
       Generuje kompletny plik .sql dla bazy PostgreSQL.

       Funkcja tworzy plik .sql, który może być wykonany na serwerze
       PostgreSQL w celu odtworzenia identycznej struktury i zawartości
       bazy danych. Automatycznie formatuje wartości i aktualizuje sekwencje.

       :param dict dane: Słownik z danymi, wynik działania funkcji :func:`generuj_dane`.
       """
       with open(OUTPUT_SQL_POSTGRES, 'w', encoding='utf-8') as f:
           f.write("-- Wygenerowany skrypt SQL dla PostgreSQL\n")
           f.write(SCHEMA_POSTGRES)
           f.write("\n\n-- Wstawianie danych\n")

           def format_sql(val):
               if isinstance(val, str):
                   return f"'{val.replace("'", "''")}'"
               if isinstance(val, datetime):
                   return f"'{val.strftime('%Y-%m-%d %H:%M:%S')}'"
               return str(val)

           for kat in KATEGORIE:
               f.write(f"INSERT INTO Kategorie VALUES ({', '.join(map(format_sql, kat))});\n")
           for dos in DOSTAWCY:
               f.write(f"INSERT INTO Dostawcy VALUES ({', '.join(map(format_sql, dos))});\n")
           for k in dane['klienci']:
               f.write(f"INSERT INTO Klienci (klient_id, imie, nazwisko, email) VALUES ({', '.join(map(format_sql, k))});\n")
           for p in dane['produkty']:
                f.write(f"INSERT INTO Produkty (produkt_id, nazwa_produktu, cena, stan_magazynowy, kategoria_id, dostawca_id) VALUES ({', '.join(map(format_sql, p))});\n")
           for z in dane['zamowienia']:
               f.write(f"INSERT INTO Zamowienia (zamowienie_id, klient_id, data_zamowienia, status) VALUES ({', '.join(map(format_sql, z))});\n")
           for pz in dane['pozycje_zamowien']:
               f.write(f"INSERT INTO PozycjeZamowienia (pozycja_id, zamowienie_id, produkt_id, ilosc, cena) VALUES ({', '.join(map(format_sql, pz))});\n")

           f.write("\n-- Aktualizacja sekwencji kluczy głównych\n")
           f.write("SELECT setval('kategorie_kategoria_id_seq', (SELECT MAX(kategoria_id) FROM Kategorie));\n")
           f.write("SELECT setval('dostawcy_dostawca_id_seq', (SELECT MAX(dostawca_id) FROM Dostawcy));\n")
           f.write("SELECT setval('klienci_klient_id_seq', (SELECT MAX(klient_id) FROM Klienci));\n")
           f.write("SELECT setval('produkty_produkt_id_seq', (SELECT MAX(produkt_id) FROM Produkty));\n")
           f.write("SELECT setval('zamowienia_zamowienie_id_seq', (SELECT MAX(zamowienie_id) FROM Zamowienia));\n")
           f.write("SELECT setval('pozycjezamowienia_pozycja_id_seq', (SELECT MAX(pozycja_id) FROM PozycjeZamowienia));\n")

       print(f"Skrypt dla PostgreSQL '{OUTPUT_SQL_POSTGRES}' został wygenerowany pomyślnie.")

   if __name__ == '__main__':
       """
       Główny blok wykonawczy skryptu.

       Jego zadaniem jest orkiestracja całego procesu: wygenerowanie danych,
       stworzenie bazy SQLite oraz wygenerowanie skryptu dla PostgreSQL.
       """
       print("Rozpoczynam generowanie baz danych.")
       dane_wygenerowane = generuj_dane()
       stworz_baze_sqlite(dane_wygenerowane)
       stworz_skrypt_postgres(dane_wygenerowane)
       print("\nZakończono. Utworzono plik bazy SQLite i plik .sql dla PostgreSQL.")