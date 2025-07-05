Partycjonowanie danych w PostgreSQL – analiza, typy, zastosowania i dobre praktyki
=================================================================================

:Autor: Bartosz Potoczny
:Data: 2025-06-12

Streszczenie
------------

Celem niniejszego sprawozdania jest kompleksowa analiza zagadnienia partycjonowania danych w systemie zarządzania relacyjną bazą danych PostgreSQL. Praca omawia teoretyczne podstawy partycjonowania, szczegółowo wyjaśnia wszystkie dostępne mechanizmy oraz przedstawia metody realizacji partycjonowania w praktyce. Zaprezentowano również typowe scenariusze użycia, narzędzia monitorowania oraz najlepsze praktyki projektowe. Całość przeanalizowano pod kątem wydajności, utrzymania i bezpieczeństwa danych.

1. Wprowadzenie
---------------

Współczesne systemy informatyczne generują i przetwarzają coraz większe ilości danych, co wymusza stosowanie zaawansowanych mechanizmów optymalizacji przechowywania i dostępu do informacji. Partycjonowanie danych jest jedną z kluczowych technik pozwalających na poprawę wydajności, skalowalności i zarządzalności baz danych. PostgreSQL, jako zaawansowany system zarządzania relacyjną bazą danych (RDBMS), oferuje rozbudowane wsparcie dla partycjonowania, umożliwiając dostosowanie architektury bazy do indywidualnych potrzeb.

2. Definicja i cel partycjonowania
----------------------------------

Partycjonowanie polega na logicznym podziale dużej tabeli na mniejsze, łatwiejsze w zarządzaniu fragmenty zwane partycjami. Mimo fizycznego rozdzielenia, partycje są prezentowane użytkownikowi jako jedna wspólna tabela nadrzędna (ang. partitioned table, master table). Celem partycjonowania jest:

- Zwiększenie wydajności operacji SELECT, INSERT, UPDATE, DELETE poprzez ograniczenie zakresu danych do przeszukania (partition pruning).
- Ułatwienie zarządzania i archiwizacji danych (np. szybkie usuwanie lub przenoszenie całych partycji).
- Lepsze rozłożenie obciążenia (możliwość przechowywania partycji na różnych dyskach/tablespaces).
- Zmniejszenie ryzyka zablokowania całej tabeli podczas operacji konserwacyjnych (VACUUM, REINDEX itp.).

3. Modele i typy partycjonowania w PostgreSQL
---------------------------------------------

PostgreSQL obsługuje trzy podstawowe typy partycjonowania:

### 3.1 Partycjonowanie zakresowe (RANGE)

Dane są przypisywane do partycji na podstawie wartości mieszczącej się w określonym zakresie (np. daty, numery, id). Każda partycja odpowiada innemu przedziałowi.

**Przykład:**

.. code-block:: sql

   CREATE TABLE events (
       event_id serial PRIMARY KEY,
       event_date date NOT NULL,
       description text
   ) PARTITION BY RANGE (event_date);

   CREATE TABLE events_2023 PARTITION OF events
       FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

   CREATE TABLE events_2024 PARTITION OF events
       FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

**Zastosowania:** logi systemowe, zamówienia, dane czasowe.

### 3.2 Partycjonowanie listowe (LIST)

Dane są przypisywane do partycji na podstawie konkretnej wartości z listy (np. kraj, status, kategoria).

**Przykład:**

.. code-block:: sql

   CREATE TABLE sales (
       sale_id serial PRIMARY KEY,
       country text,
       value numeric
   ) PARTITION BY LIST (country);

   CREATE TABLE sales_pl PARTITION OF sales FOR VALUES IN ('Poland');
   CREATE TABLE sales_de PARTITION OF sales FOR VALUES IN ('Germany');
   CREATE TABLE sales_other PARTITION OF sales DEFAULT;

**Zastosowania:** dane geograficzne, statusowe, podział według typu klienta.

### 3.3 Partycjonowanie haszowe (HASH)

Dane są rozdzielane pomiędzy partycje na podstawie funkcji haszującej zastosowanej do wybranej kolumny. Pozwala to równomiernie rozłożyć dane, gdy nie ma logicznego podziału zakresowego ani listowego.

**Przykład:**

.. code-block:: sql

   CREATE TABLE logs (
       log_id serial PRIMARY KEY,
       user_id int,
       log_time timestamp
   ) PARTITION BY HASH (user_id);

   CREATE TABLE logs_p0 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 0);
   CREATE TABLE logs_p1 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 1);
   CREATE TABLE logs_p2 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 2);
   CREATE TABLE logs_p3 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 3);

**Zastosowania:** przypadki wymagające równomiernego rozłożenia danych, np. duże systemy telemetryczne.

### 3.4 Partycjonowanie wielopoziomowe (Composite/Hierarchical Partitioning)

PostgreSQL umożliwia tworzenie partycji podrzędnych, czyli partycjonowanie już partycjonowanych tabel (tzw. subpartitioning).

