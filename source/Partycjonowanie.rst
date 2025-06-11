Sprawozdanie: Partycjonowanie danych w PostgreSQL
=================================================

:Autor: Bartosz Potoczny
:Data: 2025-06-12

Cel sprawozdania
----------------

Celem niniejszego sprawozdania jest przedstawienie procesu partycjonowania danych w systemie bazodanowym PostgreSQL, omówienie jego zalet, typów oraz prezentacja praktycznych przykładów i narzędzi do monitorowania partycji. Sprawozdanie zawiera także analizę wpływu partycjonowania na wydajność oraz wnioski praktyczne.

Wstęp teoretyczny
-----------------

Partycjonowanie w PostgreSQL polega na podziale dużej tabeli na mniejsze fragmenty zwane partycjami (ang. partitions). Każda partycja przechowuje podzbiór danych zgodnie z określonym kryterium, takim jak zakres wartości, lista wartości, czy wynik funkcji haszującej. Partycjonowanie jest całkowicie transparentne dla użytkownika – tabele partycjonowane zachowują się jak zwykłe tabele, a obsługa partycji realizowana jest przez silnik bazy danych.

**Zalety partycjonowania:**
- Zmniejszenie czasu wykonywania zapytań poprzez ograniczenie zakresu przeszukiwanych danych (tzw. partition pruning).
- Szybsze operacje usuwania i archiwizacji danych (możliwość odłączenia i usunięcia całych partycji).
- Lepsze zarządzanie miejscem na dysku i łatwiejsza konserwacja (np. reindeksacja tylko wybranych partycji).
- Poprawa wydajności przy ładowaniu dużych ilości danych (np. przez COPY do partycji zamiast do całej tabeli).

**Typy partycjonowania w PostgreSQL:**
1. **Zakresowe (RANGE):** Podział na podstawie zakresu wartości w kolumnie (np. daty, liczby). Najczęściej stosowane, gdy dane naturalnie rosną (np. logi, dane czasowe).
2. **Listowe (LIST):** Podział na podstawie konkretnych wartości (np. partycjonowanie według kraju, regionu, statusu).
3. **Haszowe (HASH):** Podział na podstawie wartości funkcji haszującej, równomiernie rozkładający dane pomiędzy partycje. Stosowane, gdy nie ma logicznego podziału według zakresu ani listy.

Opis środowiska i konfiguracji
------------------------------

- **System operacyjny:** Ubuntu 22.04 LTS
- **PostgreSQL:** wersja 15
- **Konfiguracja systemowa:** Domyślna, z włączonym autovacuum.
- **Schemat bazy:** Tabela zamówień (orders), partycjonowana po dacie zamówienia.

Przykłady partycjonowania – krok po kroku
-----------------------------------------

**1. Tworzenie tabeli partycjonowanej (zakresowej):**

.. code-block:: sql

   CREATE TABLE orders (
      order_id serial PRIMARY KEY,
      order_date date NOT NULL,
      customer_id int NOT NULL,
      amount numeric
   ) PARTITION BY RANGE (order_date);

**2. Tworzenie partycji dla poszczególnych lat:**

.. code-block:: sql

   CREATE TABLE orders_2023 PARTITION OF orders
      FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

   CREATE TABLE orders_2024 PARTITION OF orders
      FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

**3. Przykład partycjonowania listowego:**

.. code-block:: sql

   CREATE TABLE sales (
      sale_id serial PRIMARY KEY,
      country text NOT NULL,
      sale_date date NOT NULL,
      value numeric
   ) PARTITION BY LIST (country);

   CREATE TABLE sales_poland PARTITION OF sales FOR VALUES IN ('Poland');
   CREATE TABLE sales_germany PARTITION OF sales FOR VALUES IN ('Germany');

**4. Przykład partycjonowania haszowego:**

.. code-block:: sql

   CREATE TABLE logs (
      log_id serial PRIMARY KEY,
      event_time timestamp NOT NULL,
      user_id int NOT NULL
   ) PARTITION BY HASH (user_id);

   CREATE TABLE logs_p0 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 0);
   CREATE TABLE logs_p1 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 1);
   CREATE TABLE logs_p2 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 2);
   CREATE TABLE logs_p3 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 3);

**5. Wstawianie przykładowych danych:**

