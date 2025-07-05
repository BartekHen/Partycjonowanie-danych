Kontrola i konserwacja baz danych
---------------------------------

Wprowadzenie
~~~~~~~~~~~~

Autor: Bartłomiej Czyż

Systemy baz danych są niezwykle ważnym elementem infrastruktury informatycznej współczesnych organizacji. Umożliwiają przechowywanie, zarządzanie i analizę danych w sposób bezpieczny oraz wydajny. Aby zapewnić ich niezawodność, integralność i wysoką dostępność, konieczne jest prowadzenie regularnych działań z zakresu kontroli i konserwacji. Działania te można podzielić na część fizyczną oraz część programową, a sposób ich przeprowadzania różni się w zależności od rodzaju i architektury używanej bazy danych.

Podział konserwacji baz danych
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Autor: Bartłomiej Czyż

Konserwacja fizyczna
^^^^^^^^^^^^^^^^^^^^

Konserwacja fizyczna obejmuje wszystkie działania związane z infrastrukturą sprzętową i zasobami systemowymi, na których działa baza danych. Do najważniejszych elementów tej konserwacji należą:

- Monitorowanie stanu dysków twardych – pozostała przestrzeń na dyskach, zużycie dysków oraz fragmentacja danych,

- Zabezpieczenie fizyczne serwerów – kontrola dostępu, ochrona przeciwpożarowa, klimatyzacja,

- Zasilanie awaryjne (UPS) - zabezpieczenie bazy przed skutkami nagłego zaniku zasilania,

- Monitoring stanu sieci – wydajność i stabilność połączenia między bazą a klientami,

- Tworzenie kopii zapasowych na nośnikach fizycznych – np. dyskach zewnętrznych czy taśmach LTO.

Konserwacja programowa
^^^^^^^^^^^^^^^^^^^^^^

Konserwacja programowa odnosi się do czynności wykonywanych na poziomie oprogramowania i logiki działania systemu bazy danych. Obejmuje:

- Zarządzanie użytkownikami i ich uprawnieniami,

- Optymalizację zapytań SQL,

- Aktualizację oprogramowania bazodanowego (np. MySQL, PostgreSQL),

- Defragmentację indeksów,

- Weryfikację integralności danych i naprawę uszkodzonych rekordów,

- Automatyczne zadania konserwacyjne (cron, schedulery),

- Reduplikację i redundancję - konfiguracja serwerów zapasowych.

Różnice konserwacyjne w zależności od rodzaju bazy danych
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Autor: Bartłomiej Czyż

PostgreSQL
^^^^^^^^^^

PostgreSQL to zaawansowany system RDBMS, znany z silnego wsparcia dla różnych typów danych i transakcyjności.

1. Fizyczna konserwacja:
	
	- Złożona struktura katalogów danych (base, pg_wal, pg_tblspc) – wymaga regularnego monitoringu,

	- Możliwość wykorzystania narzędzia pg_basebackup do tworzenia pełnych kopii fizycznych.

2. Programowa konserwacja:
	
	- Automatyczne zadania VACUUM, ANALYZE – zapewniają odzyskiwanie przestrzeni po usunięciu rekordów,

	- Możliwość używania pg_repack do defragmentacji bez przestojów,

	- Silne wsparcie dla replikacji strumieniowej i klastrów wysokiej dostępności (HA).

MySQL
^^^^^

MySQL jest obecnie jedną z najpopularniejszych relacyjnych baz danych, szeroko stosowana w aplikacjach webowych.

1. Fizyczna konserwacja:

	- Wymaga monitorowania plików .ibd (w przypadku silknika InnoDB), które mogą znacznie rosnąć,

	- Backup danych realizowany poprzez mysqldump lub system replikacji binlogów.

2. Programowa konserwacja:

	- Regularne sprawdzanie indeksów (ANALYZE TABLE, OPTIMIZE TABLE),

	- Używanie narzędzi typu mysqlcheck do weryfikacji i naprawy tabel,

	- Konfiguracja pliku my.cnf w celu dostosowania do wymagań aplikacji.

SQLite (np. LightSQL)
^^^^^^^^^^^^^^^^^^^^^

SQLite, używana w aplikacjach mobilnych i desktopowych, różni się znacznie od serwerowych baz danych.

1. Fizyczna konserwacja:

	- Brak klasycznego serwera – baza to pojedynczy plik .db,

	- Konieczność regularnego kopiowania pliku bazy danych jako backup.

