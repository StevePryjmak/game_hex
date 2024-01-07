# Dokumentacja Gry Hex

## Dane autora
- **Autor**: Pryimak Andrii-Stepan
- **Kontakt**: andrii-stepan.pryimak.stud@pw.edu.pl

## Opis Gry
Gra Hex to strategiczna gra planszowa dla dwóch graczy. Celem gry jest połączenie dwóch przeciwległych stron planszy za pomocą nieprzerwanego łańcucha swoich kamieni. Gracze używają kamieni w dwóch kolorach, zazwyczaj czerwonym i niebieskim, i na przemian umieszczają je na planszy.

## Zasady Gry
1. **Start**: Gracze rozpoczynają na pustej planszy hexagonalnych komórek.
2. **Ruchy**: Gracze na przemian umieszczają kamienie swojego koloru.
3. **Cel**: Celem jest połączenie przeciwległych stron planszy.
4. **Zakończenie**: Gracz, który pierwszy połączy swoje strony, wygrywa.

## Strategia
Gra Hex wymaga przewidywania ruchów przeciwnika i planowania własnych, aby skutecznie zablokować przeciwnika i stworzyć nieprzerwane połączenie.



## Struktura Projektu

Projekt zawiera kilka kluczowych folderów i plików, które współpracują, aby zapewnić pełną funkcjonalność gry.

### Folder `classes`
Ten folder zawiera moduły z definicjami klas wykorzystywanych w grze Hex. Każdy moduł odpowiada za różne aspekty logiki gry:

- `gui`: Moduły interfejsu użytkownika, które zarządzają wyświetlaniem elementów gry.
  - `button.py`: Klasa `Button` odpowiada za tworzenie i zarządzanie przyciskami w grze.
  - `constants.py`: Zawiera stałe używane w GUI, takie jak rozmiary, kolory i inne wartości konfiguracyjne.
  - `gui_board.py`: Klasa `GUIBoard` zarządza wyświetlaniem planszy w interfejsie użytkownika.
  - `hexagon.py`: Klasa `Hexagon` odpowiada za reprezentację pojedynczego sześciokąta na planszy.
  - `menus.py`: Zawiera klasy do tworzenia i zarządzania menu w grze.
- `check_for_win.py`: Zawiera logikę sprawdzającą warunki wygranej w grze.
- `console_board.py`: Odpowiada za reprezentację planszy w trybie konsoli.
- `game.py`: Główny moduł gry, który inicjuje i zarządza stanem gry.
- `network.py`: Odpowiada za komunikację sieciową w grze, jeśli jest to gra wieloosobowa.

### Folder `images`
Zawiera wszystkie grafiki używane w grze, takie jak tekstury i ikony.

### Folder `test`
Zawiera testy jednostkowe sprawdzające poprawność działania poszczególnych komponentów gry.

### Plik `8-BIT WONDER.TTF`
Czcionka używana do wyświetlania tekstu w interfejsie użytkownika.

### Plik `main.py`
Punkt wejścia gry, który uruchamia interfejs użytkownika i inicjuje logikę gry.

### Plik `requirements.txt`
Lista zależności potrzebnych do uruchomienia gry, które można zainstalować za pomocą `pip`.

### Plik `constants.py`
Zawiera stałe, które można modyfikować w celu eksperymentowania z różnymi aspektami interfejsu użytkownika. Zmiana tych stałych może wpłynąć na wygląd i zachowanie elementów GUI, takich jak przyciski, kolory i wielkości elementów.

## GUI

### Klasa `Button`
Odpowiada za wyświetlanie i obsługę przycisków w GUI. Każdy przycisk może być skonfigurowany z różnymi akcjami po kliknięciu.

### Klasa `GUIBoard`
Zarządza graficzną reprezentacją planszy w grze, włącznie z umieszczaniem kamieni i wyświetlaniem możliwych ruchów.

### Klasa `Hexagon`
Reprezentuje pojedyncze pole na planszy hex. Odpowiada za wykrywanie kliknięcia i wyświetlanie stanu pola.