.. code-block:: sql

   INSERT INTO orders (order_date, customer_id, amount)
   VALUES
      ('2023-02-15', 1, 150.00),
      ('2023-11-03', 2, 400.00),
      ('2024-05-06', 3, 230.00);

**6. Sprawdzanie rozmieszczenia danych w partycjach:**

.. code-block:: sql

   SELECT tableoid::regclass AS partition, * FROM orders;

   -- lub
   SELECT * FROM orders_2023;
   SELECT * FROM orders_2024;

**7. Usuwanie całych partycji (np. archiwizacja):**

.. code-block:: sql

   -- Odłączenie partycji i późniejsze jej usunięcie
   ALTER TABLE orders DETACH PARTITION orders_2023;
   DROP TABLE orders_2023;

**8. Dodawanie nowej partycji (np. na kolejny rok):**

.. code-block:: sql

   CREATE TABLE orders_2025 PARTITION OF orders
      FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

Monitorowanie partycji i wydajności
-----------------------------------

**1. Sprawdzanie istniejących partycji:**

.. code-block:: sql

   SELECT inhrelid::regclass AS partition
   FROM pg_inherits
   WHERE inhparent = 'orders'::regclass;

**2. Analiza planu zapytania i partition pruning:**

.. code-block:: sql

   EXPLAIN ANALYZE
   SELECT * FROM orders WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01';

   -- W planie powinno być widać, że użyta została tylko partycja orders_2024.

**3. Statystyki dla partycji:**

.. code-block:: sql

   SELECT relname, n_live_tup, n_dead_tup
   FROM pg_stat_user_tables
   WHERE relname LIKE 'orders_%';

**4. Sprawdzanie rozmiaru partycji:**

.. code-block:: sql

   SELECT relname AS "Partition", pg_size_pretty(pg_total_relation_size(relid)) AS "Size"
   FROM pg_catalog.pg_statio_user_tables
   WHERE relname LIKE 'orders_%'
   ORDER BY pg_total_relation_size(relid) DESC;

Analiza i obserwacje
--------------------

1. Po wstawieniu danych do tabeli partycjonowanej, PostgreSQL automatycznie umieszcza wiersze w odpowiednich partycjach, zgodnie z regułą partycjonowania.
2. Zapytania zawężające zakres (np. WHERE order_date BETWEEN ...) przeszukują tylko właściwe partycje, co istotnie skraca czas wyszukiwania.
3. Można łatwo sprawdzić, do której partycji trafiły konkretne rekordy.
4. Możliwość dodawania i usuwania partycji pozwala na wygodne archiwizowanie starych danych bez kosztownych operacji DELETE.
5. W przypadku błędnej konfiguracji partycjonowania (brak partycji na określony zakres) próba wstawienia danych zakończy się błędem.
6. Partycjonowanie haszowe najlepiej sprawdza się, gdy dane nie dają się łatwo podzielić logicznie (np. po dacie lub wartościach dyskretnych).
7. Plan zapytania (EXPLAIN) potwierdza, że PostgreSQL wykorzystuje tzw. "partition pruning", eliminując niepotrzebne partycje z przeszukiwania.
8. Statystyki i rozmiary partycji można wygodnie monitorować, co ułatwia zarządzanie dużymi zbiorami danych.

Wnioski
-------

Partycjonowanie tabel w PostgreSQL to skuteczny sposób na poprawę wydajności i elastyczności zarządzania dużymi zbiorami danych. Prawidłowo zastosowane partycjonowanie pozwala na:
- skrócenie czasu wykonywania zapytań,
- łatwiejszą archiwizację i czyszczenie danych historycznych,
- lepszą kontrolę nad rozmiarem i wydajnością poszczególnych fragmentów tabeli.

W praktyce należy dobrze przemyśleć klucz partycjonowania, liczbę partycji oraz sposób ich utrzymania (np. automatyczne tworzenie partycji na kolejne okresy). Warto regularnie monitorować statystyki i rozmiary partycji oraz testować plany zapytań.

Bibliografia
------------

1. https://www.postgresql.org/docs/current/ddl-partitioning.html
2. https://wiki.postgresql.org/wiki/Partitioning
3. Dokumentacja PostgreSQL – Rozdział o partycjonowaniu tabel