2. Programowa konserwacja:
	
	- Użycie polecenia VACUUM do defragmentacji i zmniejszenia rozmiaru pliku,

	- Ograniczone możliwości równoczesnego dostępu – wymaga uwagi w aplikacjach wielowątkowych,

	- Nie wymaga osobnych usług do zarządzania – działa bezpośrednio w aplikacji.

Microsoft SQL Server
^^^^^^^^^^^^^^^^^^^^

System korporacyjny, szeroko wykorzystywany w dużych organizacjach.

1. Fizyczna konserwacja:

	- Obsługuje macierze RAID i pamięci masowe SAN,

	- Regularne kopie pełne, różnicowe i dzienniki transakcyjne.

2. Programowa konserwacja:

	- Zaawansowany SQL Server Agent – możliwość harmonogramowania zadań,

	- Narzędzia do monitorowania stanu instancji (SQL Profiler, Database Tuning Advisor),

	- Wsparcie dla Always On Availability Groups dla wysokiej dostępności.

Planowanie konserwacji bazy danych
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Autor: Piotr Mikołajczyk

Konserwację bazy danych należy przeprowadzać regularnie, np. co tydzień lub co miesiąc. Nie powinna mieć miejsca w godzinach szczytu. Przeprowadzenie konserwacji może również okazać się koniecznie po wykryciu błędu lub wystąpieniu awarii.

Konserwacja może obejmować m.in. zmianę parametrów konfiguracji bazy, przeprowadzenie procesu VACUUM, zmianę uprawnien użytkowników, aktualizacje systemowe i wykonanie backupów lub przywrócenie danych.

Działanie te muszą zostać przeprowadzone w czasie, gdy mamy pewność, że żaden klient nie będzie podłączony, nie będą przeprowadzane żadne transakcje. Użytkownicy powinni być uprzednio poinformowani o czasie przeprowadzenia konserwacji. Mimo to, należy wcześniej sprawdzić, czy nie ma aktywnych sesji.

Uruchamianie, zatrzymywanie i restartowanie serwera bazy danych
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Autor: Piotr Mikołajczyk

Działania, takie jak aktualizacja oprogramowania, instalacja rozszerzeń, wprowadzenie pewnych zmian w plikach konfiguracyjnych, migracja danych, wykonanie backupów bazy, wymagają zrestartowania, zatrzymania bądź ponownego uruchomienia serwera bazy danych.

Uruchamianie
^^^^^^^^^^^^

Linux:

.. code-block:: bash

	sudo systemctl start postgresql

Windows CMD:

.. code-block:: batch

	net start postgresql-x64-15


Windows PowerShell

.. code-block:: powershell

	Start-Service -Name postgresql-x64-15

Zatrzymywanie
^^^^^^^^^^^^^

Linux:

.. code-block:: bash

	sudo systemctl stop postgresql

Windows CMD:

.. code-block:: batch

	net stop postgresql-x64-15


Windows PowerShell

.. code-block:: powershell

	Stop-Service -Name postgresql-x64-15

Restartowanie
^^^^^^^^^^^^^

Linux:

.. code-block:: bash

	sudo systemctl restart postgresql

W CMD nie istnieje osobne polecenie restartowania. Należy zatrzymać serwer, a następnie uruchomić go ponownie.

Windows PowerShell

.. code-block:: powershell

	Restart-Service -Name postgresql-x64-15

Polecenia CMD mogą zostać również użyte w PowerShell.

Zarządzanie połączeniami użytkowników
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Autor: Piotr Mikołajczyk

Oprócz sytuacji, gdy trzeba zamknąć dostęp do bazy danych na czas konserwacji, połączenia użytkowników należy ograniczyć także wtedy, gdy sesja użytkownika została zawieszona lub zbyt wiele połączeń skutkuje nadmiernym zużyciem pamięci i mocy obliczeniowej, uniemożliwiając nawiązywanie nowych połączeń i spowolniając działanie serwera.

Ograniczanie użytkowników
^^^^^^^^^^^^^^^^^^^^^^^^^

Istnieje kilka sposobów ograniczenia dostępu użytkownika:

- Odebranie użytkownikowi prawa dostępu do bazy:

	.. code-block:: sql

		REVOKE CONNECT ON DATABASE baza FROM user;

- Limit liczby jednoczesnych połączeń:

	.. code-block:: sql

		ALTER ROLE user CONNECTION LIMIT 3;

