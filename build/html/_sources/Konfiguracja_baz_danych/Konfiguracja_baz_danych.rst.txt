Sprawozdanie: Konfiguracja i Zarządzanie Bazą Danych
=====================================================

:Authors:        - Piotr Domagała
                 - Piotr Kotuła
                 - Dawid Pasikowski


1. Konfiguracja bazy danych
----------------------------

Wprowadzenie do tematu konfiguracji bazy danych obejmuje podstawowe informacje na temat zarządzania i dostosowywania ustawień baz danych w systemach informatycznych. Konfiguracja ta jest kluczowa dla zapewnienia bezpieczeństwa, wydajności oraz stabilności działania aplikacji korzystających z bazy danych. Obejmuje m.in. określenie parametrów połączenia, zarządzanie użytkownikami, uprawnieniami oraz optymalizację działania systemu bazodanowego.

2. Lokalizacja i struktura katalogów
-------------------------------------

Każda baza danych przechowuje swoje pliki w określonych lokalizacjach systemowych, zależnie od używanego silnika. Przykładowe lokalizacje:

- **PostgreSQL**: ``/var/lib/pgsql/data``
- **MySQL**: ``/var/lib/mysql``
- **SQL Server**: ``C:\Program Files\Microsoft SQL Server``

Struktura katalogów obejmuje katalog główny bazy danych oraz podkatalogi na pliki danych, logi, kopie zapasowe i pliki konfiguracyjne.

**Przykład**: W dużych środowiskach produkcyjnych często stosuje się osobne dyski do przechowywania plików danych i logów transakcyjnych. Takie rozwiązanie pozwala na zwiększenie wydajności operacji zapisu oraz minimalizowanie ryzyka utraty danych.

**Dobra praktyka**: Zaleca się, aby katalogi z danymi i logami były regularnie monitorowane pod kątem dostępnego miejsca na dysku. Przepełnienie któregoś z nich może doprowadzić do zatrzymania pracy bazy danych.

3. Katalog danych
------------------

Jest to miejsce, gdzie fizycznie przechowywane są wszystkie pliki związane z bazą danych, takie jak:
  
- Pliki tabel i indeksów
- Dzienniki transakcji
- Pliki tymczasowe

**Przykładowo**: W PostgreSQL katalog danych to ``/var/lib/pgsql/data``, gdzie znajdują się zarówno pliki z danymi, jak i główny plik konfiguracyjny ``postgresql.conf``.

**Wskazówka**: Dostęp do katalogu danych powinien być ograniczony tylko do uprawnionych użytkowników systemu, co zwiększa bezpieczeństwo i zapobiega przypadkowym lub celowym modyfikacjom plików bazy.

4. Podział konfiguracji na podpliki
------------------------------------

Konfiguracja systemu bazodanowego może być rozbita na kilka mniejszych, wyspecjalizowanych plików, np.:

- ``postgresql.conf`` – główne ustawienia serwera
- ``pg_hba.conf`` – reguły autoryzacji i dostępu
- ``pg_ident.conf`` – mapowanie użytkowników systemowych na użytkowników PostgreSQL

**Przykład**: Jeśli administrator chce zmienić jedynie sposób autoryzacji użytkowników, edytuje tylko plik ``pg_hba.conf``, bez ryzyka wprowadzenia niezamierzonych zmian w innych częściach konfiguracji.

**Dobra praktyka**: Rozdzielenie konfiguracji na podpliki ułatwia zarządzanie, pozwala szybciej lokalizować błędy i minimalizuje ryzyko konfliktów podczas aktualizacji lub wdrażania zmian.

5. Katalog Konfiguracyjny
--------------------------

To miejsce przechowywania wszystkich plików konfiguracyjnych bazy danych, takich jak główny plik konfiguracyjny, pliki z ustawieniami użytkowników, uprawnień czy harmonogramów zadań.

Typowe lokalizacje to:

- ``/etc`` (np. ``my.cnf`` dla MySQL)
- Katalog danych bazy (np. ``/var/lib/pgsql/data`` dla PostgreSQL)

**Przykład**: W przypadku awarii systemu administrator może szybko przywrócić działanie bazy, kopiując wcześniej zapisane pliki konfiguracyjne z katalogu konfiguracyjnego.

**Wskazówka**: Regularne wykonywanie kopii zapasowych katalogu konfiguracyjnego jest kluczowe – utrata tych plików może uniemożliwić uruchomienie bazy danych lub spowodować utratę ważnych ustawień systemowych.