**Przykład:**

.. code-block:: sql

   CREATE TABLE measurements (
       id serial PRIMARY KEY,
       region text,
       measurement_date date,
       value numeric
   ) PARTITION BY LIST (region);

   CREATE TABLE measurements_europe PARTITION OF measurements
       FOR VALUES IN ('Europe') PARTITION BY RANGE (measurement_date);

   CREATE TABLE measurements_europe_2024 PARTITION OF measurements_europe
       FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

**Zastosowania:** bardzo duże tabele, złożona struktura danych (np. po regionie i dacie).

4. Implementacja partycjonowania w praktyce
-------------------------------------------

### 4.1 Tworzenie i zarządzanie partycjami

- **Tworzenie partycji:** Partycje tworzone są jako osobne tabele, ale zarządzane przez tabelę nadrzędną.
- **Dodawanie partycji:** Możliwe w dowolnym momencie przy użyciu CREATE TABLE ... PARTITION OF.
- **Usuwanie partycji:** ALTER TABLE ... DETACH PARTITION + DROP TABLE (po odłączeniu partycji).
- **Domyślna partycja:** Można zdefiniować partycję przechowującą dane niepasujące do żadnej innej (DEFAULT).

### 4.2 Wstawianie i odczyt danych

- Dane są automatycznie kierowane do właściwej partycji na podstawie klucza partycjonowania.
- W przypadku braku pasującej partycji (i braku DEFAULT) – błąd constraint violation.
- Zapytania ograniczone do klucza partycjonowania korzystają z partition pruning – przeszukują tylko wybrane partycje.

### 4.3 Indeksowanie partycji

- Możliwe jest tworzenie indeksów na każdej partycji osobno lub dziedziczenie indeksów z tabeli nadrzędnej (od PostgreSQL 11 wzwyż).
- Indeksy globalne (na całą tabelę partycjonowaną) nie są jeszcze dostępne (stan na 2025).

### 4.4 Ograniczenia partycjonowania

- Klucz partycjonowania musi być częścią klucza głównego (PRIMARY KEY).
- Niektóre operacje mogą wymagać wykonywania osobno na każdej partycji (np. VACUUM, REINDEX).
- Wersje PostgreSQL <10 obsługują partycjonowanie tylko przez dziedziczenie – obecnie uznawane za przestarzałe.

5. Monitorowanie i administracja
--------------------------------

### 5.1 Sprawdzanie rozmieszczenia danych

.. code-block:: sql

   SELECT tableoid::regclass AS partition, * FROM measurements;

### 5.2 Lista partycji

.. code-block:: sql

   SELECT inhrelid::regclass AS partition
   FROM pg_inherits
   WHERE inhparent = 'measurements'::regclass;

### 5.3 Rozmiar partycji

.. code-block:: sql

   SELECT relname AS "Partition", pg_size_pretty(pg_total_relation_size(relid)) AS "Size"
   FROM pg_catalog.pg_statio_user_tables
   WHERE relname LIKE 'measurements%'
   ORDER BY pg_total_relation_size(relid) DESC;

### 5.4 Analiza planu zapytania (partition pruning)

.. code-block:: sql

   EXPLAIN ANALYZE
   SELECT * FROM measurements WHERE region = 'Europe' AND measurement_date >= '2024-01-01';

   -- W planie widać użycie tylko właściwych partycji.

6. Typowe scenariusze zastosowań
--------------------------------

- **Przetwarzanie danych czasowych:** partycjonowanie zakresowe po dacie (logi, zamówienia, pomiary).
- **Dane geograficzne lub kategoryczne:** partycjonowanie listowe (kraj, region, kategoria produktu).
- **Systemy telemetryczne i IoT:** partycjonowanie haszowe lub wielopoziomowe (np. urządzenie + czas).
- **Duże systemy ERP/CRM:** partycjonowanie po kliencie, regionie, a następnie po dacie.

7. Dobre praktyki projektowania partycji
----------------------------------------

- **Dobór klucza partycjonowania:** Powinien odpowiadać najczęściej używanym warunkom w zapytaniach WHERE.
- **Optymalna liczba partycji:** Zbyt mała liczba partycji nie daje efektu, zbyt duża zwiększa narzut administracyjny.
- **Automatyzacja tworzenia partycji:** Skrypty lub narzędzia generujące nowe partycje np. na kolejne miesiące/lata.
- **Monitorowanie wydajności:** Regularne sprawdzanie rozmiarów partycji, statystyk oraz planów wykonania zapytań.
- **Bezpieczeństwo danych:** Możliwość szybkiego backupu lub usunięcia starych partycji.

8. Ograniczenia i potencjalne problemy
--------------------------------------

- Brak natywnych indeksów globalnych (stan na 2025) utrudnia niektóre zapytania przekrojowe.
- Operacje DDL na tabeli nadrzędnej mogą być kosztowne przy dużej liczbie partycji.
- Niektóre narzędzia zewnętrzne mogą nie obsługiwać partycji w pełni transparentnie.
- Przenoszenie danych między partycjami wymaga operacji INSERT + DELETE lub narzędzi specjalistycznych.