Ręczne rozłączanie użytkowników
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Według nazwy danego użytkownika:

	.. code-block:: sql

		SELECT pg_terminate_backend(pid)
		FROM pg_stat_activity
		WHERE usename = 'user';

Według PID (np. 12340):

	.. code-block:: sql

		SELECT pg_terminate_backend(12340);

Automatyczne rozłączanie użytkowników
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sesja użytkownika lub jego zapytania mogą zostać rozłączone automatycznie, jeśli wprowadzimy pewne ograniczenia czasowe:

- Rozłączenie sesji po przekroczeniu limitu czasu bezczynności podczas zapytania:

	- dla bieżącej sesji:

		.. code-block:: sql

			SET idle_in_transaction_session_timeout = '5min';

	- dla danego użytkownika:

		.. code-block:: sql

			ALTER ROLE user SET idle_in_transaction_session_timeout = '5min';

- Limit czasu zapytania:

	.. code-block:: sql

		ALTER ROLE user SET statement_timeout = '30s';

Zapobieganie nowym połączeniom
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Zablokowanie logowania konkretnego użytkownika:

	.. code-block:: sql

		ALTER ROLE user NOLOGIN;

	Odblokowanie:

	.. code-block:: sql

		ALTER ROLE user LOGIN;

Blokowanie nowych połączeń do bazy danych:

	.. code-block:: sql

		REVOKE CONNECT ON DATABASE baza FROM PUBLIC;
	
	PUBLIC oznacza wszystkich użytkowników. Nadal połączeni użytkownicy nie są rozłączani.

Proces VACUUM
~~~~~~~~~~~~~

Autor: Piotr Mikołajczyk

DELETE nie usuwa rekordów z tabeli, jedynie oznacza je jako martwe. Podobnie UPDATE pozostawia stare wersje zaktualizowanych krotek.

Proces VACUUM przeszukuje tabele i indeksy, szukając martwych wierszy, które można fizycznie usunąć lub oznaczyć do nadpisania.

Może zostać przeprowadzony na kilka sposobów:

.. code-block:: sql

	VACUUM;

Usuwa martwe krotki, ale nie odzyskuje miejsca z dysku, a jedynie udostępnia je dla przyszłych danych,

.. code-block:: sql

	VACUUM FULL;

Kompaktuje tabelę do nowego pliku, zwalnia miejsce w pamięci,

.. code-block:: sql

	VACUUM ANALYZE

Usuwa martwe krotki i przeprowadza aktualizację statystyk, nie odzyskuje miejsca.

Autovacuum
^^^^^^^^^^

Autovacuum działa w tle, automatycznie wykonując VACUUM na odpowiednich tabelach. Dzięki niemu nie trzeba ręcznie uruchamiać VACUUM po każdej modyfikacji tabeli. Autovacuum posiada wiele parametrów, od których zależy kiedy wykonany zostanie proces, między innymi:

- autovacuum - parametr logiczny, decyduje, czy serwer będzie uruchamiał launcher procesu autovacuum,

- autovacuum_max_workers - liczba całkowita, określa maksymalną ilość procesów autovacuum mogących działać w tym samym czasie, domyślnie 3,

- autovacuum_vacuum_threshold - liczba całkowita, określa ile wierszy w jednej tabeli musi zostać usunięte lub zmienione, aby wywołano VACUUM, domyślnie 50,

- autovacuum_vacuum_scale_factor - liczba zmiennoprzecinkowa, jaki procent tabeli musi zostać zmieniony aby wywołano VACUUM, domyślna wartość to 0.2 (20%).

Analogiczne parametry warunkują również wywołanie ANALYZE, na przykład autovacuum_analyze_threshold.

Próg uruchamiania VACUUM ustala się wzorem:

	autovacuum_vacuum_threshold + autovacuum_vacuum_scale_factor * liczba_wierszy
	
Podobnie dla ANALYZE:

	autovacuum_analyze_threshold + autovacuum_analyze_scale_factor * liczba_wierszy

Schemat bazy danych
~~~~~~~~~~~~~~~~~~~

Autor: Bartłomiej Czyż

Czym jest schemat bazy danych?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Schemat bazy danych to logiczna struktura opisująca organizację danych, typy danych, relacje między tabelami, ograniczenia integralności, procedury składowane, widoki i inne obiekty. Innymi słowy, schemat jest "szkieletem" bazy danych.

Przykładowe elementy schematu:

- Tabele (np. users, orders),

- Typy danych (np. INT, VARCHAR, DATE),

- Klucze główne i obce,

- Indeksy,