### Klasa `Menu`
Tworzy menu w grze, pozwalając na nawigację między różnymi ekranami, takimi jak menu główne, opcje czy ekran wyboru gry.



## Dokumentacja GUI

### `Button`
Interaktywny przycisk na ekranie gry.
- Inicjalizacja: ustawienie pozycji, rozmiaru, tekstu i zachowania po kliknięciu.
- Rysowanie: wyświetlanie przycisku.
- Kliknięcie: detekcja akcji użytkownika.
- Akcja: wykonanie powiązanej funkcji.

### `GuiBoard`
Graficzna reprezentacja planszy gry.
- Inicjalizacja: przygotowanie planszy.
- Rysowanie planszy: wyświetlanie komórek i stanu gry.
- Aktualizacja komórki: zmiana stanu po ruchu gracza.
- Aktualizacja planszy: odświeżanie stanu gry na podstawie danych.

### `Hexagon`
Sześciokątna komórka na planszy.
- Inicjalizacja: ustawienie centrum, rozmiaru i koloru.
- Rysowanie: wyświetlanie sześciokąta.
- Detekcja kliknięcia: sprawdzanie wyboru użytkownika.

### `Menu`
Menu gry z przyciskami.
- Inicjalizacja: ustawienie przycisków i okna.
- Wyświetlanie menu: obsługa i wyświetlanie menu gry.
- Tło menu: rysowanie tła menu.



## Dokumentacja logiki gry

### `WinnerChecker`
Sprawdza, czy w grze został osiągnięty stan wygranej.
- Konstruktor przyjmuje stan planszy i kolor gracza.
- Metoda `is_winner()` sprawdza, czy gracz połączył linie w swoim kolorze.

### `ConsoleBoard`
Reprezentacja planszy gry w konsoli.
- Metoda `display_board()` wyświetla aktualny stan planszy.

### `Game`
Główna klasa zarządzająca logiką gry.
- Metoda `handle_move()` obsługuje ruch gracza.
- Metoda `revert_move()` cofa ostatni ruch na planszy.

### `GameBot`
Rozszerzenie klasy `Game` o funkcjonalność bota.
- Metoda `make_random_move()` wykonuje losowy ruch.
- Metoda `revert_move()` cofa ruchy, uwzględniając ruchy bota.

### `NetworkEntity`
Zarządza sieciowymi aspektami gry.
- Metoda `setup_connection()` konfiguruje połączenie sieciowe.
- Metoda `attempt_connect()` próbuje nawiązać połączenie z serwerem.
- Metoda `handle_communication()` obsługuje komunikację sieciową.

### `Server`
Klasa serwera dla gry sieciowej.
- Metoda `start_server()` uruchamia serwer.
- Metoda `wait_for_connection()` czeka na połączenie klienta.

### `Client`
Klasa klienta dla gry sieciowej.
- Konstruktor może przyjąć adres hosta.
- Metoda `start_client()` rozpoczyna próbę połączenia z serwerem.




## Dokumentacja Modułu Głównego

W module głównym inicjowana jest gra i zarządzana jest logika rozpoczęcia, prowadzenia oraz zakończenia rozgrywki.

- Importy: moduły `pygame`, `sys` oraz potrzebne komponenty z pakietu `classes`.
- Inicjalizacja `pygame` oraz ustawienie wymiarów okna i podstawowych właściwości interfejsu użytkownika.
- Definicje funkcji pomocniczych, takich jak `quit_game()` do zamykania gry.
- Funkcja `main_menu()` definiuje i wyświetla główne menu gry.
- Funkcja `show_instruction()` prezentuje instrukcje gry.
- Funkcja `friend_game_menu()` pozwala na wybór trybu gry z przyjacielem.
- Funkcja `draw_pause()` rysuje ekran pauzy.
- Funkcja `select_color()` pozwala graczom wybrać kolor przed rozpoczęciem gry.
- Funkcja `start_game()` inicjuje i zarządza stanem gry oraz interfejsem graficznym.
- Funkcja `select_mod()` pozwala wybrać sposób połączenia dla gry sieciowej.
- Funkcja `input_host()` umożliwia wprowadzenie adresu IP dla połączenia sieciowego.
- Funkcja `play_on_2_devices()` zarządza uruchomieniem gry sieciowej jako serwer lub klient.