6. Katalog logów i struktura katalogów w PostgreSQL
----------------------------------------------------

**Katalog logów**  
PostgreSQL zapisuje logi w różnych lokalizacjach, zależnie od systemu operacyjnego:
  
- Na Debianie/Ubuntu: ``/var/log/postgresql``
- Na Red Hat/CentOS: ``/var/lib/pgsql/<wersja>/data/pg_log``

> Uwaga: Aby zapisywać logi do pliku, należy upewnić się, że opcja ``logging_collector`` jest włączona w pliku ``postgresql.conf``.

**Struktura katalogów PostgreSQL**:
  
::
  
  base/         # dane użytkownika – jedna podkatalog dla każdej bazy danych
  global/       # dane wspólne dla wszystkich baz (np. użytkownicy)
  pg_wal/       # pliki WAL (Write-Ahead Logging)
  pg_stat/      # statystyki działania serwera
  pg_log/       # logi (jeśli skonfigurowane)
  pg_tblspc/    # dowiązania do tablespace’ów
  pg_twophase/  # dane dla transakcji dwufazowych
  postgresql.conf  # główny plik konfiguracyjny
  pg_hba.conf      # kontrola dostępu
  pg_ident.conf    # mapowanie użytkowników systemowych na bazodanowych

7. Przechowywanie i lokalizacja plików konfiguracyjnych
--------------------------------------------------------

Główne pliki konfiguracyjne:

- ``postgresql.conf`` – konfiguracja instancji PostgreSQL (parametry wydajności, logowania, lokalizacji itd.)
- ``pg_hba.conf`` – kontrola dostępu (adresy IP, użytkownicy, metody autoryzacji)
- ``pg_ident.conf`` – mapowanie użytkowników systemowych na użytkowników bazodanowych

8. Podstawowe parametry konfiguracyjne
---------------------------------------

**Słuchanie połączeń:**

::
  
  listen_addresses = 'localhost'
  port = 5432

**Pamięć i wydajność:**

::
  
  shared_buffers = 512MB         # pamięć współdzielona
  work_mem = 4MB                 # pamięć na operacje sortowania/złączeń
  maintenance_work_mem = 64MB    # dla operacji VACUUM, CREATE INDEX

**Autovacuum:**

::
  
  autovacuum = on
  autovacuum_naptime = 1min

**Konfiguracja pliku** ``pg_hba.conf``:

::
  
  # TYPE  DATABASE  USER  ADDRESS         METHOD
  local   all       all   md5
  host    all       all   192.168.0.0/24  md5

**Konfiguracja pliku** ``pg_ident.conf``:

::
  
  # MAPNAME      SYSTEM-USERNAME   PG-USERNAME
  local_users  ubuntu            postgres
  local_users  jan_kowalski      janek_db

Można użyć tej mapy w pliku ``pg_hba.conf``:
  
::
  
  local   all     all     peer map=local_users

9. Wstęp teoretyczny
---------------------

Systemy zarządzania bazą danych (DBMS – *Database Management System*) umożliwiają tworzenie, modyfikowanie i zarządzanie danymi. Ułatwiają organizację danych, zapewniają integralność, bezpieczeństwo oraz możliwość jednoczesnego dostępu wielu użytkowników.

9.1 Klasyfikacja systemów zarządzania bazą danych
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Systemy DBMS można klasyfikować według:

- **Architektura działania:**
  - *Klient-serwer* – system działa jako niezależna usługa (np. PostgreSQL).
  - *Osadzony (embedded)* – baza danych jest integralną częścią aplikacji (np. SQLite).

- **Rodzaj danych i funkcjonalność:**
  - *Relacyjne (RDBMS)* – oparte na tabelach, kluczach i SQL.
  - *Nierelacyjne (NoSQL)* – oparte na dokumentach, modelu klucz-wartość lub grafach.

Oba systemy – **SQLite** oraz **PostgreSQL** – należą do relacyjnych baz danych, lecz różnią się architekturą, wydajnością, konfiguracją i przeznaczeniem.

9.2 SQLite
~~~~~~~~~~~

SQLite to lekka, bezserwerowa baza danych typu embedded, gdzie cała baza znajduje się w jednym pliku. Dzięki temu jest bardzo wygodna przy tworzeniu aplikacji lokalnych, mobilnych oraz projektów prototypowych.