9. Podsumowanie i wnioski
-------------------------

Partycjonowanie danych w PostgreSQL jest zaawansowanym i elastycznym narzędziem, pozwalającym na istotną poprawę wydajności oraz ułatwiającym zarządzanie dużymi zbiorami danych. Właściwy dobór typu partycjonowania, klucza oraz liczby i organizacji partycji wymaga analizy charakterystyki danych i typowych zapytań. Zaleca się regularne monitorowanie i dostosowywanie architektury partycjonowania, zwłaszcza w przypadku dynamicznie rosnących zbiorów danych.

10. Krótkie porównanie partycjonowania w PostgreSQL i innych systemach bazodanowych
-----------------------------------------------------------------------------------

Partycjonowanie danych jest wspierane przez większość nowoczesnych systemów baz danych, jednak szczegóły implementacji i dostępne możliwości mogą się różnić:

- **PostgreSQL:**  
  Umożliwia partycjonowanie zakresowe, listowe, haszowe oraz wielopoziomowe (od wersji 10). Partycje są w pełni zintegrowane z silnikiem (od wersji 10), a operacje na partycjonowanych tabelach są transparentne dla użytkownika. Nie obsługuje jeszcze natywnych indeksów globalnych (stan na 2025).

- **Oracle Database:**  
  Bardzo rozbudowane opcje partycjonowania (RANGE, LIST, HASH, COMPOSITE), obsługuje indeksy lokalne i globalne, automatyczne zarządzanie partycjami, także partycjonowanie na poziomie fizycznym (np. partycjonowanie indeksów, tabel LOB). Mechanizmy zaawansowane, ale często dostępne tylko w płatnych edycjach.

- **MySQL (InnoDB):**  
  Wspiera partycjonowanie RANGE, LIST, HASH, KEY. Możliwości są jednak bardziej ograniczone niż w PostgreSQL czy Oracle. Nie wszystkie operacje i typy indeksów są wspierane na partycjonowanych tabelach.

- **Microsoft SQL Server:**  
  Umożliwia partycjonowanie tabel i indeksów przy użyciu tzw. partition schemes i partition functions. Pozwala na łatwe przenoszenie partycji oraz obsługuje indeksy globalne, co ułatwia optymalizację zapytań przekrojowych.

**Podsumowanie:**  
PostgreSQL oferuje bardzo elastyczne i wydajne partycjonowanie, jednak niektóre zaawansowane funkcje (np. partycjonowanie indeksów globalnych) są jeszcze w fazie rozwoju, podczas gdy w Oracle czy SQL Server są już dojrzałymi rozwiązaniami.

11. Przykład migracji niepartyconowanej tabeli na partycjonowaną
---------------------------------------------------------------

Migracja istniejącej tabeli na partycjonowaną w PostgreSQL wymaga kilku kroków. Oto przykładowy proces dla tabeli ``orders``:

**Załóżmy, że mamy tabelę:**

.. code-block:: sql

   CREATE TABLE orders (
       id serial PRIMARY KEY,
       order_date date NOT NULL,
       customer_id int,
       amount numeric
   );

**Chcemy ją partycjonować po kolumnie ``order_date`` (zakresy roczne):**

1. Zmień nazwę oryginalnej tabeli:

   .. code-block:: sql

      ALTER TABLE orders RENAME TO orders_old;

2. Utwórz nową tabelę partycjonowaną:

   .. code-block:: sql

      CREATE TABLE orders (
          id serial PRIMARY KEY,
          order_date date NOT NULL,
          customer_id int,
          amount numeric
      ) PARTITION BY RANGE (order_date);

      CREATE TABLE orders_2023 PARTITION OF orders
          FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

      CREATE TABLE orders_2024 PARTITION OF orders
          FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

3. Skopiuj dane do partycji:

   .. code-block:: sql

      INSERT INTO orders (id, order_date, customer_id, amount)
      SELECT id, order_date, customer_id, amount FROM orders_old;

4. Sprawdź, czy dane zostały poprawnie rozdzielone:

   .. code-block:: sql

      SELECT tableoid::regclass, COUNT(*) FROM orders GROUP BY tableoid;

5. Usuń starą tabelę po upewnieniu się, że wszystko działa:

   .. code-block:: sql

      DROP TABLE orders_old;

Można też użyć narzędzi automatyzujących migracje (np. pg_partman), jeśli tabel jest bardzo dużo lub są bardzo duże.




12. Bibliografia
----------------

1. Dokumentacja PostgreSQL: https://www.postgresql.org/docs/current/ddl-partitioning.html
2. "PostgreSQL. Zaawansowane techniki programistyczne", Grzegorz Wójtowicz, Helion 2021
3. https://wiki.postgresql.org/wiki/Partitioning
4. Oficjalny blog PostgreSQL: https://www.postgresql.org/about/news/