Wszystkie te funkcje współpracują ze sobą, aby umożliwić użytkownikowi płynną rozgrywkę, zarówno lokalnie jak i przez sieć. Dodatkowo, moduł obsługuje zdarzenia związane z interfejsem użytkownika, takie jak kliknięcia przycisków, i odpowiada za wyświetlanie odpowiednich ekranów menu i konfiguracji gry.




## Instalacja

Sklonuj repozytorium lub pobierz je, a następnie uruchom `main.py`:
```bash
git clone https://gitlab-stud.elka.pw.edu.pl/apryimak/game_hex.git
cd hex-game
python main.py
```



### Wymagania Systemowe

Gra Hex została zaprojektowana z myślą o kompatybilności zarówno z systemem Windows, jak i Linux. Jedyną zewnętrzną zależnością jest biblioteka `pygame`, która jest wykorzystywana do tworzenia interfejsu użytkownika i obsługi mechanik gry. Wszystkie inne niezbędne biblioteki, takie jak `socket` dla sieciowych funkcjonalności oraz `threading` dla wielowątkowości, są dostępne w standardowej dystrybucji Pythona i nie wymagają dodatkowej instalacji.
#### Instalacja Bibliotek

Aby zainstalować niezbędne zależności, możesz użyć menedżera pakietów `pip`. Dostępne są dwie metody instalacji:

1. Bezpośrednia instalacja `pygame`:
   ```bash
   pip install pygame
   ```
2. Instalacja zależności z pliku `requirements.txt`
  ```bash
  pip install -r requirements.txt
  ```

## Część refleksyjna

Projekt Gry Hex został zaprojektowany z myślą o elastyczności i różnorodności doświadczeń graczy. 

### Konfiguracje Planszy
- **Plansza dla Trzech Graczy**: Gra Hex jest dostosowana do rozgrywki więcej niż dwóch graczy, na przykład z użyciem specjalnie zaprojektowanej planszy heksagonalnej dla trzech osób.

### Tryby Gry
- **Zasada Zamiany (Swap Rule)**: Wprowadzenie możliwości zamiany kamieni po pierwszym ruchu, dodając głębię strategiczną.
- **Dodatkowe Opcje**: Implementacja nowych wariantów rozgrywki, które mogą oferować unikalne wyzwania i zasady dostosowane do zaawansowanych graczy.

### Możliwe Rozszerzenia
- **Personalizacja Planszy**: Dodanie opcji wyboru planszy o różnych wielkościach i kształtach, umożliwiające graczom eksperymentowanie z nowymi układami i strategiami.
- **Interaktywne Mechaniki Gry**: Rozbudowa interaktywności gry poprzez dodanie nowych elementów do kolekcjonowania oraz specjalnych mocy, które gracze mogą wykorzystać w kluczowych momentach rozgrywki.
- **Zaawansowane Algorytmy dla Botów**: Planuje się wprowadzenie bardziej skomplikowanych algorytmów dla botów, co zwiększy ich wydajność i będzie stanowiło większe wyzwanie dla graczy.
- **Rozbudowa Możliwości Serwera**: Prace nad serwerem obejmować będą rozbudowę o funkcje pozwalające na komunikację klient-klient i obsługę wielu sesji gry jednocześnie, co znacząco poszerzy możliwości rozgrywki sieciowej.

Każda z tych opcji powinna być projektowana z myślą o dostarczeniu graczom unikalnego doświadczenia przy każdej partii. Dzięki temu Gry Hex będzie nie tylko pojedynczą rozgrywką, ale platformą dla różnych wariantów gier strategicznych, które mogą być ciągle rozwijane i dostosowywane do potrzeb społeczności graczy.