**Cechy SQLite:**
  
- Brak osobnego procesu serwera – baza działa w kontekście aplikacji.
- Niskie wymagania systemowe – brak potrzeby instalacji i konfiguracji.
- Baza przechowywana jako pojedynczy plik (*.sqlite* lub *.db*).
- Pełna obsługa SQL (z pewnymi ograniczeniami) – wspiera standard SQL-92.
- Ograniczona skalowalność przy wielu użytkownikach.

**Zastosowanie:**
  
- Aplikacje desktopowe (np. Firefox, VS Code).
- Aplikacje mobilne (Android, iOS).
- Małe i średnie systemy bazodanowe.

9.3 PostgreSQL
~~~~~~~~~~~~~~~

PostgreSQL to zaawansowany system relacyjnej bazy danych typu klient-serwer, rozwijany jako projekt open-source. Zapewnia pełne wsparcie dla SQL oraz liczne rozszerzenia (np. typy przestrzenne, JSON).

**Cechy PostgreSQL:**
  
- Architektura klient-serwer – działa jako oddzielny proces.
- Wysoka skalowalność i niezawodność – obsługuje wielu użytkowników, złożone zapytania, replikację.
- Obsługa transakcji, MVCC, indeksowania oraz zarządzania uprawnieniami.
- Rozszerzalność – możliwość definiowania własnych typów danych, funkcji i procedur.

**Konfiguracja:**  
Plikami konfiguracyjnymi są:
  
- ``postgresql.conf`` – ustawienia ogólne (port, ścieżki, pamięć, logi).
- ``pg_hba.conf`` – reguły autoryzacji.
- ``pg_ident.conf`` – mapowanie użytkowników systemowych na bazodanowych.

**Zastosowanie:**
  
- Systemy biznesowe, bankowe, analityczne.
- Aplikacje webowe i serwery aplikacyjne.
- Środowiska o wysokich wymaganiach bezpieczeństwa i kontroli dostępu.

9.4 Cel użycia obu systemów
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

W ramach zajęć wykorzystano zarówno **SQLite** (dla szybkiego startu i analizy zapytań bez instalacji serwera), jak i **PostgreSQL** (dla nauki konfiguracji, zarządzania użytkownikami, uprawnieniami oraz obsługi złożonych operacji).

10. Zarządzanie konfiguracją w PostgreSQL
------------------------------------------

PostgreSQL oferuje rozbudowany i elastyczny mechanizm konfiguracji, umożliwiający precyzyjne dostosowanie działania bazy danych do potrzeb użytkownika oraz środowiska (lokalnego, deweloperskiego, testowego czy produkcyjnego).

10.1 Pliki konfiguracyjne
~~~~~~~~~~~~~~~~~~~~~~~~~~

Główne pliki konfiguracyjne PostgreSQL:
  
- **postgresql.conf** – ustawienia dotyczące pamięci, sieci, logowania, autovacuum, planowania zapytań.
- **pg_hba.conf** – definiuje metody uwierzytelniania i dostęp z określonych adresów.
- **pg_ident.conf** – mapowanie nazw użytkowników systemowych na użytkowników PostgreSQL.

Pliki te zazwyczaj znajdują się w katalogu danych (np. ``/var/lib/postgresql/15/main/`` lub ``/etc/postgresql/15/main/``).

10.2 Przykładowe kluczowe parametry ``postgresql.conf``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1

   * - **Parametr**
     - **Opis**
   * - shared_buffers
     - Ilość pamięci RAM przeznaczona na bufor danych (rekomendacja: 25–40% RAM).
   * - work_mem
     - Pamięć dla pojedynczej operacji zapytania (np. sortowania).
   * - maintenance_work_mem
     - Pamięć dla operacji administracyjnych (np. VACUUM, CREATE INDEX).
   * - effective_cache_size
     - Szacunkowa ilość pamięci dostępnej na cache systemu operacyjnego.
   * - max_connections
     - Maksymalna liczba jednoczesnych połączeń z bazą danych.
   * - log_directory
     - Katalog, w którym zapisywane są logi PostgreSQL.
   * - autovacuum
     - Włącza lub wyłącza automatyczne odświeżanie nieużywanych wierszy.

