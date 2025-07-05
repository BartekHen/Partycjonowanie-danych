.. _rozdzial_4:

#####################################
Analiza i Implementacja Bazy Danych
#####################################

Ten rozdział poświęcony jest szczegółowej analizie struktury bazy danych "Sklep", procesowi jej normalizacji oraz prezentacji kluczowych skryptów i zapytań SQL, które umożliwiają interakcję z danymi.

Analiza Struktury i Normalizacja
=================================

Projekt bazy danych został oparty o model relacyjny, co gwarantuje spójność i integralność danych. Proces projektowania uwzględniał zasady normalizacji, aby wyeliminować redundancję i anomalie danych.

Pierwsza Postać Normalna (1NF)
-------------------------------
Każda tabela w bazie posiada klucz główny, a wszystkie atrybuty w tabelach przechowują wartości atomowe (niepodzielne). Przykładowo, w tabeli `Klienci` adres email jest pojedynczą informacją, a w `Produktach` cena jest jedną liczbą. Nie ma pól, które zawierałyby listy czy zbiory danych.

Druga Postać Normalna (2NF)
----------------------------
Wszystkie atrybuty w tabelach, które mają klucze złożone (w naszym przypadku tylko tabela asocjacyjna `PozycjeZamowienia`), są w pełni zależne od całego klucza głównego. W pozostałych tabelach klucze główne są proste (jednopolowe), więc warunek 2NF jest automatycznie spełniony. W `PozycjeZamowienia` atrybuty `ilosc` i `cena` zależą zarówno od `zamowienie_id`, jak i `produkt_id`.

Trzecia Postać Normalna (3NF)
-----------------------------
W bazie nie występują zależności przechodnie. Żaden atrybut niekluczowy nie jest zależny od innego atrybutu niekluczowego. Na przykład, w tabeli `Produkty` nie przechowujemy nazwy kategorii czy danych dostawcy – zamiast tego używamy kluczy obcych (`kategoria_id`, `dostawca_id`), które wskazują na odpowiednie rekordy w tabelach `Kategorie` i `Dostawcy`. Dzięki temu zmiana nazwy kategorii wymaga modyfikacji tylko jednego rekordu w tabeli `Kategorie`.

Podsumowując, schemat bazy danych jest zgodny z **trzecią postacią normalną (3NF)**, co jest standardem dla dobrze zaprojektowanych relacyjnych baz danych.

Skrypty SQL i Generowanie Danych
=================================

Do stworzenia i wypełnienia bazy danych przygotowano skrypty SQL dla dwóch popularnych systemów: SQLite oraz PostgreSQL.

Implementacja w SQLite
----------------------
Poniższy fragment kodu SQL definiuje kompletną strukturę tabel dla bazy SQLite. Używa typów danych specyficznych dla tego systemu, takich jak `INTEGER PRIMARY KEY` dla automatycznie inkrementowanych kluczy.

.. code-block:: sql
   :caption: Schemat bazy danych dla SQLite

   CREATE TABLE Kategorie (
       kategoria_id INTEGER PRIMARY KEY,
       nazwa_kategorii TEXT NOT NULL,
       opis TEXT
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
   -- ... pozostałe tabele ...

Implementacja w PostgreSQL
--------------------------
Dla systemu PostgreSQL schemat wykorzystuje bardziej rygorystyczne typy danych (`VARCHAR`, `NUMERIC`, `TIMESTAMP`) oraz sekwencje (`SERIAL`) do automatycznego generowania kluczy głównych.

.. code-block:: sql
   :caption: Schemat bazy danych dla PostgreSQL

   CREATE TABLE Kategorie (
       kategoria_id SERIAL PRIMARY KEY,
       nazwa_kategorii VARCHAR(100) NOT NULL,
       opis TEXT
   );
   CREATE TABLE Produkty (
       produkt_id SERIAL PRIMARY KEY,
       nazwa_produktu VARCHAR(255) NOT NULL,
       cena NUMERIC(10, 2) NOT NULL,
       stan_magazynowy INT NOT NULL,
       kategoria_id INT REFERENCES Kategorie(kategoria_id),
       dostawca_id INT REFERENCES Dostawcy(dostawca_id)
   );
   -- ... pozostałe tabele ...


Przykładowe Zapytania i Optymalizacja
======================================

Poniżej znajdują się przykłady zapytań SQL, które można wykonać na bazie "Sklep", wraz z omówieniem potencjalnych optymalizacji.

Zapytanie 1: Suma wartości zamówień dla każdego klienta
-------------------------------------------------------
To zapytanie oblicza łączną kwotę wydaną przez każdego klienta.

.. code-block:: sql

   SELECT
       k.imie,
       k.nazwisko,
       k.email,
       SUM(pz.ilosc * pz.cena) AS laczna_wartosc_zamowien
   FROM Klienci k
   JOIN Zamowienia z ON k.klient_id = z.klient_id
   JOIN PozycjeZamowienia pz ON z.zamowienie_id = pz.zamowienie_id
   GROUP BY k.klient_id, k.imie, k.nazwisko, k.email
   ORDER BY laczna_wartosc_zamowien DESC;

**Optymalizacja:** Zapytanie wykorzystuje złączenia (JOIN) tabel. Aby przyspieszyć jego wykonanie, kluczowe jest posiadanie **indeksów** na kolumnach używanych do złączeń, czyli `Klienci(klient_id)`, `Zamowienia(klient_id)`, `Zamowienia(zamowienie_id)` oraz `PozycjeZamowienia(zamowienie_id)`. W naszym schemacie kolumny te są kluczami głównymi lub obcymi, na których systemy bazodanowe zazwyczaj automatycznie tworzą indeksy.

Zapytanie 2: Znalezienie 5 najpopularniejszych produktów
-------------------------------------------------------
To zapytanie zlicza, ile razy każdy produkt został zamówiony.

.. code-block:: sql

   SELECT
       p.nazwa_produktu,
       COUNT(pz.produkt_id) AS liczba_zamowien
   FROM Produkty p
   JOIN PozycjeZamowienia pz ON p.produkt_id = pz.produkt_id
   GROUP BY p.produkt_id, p.nazwa_produktu
   ORDER BY liczba_zamowien DESC
   LIMIT 5;

**Optymalizacja:** Podobnie jak w poprzednim przypadku, wydajność zależy od indeksów na kolumnach `Produkty(produkt_id)` i `PozycjeZamowienia(produkt_id)`. Przy bardzo dużej liczbie pozycji w zamówieniach, wydajność można by dalej poprawić poprzez denormalizację, np. dodając licznik zamówień bezpośrednio w tabeli `Produkty`, jednak odbyłoby się to kosztem utrzymania spójności danych. Dla obecnej struktury indeksy są wystarczające.