- Widoki (VIEW),

- Procedury i funkcje (STORED PROCEDURES),

- Ograniczenia (CHECK, NOT NULL, UNIQUE).

Rola schematu w konserwacji bazy danych
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Schemat ma kluczowe znaczenie dla utrzymania spójności i integralności danych, dlatego jego kontrola i konserwacja obejmuje m.in.:

- Dokumentację schematu - niezbędna przy aktualizacjach i migracjach,

- Weryfikację integralności relacji - sprawdzenie czy klucze obce i reguły są respektowane,

- Normalizację - kontrola nad nadmiarem danych i poprawnością logiczną,

- Aktualizacje schematu - np. dodawanie nowych kolumn, zmiana typu danych,

- Kontrola zgodności - wersjonowanie schematu (np. za pomocą narzędzi typu Liquibase, Flyway),

- Zabezpieczenia schematów - nadawanie uprawnień tylko zaufanym użytkownikom.

Przykład konserwacji:

W PostgreSQL można analizować i optymalizować strukturę przy pomocy pgAdmin oraz narzędzi takich jak pg_dump --schema-only.

Różnice w implementacji schematu w różnych systemach
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- MySQL - obsługuje wiele schematów w jednej bazie; ograniczone typy kolumn w starszych wersjach,

- PostgreSQL - bardzo elastyczny system schematów - możliwość teorzenia przestrzeni nazw,

- SQLite - pojedynczy schemat, uproszczony system typów,

- SQL Server - schemat jako logiczna przestrzeń obiektów, np. dbo, hr, finance.

Transakcje
~~~~~~~~~~

Autor: Bartłomiej Czyż

Czym jest transakcja?
^^^^^^^^^^^^^^^^^^^^^

Transakcja to zbiór operacji na bazie danych, które są traktowane jako jedna, nierozdzielna całość. Albo wykonują się wszystkie operacje, albo żadna - zasada atomiczności. Transakcje są podstawą do zachowania spójności danych, szczególnie w środowiskach wieloużytkownikowych.

Zasady ACID
^^^^^^^^^^^

Transakcje w bazach danych opierają się na czterech podstawowych zasadach, znanych jako ACID:

- A - Atomicity (Atomowość) - operacje wchodzące w skład transakcji są niepodzielne - wszystkie muszą się powieść, lub wszystkie są wycofywane,

- C - Consistency (Spójność) - transakcje przekształcają dane ze stanu spójnego w stan spójny,

- I - Isolation (Izolacja) - równoczesne transakcje nie wpływają na siebie nawzajem,

- D - Durability (Trwałość) - po zatwierdzeniu transakcji dane są trwale zapisane, nawet w przypadku awarii.

Rola transakcji w kontroli i konserwacji
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Transakcje mają ogromne znaczenie dla bezpieczeństwa danych, dlatego są nieodłącznym elementem procesów konserwacyjnych. Ich zastosowanie obejmuje:

- Zabezpieczenie operacji aktualizacji - np. przy masowych zmianach danych,

- Replikacja i synchronizacja danych - transakcje zapewniają spójność między główną bazą, a replikami,

- Zarządzanie błędami - w przypadku błędu można wykonać ROLLBACK i przywrócić stan bazy,

- Tworzenie backupów spójnych z punktu w czasie - snapshoty danych często wymagają wsparcia transakcyjnego,

- Ochrona przed uszkodzeniami logicznymi - np. przez niekompletne aktualizacje.

Różnice w implementacji transakcji w różnych systemach
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- MySQL - w pełni wspierane w silniku InnoDB; START TRANSACTION, COMMIT, ROLLBACK,

- PostgreSQL - silne wsparcie ACID, zaawansowana izolacja (REPEATABLE READ, SERIALIZABLE),

- SQLite - transakcje działają w trybie plikowym; BEGIN, COMMIT i ROLLBACK są wspierane,

- SQL Server - zaawansowany mechanizm transakcji z kontrolą poziomów izolacji, także eksplicytny SAVEPOINT.

Literatura
~~~~~~~~~~

- `Oficjalna dokumentacja PostgreSQL <https://www.postgresql.org/docs/current/index.html>`_

- Riggs S., Krosing H., PostgreSQL. Receptury dla administratora, Helion 2011

- Matthew N., Stones R., Beginning Databases with PostgreSQL. From Novice to Professional, Apress 2006

- Juba S., Vannahme A., Volkov A., Learning PostgreSQL, Packt Publishing 2015