10.3 Sposoby zmiany konfiguracji
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Edycja pliku** ``postgresql.conf``  
   
   Zmiany są trwałe, ale wymagają restartu serwera (w niektórych przypadkach wystarczy reload).

   **Przykład:**
   
   ::
      
      shared_buffers = 512MB
      work_mem = 64MB

2. **Dynamiczna zmiana poprzez SQL**

   **Przykład:**
   
   ::
      
      ALTER SYSTEM SET work_mem = '64MB';
      SELECT pg_reload_conf();  # ładowanie zmian bez restartu

3. **Tymczasowa zmiana dla jednej sesji**

   **Przykład:**
   
   ::
      
      SET work_mem = '128MB';

10.4 Sprawdzanie konfiguracji
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Aby sprawdzić aktualną wartość parametru:
  
  ::
      
      SHOW work_mem;

- Pobranie szczegółowych informacji:
  
  ::
      
      SELECT name, setting, unit, context, source
      FROM pg_settings
      WHERE name = 'work_mem';

- Wylistowanie parametrów wymagających restartu serwera:
  
  ::
      
      SELECT name FROM pg_settings WHERE context = 'postmaster';

10.5 Narzędzia pomocnicze
~~~~~~~~~~~~~~~~~~~~~~~~~~

- **pg_ctl** – narzędzie do zarządzania serwerem (start/stop/reload).
- **psql** – klient terminalowy PostgreSQL do wykonywania zapytań oraz operacji administracyjnych.
- **pgAdmin** – graficzne narzędzie do zarządzania bazą PostgreSQL (umożliwia edycję konfiguracji przez GUI).

10.6 Kontrola dostępu i mechanizmy uwierzytelniania
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Konfiguracja umożliwia określenie, z jakich adresów i w jaki sposób można łączyć się z bazą:
  
- **Dostęp lokalny (localhost)** – połączenia z tej samej maszyny.
- **Dostęp z podsieci** – administrator może wskazać konkretne podsieci IP (np. ``192.168.0.0/24``).
- **Mechanizmy uwierzytelniania** – np. ``md5``, ``scram-sha-256``, ``peer`` (weryfikacja użytkownika systemowego) czy ``trust``.

Ważne, aby mechanizm ``peer`` był odpowiednio skonfigurowany, gdyż umożliwia automatyczną autoryzację, jeśli nazwa użytkownika systemowego i bazy zgadza się.

11. Planowanie
---------------

Planowanie w kontekście PostgreSQL oznacza optymalizację wykonania zapytań oraz efektywne zarządzanie zasobami.

11.1 Co to jest planowanie zapytań?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Proces planowania zapytań obejmuje:
  
- Analizę składni i struktury zapytania SQL.
- Przegląd dostępnych statystyk dotyczących tabel, indeksów i danych.
- Dobór sposobu dostępu do danych (pełny skan, indeks, join, sortowanie).
- Tworzenie planu wykonania, czyli sekwencji operacji potrzebnych do uzyskania wyniku.

Administrator może również kontrolować częstotliwość aktualizacji statystyk (np. ``default_statistics_target``, ``autovacuum``).

11.2 Mechanizm planowania w PostgreSQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PostgreSQL wykorzystuje kosztowy optymalizator; przy użyciu statystyk (liczby wierszy, rozkładu danych) szacuje „koszt” różnych metod wykonania zapytania, wybierając tę, która jest najtańsza pod względem czasu i zasobów.

11.3 Statystyki i ich aktualizacja
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Statystyki są tworzone przy pomocy polecenia ``ANALYZE`` – zbiera dane o rozkładzie wartości kolumn.
- Mechanizm autovacuum odświeża statystyki automatycznie.

**Przykład:**
  
::
  
    ANALYZE [nazwa_tabeli];

W systemach o dużym obciążeniu planowanie uwzględnia również równoległość (parallel query).

11.4 Typy planów wykonania
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Przykładowe typy planów wykonania:
  
- **Seq Scan** – pełny skan tabeli (gdy indeksy są niedostępne lub nieefektywne).
- **Index Scan** – wykorzystanie indeksu.
- **Bitmap Index Scan** – łączenie efektywności indeksów ze skanem sekwencyjnym.
- **Nested Loop Join** – efektywny join dla małych zbiorów.
- **Hash Join** – buduje tablicę hash dla dużych zbiorów.
- **Merge Join** – stosowany, gdy dane są posortowane.

11.5 Jak sprawdzić plan zapytania?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aby zobaczyć plan wybrany przez PostgreSQL, można użyć:
  
::
  
    EXPLAIN ANALYZE SELECT * FROM tabela WHERE kolumna = 'wartość';

- ``EXPLAIN`` – wyświetla plan bez wykonania zapytania.
- ``ANALYZE`` – wykonuje zapytanie i podaje rzeczywiste czasy wykonania.

**Przykładowy wynik:**
  
::
  
    Index Scan using idx_kolumna on tabela (cost=0.29..8.56 rows=3 width=244)
    Index Cond: (kolumna = 'wartość'::text)

11.6 Parametry planowania i optymalizacji
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

W pliku ``postgresql.conf`` można konfigurować m.in.:
  
- ``random_page_cost`` – koszt odczytu strony z dysku SSD/HDD.
- ``cpu_tuple_cost`` – koszt przetwarzania pojedynczego wiersza.
- ``enable_seqscan``, ``enable_indexscan``, ``enable_bitmapscan`` – włączanie/wyłączanie konkretnych typów skanów.

Dostosowanie tych parametrów pozwala zoptymalizować planowanie zgodnie ze specyfiką sprzętu i obciążenia.

12. Tabele – rozmiar, planowanie i monitorowanie
-------------------------------------------------

12.1 Rozmiar tabeli
~~~~~~~~~~~~~~~~~~~~

Rozmiar tabeli w PostgreSQL obejmuje dane (wiersze), strukturę, indeksy, dane TOAST oraz pliki statystyk. Do monitorowania rozmiaru stosuje się funkcje:
  
- ``pg_relation_size()`` – rozmiar tabeli lub pojedynczego indeksu.
- ``pg_total_relation_size()`` – całkowity rozmiar tabeli wraz z indeksami i TOAST.

12.2 Planowanie rozmiaru i jego kontrola
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Podczas projektowania bazy danych należy oszacować potencjalny rozmiar tabel, biorąc pod uwagę liczbę wierszy i rozmiar pojedynczego rekordu. PostgreSQL nie posiada sztywnego limitu (poza ograniczeniami systemu plików i 32-bitowym limitem liczby stron). Parametr ``fillfactor`` może być stosowany do optymalizacji częstotliwości operacji UPDATE i VACUUM.

12.3 Monitorowanie rozmiaru tabel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Przykład zapytania:**
  
::
  
    SELECT pg_size_pretty(pg_total_relation_size('nazwa_tabeli'));

Inne funkcje:
  
- ``pg_relation_size`` – rozmiar samej tabeli.
- ``pg_indexes_size`` – rozmiar indeksów.
- ``pg_table_size`` – zwraca łączny rozmiar tabeli wraz z TOAST.

12.4 Planowanie na poziomie tabel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Administrator może wpływać na fizyczne rozmieszczenie danych poprzez:
  
- **Tablespaces** – przenoszenie tabel lub indeksów na inne dyski/partycje.
- **Podział tabel (partitioning)** – rozbijanie dużych tabel na mniejsze części.

12.5 Monitorowanie stanu tabel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Monitorowanie obejmuje:
  
- Śledzenie fragmentacji danych.
- Kontrolę wzrostu tabel i indeksów.
- Statystyki dotyczące operacji odczytów i zapisów.

Narzędzia i widoki systemowe:
  
- ``pg_stat_all_tables``
- ``pg_stat_user_tables``
- ``pg_stat_activity``

12.6 Konserwacja i optymalizacja tabel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Regularne uruchamianie poleceń:
  
- **VACUUM** – usuwa martwe wiersze, zapobiegając nadmiernej fragmentacji.
- **ANALYZE** – aktualizuje statystyki, ułatwiając optymalizację zapytań.

Dla bardzo dużych tabel można stosować ``VACUUM FULL`` lub reorganizację danych, aby odzyskać przestrzeń.

13. Rozmiar pojedynczych tabel, rozmiar wszystkich tabel, indeksów tabeli
--------------------------------------------------------------------------

Efektywne zarządzanie rozmiarem tabel oraz ich indeksów ma kluczowe znaczenie dla wydajności systemu.

13.1 Rozmiar pojedynczej tabeli
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Do pozyskania informacji o rozmiarze konkretnej tabeli służą funkcje:
  
- ``pg_relation_size('nazwa_tabeli')`` – rozmiar danych tabeli (w bajtach).
- ``pg_table_size('nazwa_tabeli')`` – rozmiar danych tabeli wraz z danymi TOAST.
- ``pg_total_relation_size('nazwa_tabeli')`` – całkowity rozmiar tabeli wraz z indeksami i TOAST.

**Przykład zapytania:**
  
::
  
    SELECT
      pg_size_pretty(pg_relation_size('nazwa_tabeli')) AS data_size,
      pg_size_pretty(pg_indexes_size('nazwa_tabeli')) AS indexes_size,
      pg_size_pretty(pg_total_relation_size('nazwa_tabeli')) AS total_size;

13.2 Rozmiar wszystkich tabel w bazie
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Zapytanie pozwalające wylistować wszystkie tabele i ich rozmiary:
  
::
  
    SELECT
      schemaname,
      relname AS table_name,
      pg_size_pretty(pg_total_relation_size(relid)) AS total_size
    FROM
      pg_catalog.pg_statio_user_tables
    ORDER BY
      pg_total_relation_size(relid) DESC;

13.3 Rozmiar indeksów tabeli
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Funkcja:
  
::
  
    pg_indexes_size('nazwa_tabeli')

Pozwala sprawdzić rozmiar wszystkich indeksów przypisanych do danej tabeli. Monitorowanie indeksów pomaga w podejmowaniu decyzji o ich przebudowie lub usunięciu.

13.4 Znaczenie rozmiarów
~~~~~~~~~~~~~~~~~~~~~~~~~

Duże tabele i indeksy mogą powodować:
  
- Wolniejsze operacje zapisu i odczytu.
- Wydłużony czas tworzenia kopii zapasowych.
- Większe wymagania przestrzeni dyskowej.

Regularne monitorowanie rozmiaru umożliwia planowanie działań optymalizacyjnych i konserwacyjnych.

14. Rozmiar
------------

Pojęcie „rozmiar” odnosi się do przestrzeni dyskowej zajmowanej przez elementy bazy danych – tabele, indeksy, pliki TOAST, a także całe bazy danych lub schematy.

14.1 Rodzaje rozmiarów w PostgreSQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Rozmiar pojedynczego obiektu** (tabeli, indeksu):  
  Funkcje takie jak ``pg_relation_size()``, ``pg_table_size()``, ``pg_indexes_size()`` oraz ``pg_total_relation_size()``.
- **Rozmiar schematu lub bazy danych**:  
  Funkcje ``pg_namespace_size('nazwa_schematu')`` oraz ``pg_database_size('nazwa_bazy')``.
- **Rozmiar plików TOAST**:  
  Duże wartości (np. teksty, obrazy) są przenoszone do struktur TOAST, których rozmiar wliczany jest do rozmiaru tabeli, choć można go analizować osobno.

14.2 Monitorowanie i kontrola rozmiaru
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Administratorzy baz danych powinni regularnie monitorować rozmiar baz danych i jej obiektów, aby:
  
- Zapobiegać przekroczeniu limitów przestrzeni dyskowej.
- Wcześniej wykrywać problemy z fragmentacją.
- Planować archiwizację lub czyszczenie danych.

Do monitoringu można wykorzystać zapytania SQL lub narzędzia zewnętrzne (np. pgAdmin, pgBadger).

14.3 Optymalizacja rozmiaru
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Działania optymalizacyjne obejmują:
  
- **Reorganizację i VACUUM**: odzyskiwanie przestrzeni po usuniętych lub zaktualizowanych rekordach oraz poprawa statystyk.
- **Partycjonowanie tabel**: dzielenie dużych tabel na mniejsze, co ułatwia zarządzanie.
- **Ograniczenia i typy danych**: odpowiedni dobór typów danych (np. ``varchar(n)`` zamiast ``text``) oraz stosowanie ograniczeń (np. CHECK) zmniejsza rozmiar danych.

14.4 Znaczenie zarządzania rozmiarem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Niewłaściwe zarządzanie przestrzenią dyskową może prowadzić do:
  
- Spowolnienia działania bazy.
- Problemów z backupem i odtwarzaniem.
- Wzrostu kosztów utrzymania infrastruktury.

Podsumowanie
-------------

Zarządzanie konfiguracją bazy danych PostgreSQL, optymalizacja zapytań oraz monitorowanie i konserwacja tabel stanowią fundament skutecznego zarządzania systemem bazodanowym. Prawidłowe podejście do tych elementów zapewnia wysoką wydajność, niezawodność i skalowalność systemu.

---
