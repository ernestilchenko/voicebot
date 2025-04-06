document_types = {
            # DOKUMENTY TOŻSAMOŚCI I IDENTYFIKACYJNE
            "dowod": {
                "type": "Dowód osobisty",
                "fields": ["Nazwisko", "Imię", "PESEL", "Data urodzenia", "Płeć", "Adres zameldowania", "Data wydania",
                           "Data ważności"],
                "content": "Dokument tożsamości wydany przez organ państwowy, potwierdzający tożsamość obywatela.",
                "issuer": "Urząd miasta/gminy",
                "renewal_process": "Wymaga osobistej wizyty w urzędzie i zdjęcia biometrycznego. Czas odnowienia: 2-4 tygodnie."
            },
            "paszport": {
                "type": "Paszport",
                "fields": ["Nazwisko", "Imię", "PESEL", "Data urodzenia", "Płeć", "Miejsce urodzenia", "Data wydania",
                           "Data ważności"],
                "content": "Dokument podróży uprawniający do przekraczania granic państwowych.",
                "issuer": "Urząd wojewódzki",
                "renewal_process": "Wymaga złożenia wniosku w urzędzie wojewódzkim lub konsularnym. Czas odnowienia: 3-4 tygodnie."
            },
            "prawo": {
                "type": "Prawo jazdy",
                "fields": ["Nazwisko", "Imię", "Data urodzenia", "Miejsce urodzenia", "Data wydania", "Data ważności",
                           "Kategorie uprawnień"],
                "content": "Dokument uprawniający do prowadzenia pojazdów mechanicznych.",
                "issuer": "Starostwo powiatowe",
                "renewal_process": "Wymaga złożenia wniosku i aktualnego orzeczenia lekarskiego. Czas odnowienia: 1-2 tygodnie."
            },
            "tymczasowy_dowod": {
                "type": "Tymczasowy dowód osobisty",
                "fields": ["Nazwisko", "Imię", "PESEL", "Data urodzenia", "Data wydania", "Data ważności"],
                "content": "Tymczasowy dokument tożsamości wydawany w przypadku utraty dowodu lub oczekiwania na nowy.",
                "issuer": "Urząd miasta/gminy",
                "renewal_process": "Po upływie terminu ważności należy odebrać stały dowód osobisty. Nie podlega odnowieniu."
            },
            "karta_pobytu": {
                "type": "Karta pobytu",
                "fields": ["Nazwisko", "Imię", "Data urodzenia", "Obywatelstwo", "Adres zamieszkania", "Rodzaj pobytu",
                           "Data wydania", "Data ważności"],
                "content": "Dokument wydawany cudzoziemcom przebywającym legalnie na terytorium Polski.",
                "issuer": "Urząd wojewódzki",
                "renewal_process": "Wymaga złożenia wniosku na co najmniej 30 dni przed upływem ważności. Czas odnowienia: 1-3 miesiące."
            },
            "legitymacja_studencka": {
                "type": "Legitymacja studencka",
                "fields": ["Imię", "Nazwisko", "Numer albumu", "Nazwa uczelni", "Data wydania", "Data ważności"],
                "content": "Dokument potwierdzający status studenta, uprawniający do zniżek i świadczeń studenckich.",
                "issuer": "Uczelnia wyższa",
                "renewal_process": "Wymaga przedłużania ważności w każdym semestrze w dziekanacie. Czas odnowienia: 1-3 dni."
            },
            "legitymacja_szkolna": {
                "type": "Legitymacja szkolna",
                "fields": ["Imię", "Nazwisko", "Data urodzenia", "Nazwa szkoły", "Data wydania", "Data ważności"],
                "content": "Dokument potwierdzający status ucznia szkoły podstawowej lub średniej.",
                "issuer": "Szkoła",
                "renewal_process": "Aktualizowana co roku szkolny przez szkołę. Czas odnowienia: 1-7 dni."
            },
            "karta_mpk": {
                "type": "Karta miejska (MPK)",
                "fields": ["Imię", "Nazwisko", "PESEL", "Numer karty", "Data wydania", "Data ważności"],
                "content": "Elektroniczna karta służąca do korzystania z usług komunikacji miejskiej.",
                "issuer": "Miejskie Przedsiębiorstwo Komunikacyjne",
                "renewal_process": "Wymaga przedłużenia w punkcie obsługi klienta MPK. Czas odnowienia: 1 dzień."
            },
            "legitymacja_emeryta": {
                "type": "Legitymacja emeryta/rencisty",
                "fields": ["Imię", "Nazwisko", "PESEL", "Numer legitymacji", "Data wydania"],
                "content": "Dokument potwierdzający status emeryta lub rencisty, uprawniający do zniżek.",
                "issuer": "Zakład Ubezpieczeń Społecznych (ZUS)",
                "renewal_process": "Dokument bezterminowy, nie wymaga odnowienia."
            },
            "karta_ekuz": {
                "type": "Europejska Karta Ubezpieczenia Zdrowotnego (EKUZ)",
                "fields": ["Imię", "Nazwisko", "Data urodzenia", "Numer identyfikacyjny", "Data ważności"],
                "content": "Dokument uprawniający do korzystania z opieki zdrowotnej w krajach UE/EFTA.",
                "issuer": "Narodowy Fundusz Zdrowia (NFZ)",
                "renewal_process": "Wymaga złożenia wniosku w oddziale NFZ. Czas odnowienia: 1-7 dni."
            },

            # DOKUMENTY POJAZDOWE
            "dowod_rejestracyjny": {
                "type": "Dowód rejestracyjny pojazdu",
                "fields": ["Marka", "Model", "Nr rejestracyjny", "Nr VIN", "Właściciel", "Data pierwszej rejestracji",
                           "Data ważności badania technicznego"],
                "content": "Dokument potwierdzający dopuszczenie pojazdu do ruchu drogowego oraz jego parametry techniczne.",
                "issuer": "Starostwo powiatowe",
                "renewal_process": "Wymaga wymiany w przypadku braku miejsca na wpisy badań technicznych. Czas odnowienia: 1-2 tygodnie."
            },
            "karta_pojazdu": {
                "type": "Karta pojazdu",
                "fields": ["Marka", "Model", "Nr rejestracyjny", "Nr VIN", "Historia właścicieli", "Historia napraw"],
                "content": "Dokument zawierający historię pojazdu, jego właścicieli i przeprowadzonych napraw.",
                "issuer": "Starostwo powiatowe",
                "renewal_process": "Nie wymaga odnowienia, wydawana jednorazowo dla pojazdu."
            },
            "ubezpieczenie_oc": {
                "type": "Polisa ubezpieczenia OC pojazdu",
                "fields": ["Ubezpieczyciel", "Ubezpieczający", "Nr rejestracyjny", "Nr VIN", "Okres ubezpieczenia",
                           "Składka"],
                "content": "Dokument potwierdzający obowiązkowe ubezpieczenie odpowiedzialności cywilnej pojazdu.",
                "issuer": "Towarzystwo ubezpieczeniowe",
                "renewal_process": "Wymaga odnowienia przed upływem okresu ubezpieczenia. Czas odnowienia: 1 dzień."
            },
            "ubezpieczenie_ac": {
                "type": "Polisa ubezpieczenia AC pojazdu",
                "fields": ["Ubezpieczyciel", "Ubezpieczający", "Nr rejestracyjny", "Nr VIN", "Okres ubezpieczenia",
                           "Zakres ubezpieczenia", "Składka"],
                "content": "Dokument potwierdzający dobrowolne ubezpieczenie autocasco pojazdu.",
                "issuer": "Towarzystwo ubezpieczeniowe",
                "renewal_process": "Wymaga odnowienia przed upływem okresu ubezpieczenia. Czas odnowienia: 1-2 dni."
            },
            "karta_gwarancyjna_pojazdu": {
                "type": "Karta gwarancyjna pojazdu",
                "fields": ["Marka", "Model", "Nr VIN", "Data sprzedaży", "Okres gwarancji", "Warunki gwarancji"],
                "content": "Dokument określający warunki i okres gwarancji na pojazd.",
                "issuer": "Producent/dealer",
                "renewal_process": "Nie podlega odnowieniu. Po upływie okresu gwarancji możliwe przedłużenie odpłatne."
            },
            "pozwolenie_czasowe": {
                "type": "Pozwolenie czasowe na pojazd",
                "fields": ["Marka", "Model", "Nr rejestracyjny", "Nr VIN", "Właściciel", "Data wydania",
                           "Data ważności"],
                "content": "Tymczasowy dokument dopuszczający pojazd do ruchu, wydawany przed otrzymaniem stałego dowodu rejestracyjnego.",
                "issuer": "Starostwo powiatowe",
                "renewal_process": "Nie podlega odnowieniu. Po upływie terminu należy odebrać stały dowód rejestracyjny."
            },
            "naklejka_kontrolna": {
                "type": "Naklejka kontrolna na szybę pojazdu",
                "fields": ["Nr rejestracyjny", "Kod weryfikacyjny"],
                "content": "Naklejka umieszczana na przedniej szybie pojazdu, stanowiąca potwierdzenie legalności rejestracji.",
                "issuer": "Starostwo powiatowe",
                "renewal_process": "Wymaga wymiany przy zmianie dowodu rejestracyjnego. Czas wymiany: 1-7 dni."
            },

            # DOKUMENTY NIERUCHOMOŚCI
            "akt_wlasnosci": {
                "type": "Akt własności nieruchomości",
                "fields": ["Właściciel", "Adres nieruchomości", "Nr księgi wieczystej", "Powierzchnia", "Data nabycia"],
                "content": "Dokument potwierdzający prawo własności do nieruchomości.",
                "issuer": "Kancelaria notarialna",
                "renewal_process": "Dokument bezterminowy, nie wymaga odnowienia."
            },
            "ksiega_wieczysta": {
                "type": "Odpis z księgi wieczystej",
                "fields": ["Nr księgi wieczystej", "Właściciel", "Adres nieruchomości", "Obciążenia", "Służebności",
                           "Data wydania odpisu"],
                "content": "Dokument zawierający informacje o stanie prawnym nieruchomości i jej obciążeniach.",
                "issuer": "Sąd rejonowy (wydział ksiąg wieczystych)",
                "renewal_process": "Odpis aktualny na datę wydania. Przy zmianach należy pobrać nowy odpis. Czas uzyskania: 1-14 dni."
            },
            "wypis_z_rejestru_gruntow": {
                "type": "Wypis z rejestru gruntów",
                "fields": ["Nr działki", "Powierzchnia", "Klasa gruntu", "Właściciel", "Położenie", "Data wydania"],
                "content": "Dokument zawierający informacje o działce z ewidencji gruntów i budynków.",
                "issuer": "Starostwo powiatowe",
                "renewal_process": "Dokument aktualny na datę wydania. Przy zmianach należy pobrać nowy wypis. Czas uzyskania: 1-14 dni."
            },
            "pozwolenie_na_budowe": {
                "type": "Pozwolenie na budowę",
                "fields": ["Inwestor", "Adres inwestycji", "Nr działki", "Rodzaj inwestycji", "Data wydania",
                           "Data ważności"],
                "content": "Dokument uprawniający do rozpoczęcia i prowadzenia budowy lub wykonywania robót budowlanych.",
                "issuer": "Starostwo powiatowe lub urząd miasta",
                "renewal_process": "Ważne przez 3 lata od wydania. Wymaga przedłużenia przed upływem ważności. Czas odnowienia: 1-30 dni."
            },
            "projekt_budowlany": {
                "type": "Projekt budowlany",
                "fields": ["Inwestor", "Adres inwestycji", "Projektant", "Nr uprawnień projektanta", "Data opracowania",
                           "Zakres projektu"],
                "content": "Dokument zawierający szczegółowy plan budowy lub przebudowy obiektu budowlanego.",
                "issuer": "Uprawniony projektant",
                "renewal_process": "Nie wymaga odnowienia. Aktualizowany w przypadku zmian w projekcie."
            },
            "umowa_najmu": {
                "type": "Umowa najmu nieruchomości",
                "fields": ["Wynajmujący", "Najemca", "Adres nieruchomości", "Okres najmu", "Czynsz", "Data zawarcia"],
                "content": "Dokument określający warunki najmu nieruchomości przez najemcę od wynajmującego.",
                "issuer": "Strony umowy (wynajmujący i najemca)",
                "renewal_process": "Wymaga przedłużenia przed upływem okresu najmu poprzez aneks lub nową umowę. Czas odnowienia: 1-7 dni."
            },
            "swiadectwo_energetyczne": {
                "type": "Świadectwo charakterystyki energetycznej",
                "fields": ["Adres nieruchomości", "Wskaźnik EP", "Wskaźnik EK", "Osoba sporządzająca", "Nr uprawnień",
                           "Data wydania", "Data ważności"],
                "content": "Dokument określający energochłonność budynku lub lokalu.",
                "issuer": "Uprawniony audytor energetyczny",
                "renewal_process": "Ważne przez 10 lat od wydania. Wymaga odnowienia po upływie ważności. Czas odnowienia: 1-14 dni."
            },
            "akt_notarialny": {
                "type": "Akt notarialny",
                "fields": ["Strony umowy", "Przedmiot umowy", "Cena", "Data sporządzenia", "Numer repertorium"],
                "content": "Dokument sporządzony przez notariusza, potwierdzający określoną czynność prawną.",
                "issuer": "Kancelaria notarialna",
                "renewal_process": "Dokument bezterminowy, nie wymaga odnowienia."
            },

            # DOKUMENTY FINANSOWE I UBEZPIECZENIOWE
            "ubezpieczenie": {
                "type": "Polisa ubezpieczeniowa",
                "fields": ["Ubezpieczający", "Ubezpieczony", "Przedmiot ubezpieczenia", "Suma ubezpieczenia", "Składka",
                           "Data rozpoczęcia", "Data zakończenia"],
                "content": "Umowa ubezpieczenia zawarta pomiędzy ubezpieczającym a ubezpieczycielem.",
                "issuer": "Towarzystwo ubezpieczeniowe",
                "renewal_process": "Wymaga kontaktu z agentem ubezpieczeniowym. Czas odnowienia: 1-3 dni."
            },
            "umowa_kredytowa": {
                "type": "Umowa kredytowa",
                "fields": ["Kredytobiorca", "Kredytodawca", "Kwota kredytu", "Okres kredytowania", "Oprocentowanie",
                           "Rata", "Data zawarcia"],
                "content": "Dokument określający warunki udzielenia kredytu przez bank kredytobiorcy.",
                "issuer": "Bank",
                "renewal_process": "Nie wymaga odnowienia. Wygasa po spłacie kredytu."
            },
            "umowa_pozyczki": {
                "type": "Umowa pożyczki",
                "fields": ["Pożyczkodawca", "Pożyczkobiorca", "Kwota pożyczki", "Okres spłaty", "Oprocentowanie",
                           "Data zawarcia"],
                "content": "Dokument określający warunki udzielenia pożyczki pożyczkobiorcy przez pożyczkodawcę.",
                "issuer": "Instytucja finansowa lub osoby prywatne",
                "renewal_process": "Nie wymaga odnowienia. Wygasa po spłacie pożyczki."
            },
            "polisa_na_zycie": {
                "type": "Polisa ubezpieczenia na życie",
                "fields": ["Ubezpieczający", "Ubezpieczony", "Uposażeni", "Suma ubezpieczenia", "Składka",
                           "Data rozpoczęcia", "Data zakończenia"],
                "content": "Dokument potwierdzający zawarcie umowy ubezpieczenia na życie.",
                "issuer": "Towarzystwo ubezpieczeniowe",
                "renewal_process": "Wymaga odnowienia przed upływem okresu ubezpieczenia. Czas odnowienia: 1-7 dni."
            },
            "polisa_zdrowotna": {
                "type": "Polisa ubezpieczenia zdrowotnego",
                "fields": ["Ubezpieczający", "Ubezpieczony", "Zakres ubezpieczenia", "Składka", "Data rozpoczęcia",
                           "Data zakończenia"],
                "content": "Dokument potwierdzający zawarcie umowy prywatnego ubezpieczenia zdrowotnego.",
                "issuer": "Towarzystwo ubezpieczeniowe",
                "renewal_process": "Wymaga odnowienia przed upływem okresu ubezpieczenia. Czas odnowienia: 1-7 dni."
            },
            "polisa_mieszkaniowa": {
                "type": "Polisa ubezpieczenia mieszkania",
                "fields": ["Ubezpieczający", "Adres ubezpieczanej nieruchomości", "Zakres ubezpieczenia",
                           "Suma ubezpieczenia", "Składka", "Data rozpoczęcia", "Data zakończenia"],
                "content": "Dokument potwierdzający zawarcie umowy ubezpieczenia mieszkania lub domu.",
                "issuer": "Towarzystwo ubezpieczeniowe",
                "renewal_process": "Wymaga odnowienia przed upływem okresu ubezpieczenia. Czas odnowienia: 1-3 dni."
            },
            "umowa_hipoteczna": {
                "type": "Umowa kredytu hipotecznego",
                "fields": ["Kredytobiorca", "Kredytodawca", "Kwota kredytu", "Okres kredytowania", "Oprocentowanie",
                           "Adres nieruchomości", "Data zawarcia"],
                "content": "Dokument określający warunki udzielenia kredytu zabezpieczonego hipoteką na nieruchomości.",
                "issuer": "Bank",
                "renewal_process": "Nie wymaga odnowienia. Wygasa po spłacie kredytu."
            },
            "faktura": {
                "type": "Faktura",
                "fields": ["Sprzedawca", "Nabywca", "NIP", "Przedmiot sprzedaży", "Kwota", "Data wystawienia",
                           "Termin płatności"],
                "content": "Dokument potwierdzający sprzedaż towaru lub usługi.",
                "issuer": "Sprzedawca (przedsiębiorca)",
                "renewal_process": "Nie wymaga odnowienia. Dokument jednorazowy."
            },
            "wycena_nieruchomosci": {
                "type": "Operat szacunkowy (wycena nieruchomości)",
                "fields": ["Adres nieruchomości", "Wartość nieruchomości", "Rzeczoznawca", "Nr uprawnień",
                           "Data sporządzenia", "Data ważności"],
                "content": "Dokument określający wartość rynkową nieruchomości, sporządzony przez rzeczoznawcę majątkowego.",
                "issuer": "Rzeczoznawca majątkowy",
                "renewal_process": "Ważny przez 12 miesięcy od daty sporządzenia. Po tym czasie wymaga aktualizacji. Czas odnowienia: 1-14 dni."
            },

            # DOKUMENTY PODRÓŻY
            "wiza": {
                "type": "Wiza",
                "fields": ["Nazwisko", "Imię", "Data urodzenia", "Typ wizy", "Państwo wydania", "Data wydania",
                           "Data ważności", "Liczba dozwolonych wjazdów"],
                "content": "Dokument lub adnotacja w dokumencie podróży, zezwalająca na przekroczenie granicy i pobyt w danym kraju.",
                "issuer": "Ambasada lub konsulat danego państwa",
                "renewal_process": "Wymaga złożenia nowego wniosku wizowego. Czas odnowienia: 5-30 dni, zależnie od państwa."
            },
            "bilet_lotniczy": {
                "type": "Bilet lotniczy",
                "fields": ["Pasażer", "Numer lotu", "Linia lotnicza", "Lotnisko wylotu", "Lotnisko przylotu",
                           "Data i godzina wylotu", "Numer rezerwacji"],
                "content": "Dokument uprawniający do podróży samolotem na określonej trasie.",
                "issuer": "Linia lotnicza lub agent sprzedaży",
                "renewal_process": "Nie podlega odnowieniu. W przypadku zmian należy dokonać nowej rezerwacji."
            },
            "bilet_kolejowy": {
                "type": "Bilet kolejowy",
                "fields": ["Pasażer", "Relacja", "Data podróży", "Godzina odjazdu", "Numer pociągu",
                           "Numer wagonu i miejsca"],
                "content": "Dokument uprawniający do podróży pociągiem na określonej trasie.",
                "issuer": "Przewoźnik kolejowy",
                "renewal_process": "Nie podlega odnowieniu. W przypadku zmian należy zakupić nowy bilet."
            },
            "voucher_hotelowy": {
                "type": "Voucher hotelowy",
                "fields": ["Gość", "Nazwa hotelu", "Adres hotelu", "Data zameldowania", "Data wymeldowania",
                           "Rodzaj pokoju", "Numer rezerwacji"],
                "content": "Dokument potwierdzający rezerwację i opłacenie pobytu w hotelu.",
                "issuer": "Hotel lub biuro podróży",
                "renewal_process": "Nie podlega odnowieniu. W przypadku zmian należy kontaktować się z hotelem."
            },
            "karta_pokładowa": {
                "type": "Karta pokładowa",
                "fields": ["Pasażer", "Numer lotu", "Linia lotnicza", "Lotnisko wylotu", "Lotnisko przylotu",
                           "Data i godzina wylotu", "Numer miejsca"],
                "content": "Dokument uprawniający do wejścia na pokład samolotu.",
                "issuer": "Linia lotnicza",
                "renewal_process": "Nie podlega odnowieniu. Wydawana jednorazowo na konkretny lot."
            },
            "ubezpieczenie_podrozne": {
                "type": "Polisa ubezpieczenia podróżnego",
                "fields": ["Ubezpieczony", "Zakres terytorialny", "Zakres ubezpieczenia", "Suma ubezpieczenia",
                           "Data rozpoczęcia", "Data zakończenia"],
                "content": "Dokument potwierdzający zawarcie umowy ubezpieczenia na czas podróży.",
                "issuer": "Towarzystwo ubezpieczeniowe",
                "renewal_process": "Nie podlega odnowieniu. Wymaga zakupu nowej polisy na kolejną podróż."
            },
            "miedzynarodowe_prawo_jazdy": {
                "type": "Międzynarodowe prawo jazdy",
                "fields": ["Nazwisko", "Imię", "Data urodzenia", "Miejsce urodzenia", "Kategorie uprawnień",
                           "Data wydania", "Data ważności"],
                "content": "Dokument uprawniający do prowadzenia pojazdów poza granicami kraju, uznawany międzynarodowo.",
                "issuer": "Starostwo powiatowe",
                "renewal_process": "Ważne przez 3 lata od daty wydania. Wymaga ponownego złożenia wniosku. Czas odnowienia: 1-14 dni."
            },
            "karta_turysty": {
                "type": "Karta turysty",
                "fields": ["Nazwisko", "Imię", "Data ważności", "Zakres uprawnień", "Miejscowość/region"],
                "content": "Dokument uprawniający do zniżek i wstępu do atrakcji turystycznych w danym regionie.",
                "issuer": "Lokalna organizacja turystyczna",
                "renewal_process": "Nie podlega odnowieniu. Należy zakupić nową kartę na kolejny pobyt."
            },

            # DOKUMENTY MEDYCZNE
            "karta_szczepien": {
                "type": "Międzynarodowa książeczka szczepień",
                "fields": ["Nazwisko", "Imię", "Data urodzenia", "Historia szczepień", "Daty wykonania",
                           "Daty ważności"],
                "content": "Dokument potwierdzający wykonane szczepienia, wymagany przy podróżach do niektórych krajów.",
                "issuer": "Placówka medyczna wykonująca szczepienia",
                "renewal_process": "Dokument jest uzupełniany o nowe szczepienia. Nie wymaga odnowienia."
            },
            "recepta_lekarska": {
                "type": "Recepta lekarska",
                "fields": ["Dane pacjenta", "Dane lekarza", "Nazwa leku", "Dawkowanie", "Data wystawienia",
                           "Kod recepty"],
                "content": "Dokument upoważniający do zakupu określonych leków w aptece.",
                "issuer": "Lekarz",
                "renewal_process": "Ważna przez określony czas (zwykle 30 dni). Wymaga ponownej wizyty u lekarza. Czas odnowienia: 1 dzień."
            },
            "karta_zdrowia": {
                "type": "Karta zdrowia pacjenta",
                "fields": ["Dane pacjenta", "Historia chorób", "Alergie", "Przyjmowane leki",
                           "Historia hospitalizacji"],
                "content": "Dokument zawierający historię medyczną pacjenta.",
                "issuer": "Placówka medyczna",
                "renewal_process": "Nie wymaga odnowienia. Jest uzupełniana przez lekarzy podczas wizyt."
            },
            "orzeczenie_lekarskie": {
                "type": "Orzeczenie lekarskie",
                "fields": ["Dane pacjenta", "Diagnoza", "Zalecenia", "Dane lekarza", "Data wydania", "Data ważności"],
                "content": "Dokument zawierający diagnozę i zalecenia lekarskie, często wymagany do określonych aktywności.",
                "issuer": "Lekarz specjalista lub komisja lekarska",
                "renewal_process": "Ważne przez określony czas. Wymaga ponownego badania. Czas odnowienia: 1-14 dni."
            },
            "karta_ciazy": {
                "type": "Karta przebiegu ciąży",
                "fields": ["Dane pacjentki", "Termin porodu", "Historia badań", "Wyniki USG", "Zalecenia lekarskie"],
                "content": "Dokument zawierający informacje o przebiegu ciąży, wynikach badań i zaleceniach dla ciężarnej.",
                "issuer": "Lekarz ginekolog",
                "renewal_process": "Nie wymaga odnowienia. Jest uzupełniana podczas wizyt kontrolnych w czasie ciąży."
            },
            "skierowanie": {
                "type": "Skierowanie na badania lub do specjalisty",
                "fields": ["Dane pacjenta", "Rodzaj badania/specjalizacja", "Rozpoznanie", "Dane lekarza kierującego",
                           "Data wystawienia"],
                "content": "Dokument kierujący pacjenta na określone badania lub do lekarza specjalisty.",
                "issuer": "Lekarz",
                "renewal_process": "Ważne przez określony czas (zwykle 3 lub 12 miesięcy). Wymaga ponownej wizyty u lekarza. Czas odnowienia: 1 dzień."
            },
            "zaswiadczenie_lekarskie": {
                "type": "Zaświadczenie lekarskie",
                "fields": ["Dane pacjenta", "Treść zaświadczenia", "Dane lekarza", "Data wystawienia", "Cel wydania"],
                "content": "Dokument potwierdzający określony stan zdrowia lub fakt medyczny.",
                "issuer": "Lekarz",
                "renewal_process": "Ważne przez okres wskazany w zaświadczeniu. Wymaga ponownej wizyty u lekarza. Czas odnowienia: 1 dzień."
            },
            "zwolnienie_lekarskie": {
                "type": "Zwolnienie lekarskie (L4)",
                "fields": ["Dane pacjenta", "Okres niezdolności do pracy", "Kod choroby", "Dane lekarza",
                           "Data wystawienia"],
                "content": "Dokument potwierdzający czasową niezdolność do pracy z powodu choroby.",
                "issuer": "Lekarz",
                "renewal_process": "Nie podlega odnowieniu. W przypadku przedłużającej się choroby wystawiane jest nowe zwolnienie."
            },

            # DOKUMENTY EDUKACYJNE
            "dyplom_ukonczenia_studiow": {
                "type": "Dyplom ukończenia studiów",
                "fields": ["Imię i nazwisko", "Data urodzenia", "Kierunek studiów", "Uzyskany tytuł", "Ocena końcowa",
                           "Data wydania", "Numer dyplomu"],
                "content": "Dokument potwierdzający ukończenie studiów wyższych i uzyskanie tytułu zawodowego.",
                "issuer": "Uczelnia wyższa",
                "renewal_process": "Dokument bezterminowy, nie wymaga odnowienia. W przypadku zgubienia można uzyskać duplikat."
            },
            "swiadectwo_maturalne": {
                "type": "Świadectwo dojrzałości (matura)",
                "fields": ["Imię i nazwisko", "Data urodzenia", "Oceny z przedmiotów", "Wyniki egzaminów",
                           "Data wydania", "Numer świadectwa"],
                "content": "Dokument potwierdzający zdanie egzaminu maturalnego.",
                "issuer": "Okręgowa Komisja Egzaminacyjna",
                "renewal_process": "Dokument bezterminowy, nie wymaga odnowienia. W przypadku zgubienia można uzyskać duplikat."
            },
            "swiadectwo_szkolne": {
                "type": "Świadectwo szkolne",
                "fields": ["Imię i nazwisko", "Data urodzenia", "Klasa/Rok szkolny", "Oceny z przedmiotów",
                           "Data wydania", "Numer świadectwa"],
                "content": "Dokument potwierdzający ukończenie określonego etapu edukacji lub roku szkolnego.",
                "issuer": "Szkoła",
                "renewal_process": "Dokument bezterminowy, nie wymaga odnowienia. W przypadku zgubienia można uzyskać duplikat."
            },
            "legitymacja_doktorancka": {
                "type": "Legitymacja doktorancka",
                "fields": ["Imię i nazwisko", "Numer albumu", "Nazwa uczelni", "Dziedzina nauki", "Data wydania",
                           "Data ważności"],
                "content": "Dokument potwierdzający status doktoranta, uprawniający do zniżek.",
                "issuer": "Uczelnia wyższa",
                "renewal_process": "Wymaga przedłużania ważności w każdym roku akademickim. Czas odnowienia: 1-7 dni."
            },
            "certyfikat_jezykowy": {
                "type": "Certyfikat językowy",
                "fields": ["Imię i nazwisko", "Język", "Poziom znajomości", "Wynik egzaminu", "Data wydania",
                           "Data ważności"],
                "content": "Dokument potwierdzający znajomość języka obcego na określonym poziomie.",
                "issuer": "Instytucja certyfikująca",
                "renewal_process": "Niektóre certyfikaty są bezterminowe, inne wymagają ponownego podejścia do egzaminu po okresie ważności (zwykle 2-3 lata)."
            },
            "certyfikat": {
                "type": "Certyfikat",
                "fields": ["Nazwa certyfikatu", "Posiadacz", "Zakres uprawnień", "Data wydania", "Data ważności"],
                "content": "Dokument potwierdzający określone kwalifikacje lub uprawnienia.",
                "issuer": "Instytucja certyfikująca",
                "renewal_process": "Może wymagać ponownego szkolenia i egzaminu. Czas odnowienia: zależny od rodzaju certyfikatu."
            },
            "zaswiadczenie_o_ukonczeniu_kursu": {
                "type": "Zaświadczenie o ukończeniu kursu",
                "fields": ["Imię i nazwisko", "Nazwa kursu", "Liczba godzin", "Uzyskane umiejętności", "Data wydania"],
                "content": "Dokument potwierdzający ukończenie kursu lub szkolenia.",
                "issuer": "Organizator kursu",
                "renewal_process": "Dokument bezterminowy, nie wymaga odnowienia."
            },
            "indeks": {
                "type": "Indeks studenta",
                "fields": ["Imię i nazwisko", "Numer albumu", "Nazwa uczelni", "Kierunek studiów", "Przedmioty",
                           "Oceny"],
                "content": "Dokument zawierający przebieg studiów i uzyskane oceny.",
                "issuer": "Uczelnia wyższa",
                "renewal_process": "Nie wymaga odnowienia. Uzupełniany w trakcie studiów."
            },

            # DOKUMENTY BIZNESOWE
            "umowa": {
                "type": "Umowa",
                "fields": ["Strony umowy", "Przedmiot umowy", "Wartość umowy", "Data zawarcia", "Data zakończenia"],
                "content": "Dokument zawierający porozumienie stron dotyczące określonych praw i obowiązków.",
                "issuer": "Strony umowy",
                "renewal_process": "Wymaga renegocjacji warunków i podpisania aneksu lub nowej umowy. Czas odnowienia: zależny od stron."
            },
            "umowa_o_prace": {
                "type": "Umowa o pracę",
                "fields": ["Pracodawca", "Pracownik", "Stanowisko", "Wynagrodzenie", "Wymiar etatu", "Data rozpoczęcia",
                           "Okres umowy"],
                "content": "Dokument określający warunki zatrudnienia pracownika przez pracodawcę.",
                "issuer": "Pracodawca",
                "renewal_process": "W przypadku umowy na czas określony wymaga przedłużenia przed upływem terminu. Czas odnowienia: 1-7 dni."
            },
            "umowa_zlecenie": {
                "type": "Umowa zlecenie",
                "fields": ["Zleceniodawca", "Zleceniobiorca", "Przedmiot zlecenia", "Wynagrodzenie", "Data zawarcia",
                           "Termin wykonania"],
                "content": "Dokument określający warunki wykonania określonej czynności przez zleceniobiorcę dla zleceniodawcy.",
                "issuer": "Zleceniodawca",
                "renewal_process": "Wygasa po wykonaniu zlecenia. Wymaga zawarcia nowej umowy dla kolejnych zleceń."
            },
            "umowa_o_dzielo": {
                "type": "Umowa o dzieło",
                "fields": ["Zamawiający", "Wykonawca", "Przedmiot umowy", "Wynagrodzenie", "Data zawarcia",
                           "Termin wykonania"],
                "content": "Dokument określający warunki wykonania określonego dzieła przez wykonawcę dla zamawiającego.",
                "issuer": "Zamawiający",
                "renewal_process": "Wygasa po wykonaniu dzieła. Wymaga zawarcia nowej umowy dla kolejnych dzieł."
            },
            "umowa_najmu": {
                "type": "Umowa najmu lokalu",
                "fields": ["Wynajmujący", "Najemca", "Adres lokalu", "Czynsz", "Okres najmu", "Data zawarcia"],
                "content": "Dokument określający warunki najmu lokalu przez najemcę od wynajmującego.",
                "issuer": "Strony umowy (wynajmujący i najemca)",
                "renewal_process": "Wymaga przedłużenia przed upływem okresu najmu poprzez aneks lub nową umowę. Czas odnowienia: 1-7 dni."
            },
            "koncesja": {
                "type": "Koncesja",
                "fields": ["Nazwa podmiotu", "Numer koncesji", "Zakres działalności", "Data wydania", "Data ważności",
                           "Organ wydający"],
                "content": "Dokument upoważniający do prowadzenia określonej działalności gospodarczej wymagającej koncesji.",
                "issuer": "Organ administracji publicznej (np. minister)",
                "renewal_process": "Wymaga złożenia wniosku o przedłużenie przed upływem ważności. Czas odnowienia: 30-90 dni."
            },
            "zezwolenie": {
                "type": "Zezwolenie na prowadzenie działalności",
                "fields": ["Nazwa podmiotu", "Numer zezwolenia", "Rodzaj działalności", "Adres działalności",
                           "Data wydania", "Data ważności"],
                "content": "Dokument uprawniający do prowadzenia określonego rodzaju działalności gospodarczej.",
                "issuer": "Organ administracji publicznej (np. prezydent miasta, starosta)",
                "renewal_process": "Wymaga złożenia wniosku o przedłużenie przed upływem ważności. Czas odnowienia: 14-60 dni."
            },
            "wpis_do_rejestru": {
                "type": "Zaświadczenie o wpisie do rejestru działalności gospodarczej",
                "fields": ["Nazwa podmiotu", "NIP", "REGON", "Adres siedziby", "Przedmiot działalności", "Data wpisu"],
                "content": "Dokument potwierdzający wpis do rejestru działalności gospodarczej.",
                "issuer": "Urząd miasta/gminy lub KRS",
                "renewal_process": "Nie wymaga odnowienia. W przypadku zmian należy dokonać aktualizacji wpisu."
            },
            "odpis_krs": {
                "type": "Odpis z Krajowego Rejestru Sądowego",
                "fields": ["Nazwa podmiotu", "Numer KRS", "NIP", "REGON", "Adres siedziby", "Reprezentacja",
                           "Data wydania odpisu"],
                "content": "Dokument zawierający informacje o podmiocie wpisanym do Krajowego Rejestru Sądowego.",
                "issuer": "Sąd rejonowy (wydział gospodarczy KRS)",
                "renewal_process": "Odpis aktualny na datę wydania. Przy zmianach należy pobrać nowy odpis. Czas uzyskania: 1-7 dni."
            },

            # DOKUMENTY PRAWNE
            "pełnomocnictwo": {
                "type": "Pełnomocnictwo",
                "fields": ["Mocodawca", "Pełnomocnik", "Zakres umocowania", "Data udzielenia", "Data ważności"],
                "content": "Dokument upoważniający pełnomocnika do działania w imieniu mocodawcy.",
                "issuer": "Mocodawca",
                "renewal_process": "Wygasa po upływie terminu ważności lub odwołaniu. Wymaga wystawienia nowego dokumentu."
            },
            "testament": {
                "type": "Testament",
                "fields": ["Testator", "Spadkobiercy", "Rozporządzenia", "Data sporządzenia", "Podpis testatora",
                           "Podpisy świadków"],
                "content": "Dokument zawierający ostatnią wolę osoby dotyczącą rozporządzenia jej majątkiem po śmierci.",
                "issuer": "Testator (osoba sporządzająca testament) lub notariusz",
                "renewal_process": "Nie wymaga odnowienia. Może być zmieniony lub odwołany przez testatora za życia."
            },
            "pozew": {
                "type": "Pozew sądowy",
                "fields": ["Powód", "Pozwany", "Przedmiot sporu", "Wartość przedmiotu sporu", "Żądania",
                           "Data złożenia"],
                "content": "Dokument wszczynający postępowanie sądowe, zawierający roszczenia powoda wobec pozwanego.",
                "issuer": "Powód lub jego pełnomocnik",
                "renewal_process": "Nie wymaga odnowienia. Dokument procesowy jednorazowy."
            },
            "wyrok_sadowy": {
                "type": "Wyrok sądowy",
                "fields": ["Sąd", "Sygnatura akt", "Strony postępowania", "Rozstrzygnięcie", "Uzasadnienie",
                           "Data wydania"],
                "content": "Dokument zawierający rozstrzygnięcie sądu w sprawie cywilnej lub karnej.",
                "issuer": "Sąd",
                "renewal_process": "Nie wymaga odnowienia. Dokument bezterminowy."
            },
            "decyzja_administracyjna": {
                "type": "Decyzja administracyjna",
                "fields": ["Organ wydający", "Strona", "Podstawa prawna", "Rozstrzygnięcie", "Data wydania",
                           "Pouczenie"],
                "content": "Dokument wydany przez organ administracji publicznej, rozstrzygający sprawę administracyjną.",
                "issuer": "Organ administracji publicznej",
                "renewal_process": "Nie wymaga odnowienia. W przypadku decyzji terminowych może wymagać złożenia nowego wniosku."
            },
            "oświadczenie": {
                "type": "Oświadczenie",
                "fields": ["Osoba składająca", "Treść oświadczenia", "Data złożenia", "Podpis"],
                "content": "Dokument zawierający jednostronne oświadczenie woli lub wiedzy osoby.",
                "issuer": "Osoba składająca oświadczenie",
                "renewal_process": "Nie wymaga odnowienia. Dokument jednorazowy."
            },
            "ugoda": {
                "type": "Ugoda",
                "fields": ["Strony ugody", "Przedmiot ugody", "Warunki porozumienia", "Data zawarcia"],
                "content": "Dokument zawierający porozumienie stron w sprawie spornej.",
                "issuer": "Strony ugody lub mediator",
                "renewal_process": "Nie wymaga odnowienia. Dokument bezterminowy."
            },
            "umowa_przedwstepna": {
                "type": "Umowa przedwstępna",
                "fields": ["Strony umowy", "Przedmiot umowy docelowej", "Termin zawarcia umowy docelowej",
                           "Zadatek/zaliczka", "Data zawarcia"],
                "content": "Dokument zobowiązujący strony do zawarcia w przyszłości umowy docelowej o określonej treści.",
                "issuer": "Strony umowy",
                "renewal_process": "Wygasa po zawarciu umowy docelowej lub upływie terminu. Wymaga zawarcia nowej umowy."
            },

            # DOKUMENTY URZĘDOWE
            "zaswiadczenie_o_niekaralnosci": {
                "type": "Zaświadczenie o niekaralności",
                "fields": ["Imię i nazwisko", "PESEL", "Data urodzenia", "Informacja o karalności", "Data wydania",
                           "Numer zaświadczenia"],
                "content": "Dokument potwierdzający brak wpisu w Krajowym Rejestrze Karnym.",
                "issuer": "Krajowy Rejestr Karny",
                "renewal_process": "Ważne przez określony czas (zwykle 3-6 miesięcy). Wymaga złożenia nowego wniosku. Czas odnowienia: 1-14 dni."
            },
            "zaswiadczenie_o_zameldowaniu": {
                "type": "Zaświadczenie o zameldowaniu",
                "fields": ["Imię i nazwisko", "PESEL", "Adres zameldowania", "Rodzaj zameldowania", "Data wydania"],
                "content": "Dokument potwierdzający zameldowanie osoby pod wskazanym adresem.",
                "issuer": "Urząd miasta/gminy",
                "renewal_process": "Ważne przez określony czas (zwykle 2-3 miesiące). Wymaga złożenia nowego wniosku. Czas odnowienia: 1-7 dni."
            },
            "zaswiadczenie_o_dochodach": {
                "type": "Zaświadczenie o dochodach",
                "fields": ["Imię i nazwisko", "PESEL", "Pracodawca", "Wysokość dochodu", "Okres dochodu",
                           "Data wydania"],
                "content": "Dokument potwierdzający wysokość dochodów osoby w określonym okresie.",
                "issuer": "Pracodawca, ZUS lub urząd skarbowy",
                "renewal_process": "Ważne przez określony czas (zwykle 1-3 miesiące). Wymaga złożenia nowego wniosku. Czas odnowienia: 1-7 dni."
            },
            "zaswiadczenie_o_niezaleganiu": {
                "type": "Zaświadczenie o niezaleganiu w podatkach",
                "fields": ["Nazwa podmiotu", "NIP", "Informacja o zaległościach", "Data wydania",
                           "Numer zaświadczenia"],
                "content": "Dokument potwierdzający brak zaległości podatkowych.",
                "issuer": "Urząd skarbowy",
                "renewal_process": "Ważne przez określony czas (zwykle 1-3 miesiące). Wymaga złożenia nowego wniosku. Czas odnowienia: 7-14 dni."
            },
            "zaswiadczenie_zus": {
                "type": "Zaświadczenie ZUS o niezaleganiu ze składkami",
                "fields": ["Nazwa podmiotu", "NIP", "REGON", "Informacja o zaległościach", "Data wydania",
                           "Numer zaświadczenia"],
                "content": "Dokument potwierdzający brak zaległości w opłacaniu składek na ubezpieczenia społeczne.",
                "issuer": "Zakład Ubezpieczeń Społecznych (ZUS)",
                "renewal_process": "Ważne przez określony czas (zwykle 30 dni). Wymaga złożenia nowego wniosku. Czas odnowienia: 7-14 dni."
            },
            "odpis_aktu_urodzenia": {
                "type": "Odpis aktu urodzenia",
                "fields": ["Imię i nazwisko", "Data urodzenia", "Miejsce urodzenia", "Rodzice", "Data wydania odpisu",
                           "Numer aktu"],
                "content": "Dokument potwierdzający fakt urodzenia osoby.",
                "issuer": "Urząd stanu cywilnego",
                "renewal_process": "Dokument bezterminowy. W przypadku potrzeby można uzyskać nowy odpis. Czas uzyskania: 1-7 dni."
            },
            "odpis_aktu_malzenstwa": {
                "type": "Odpis aktu małżeństwa",
                "fields": ["Imiona i nazwiska małżonków", "Data zawarcia małżeństwa", "Miejsce zawarcia małżeństwa",
                           "Data wydania odpisu", "Numer aktu"],
                "content": "Dokument potwierdzający fakt zawarcia małżeństwa.",
                "issuer": "Urząd stanu cywilnego",
                "renewal_process": "Dokument bezterminowy. W przypadku potrzeby można uzyskać nowy odpis. Czas uzyskania: 1-7 dni."
            },
            "odpis_aktu_zgonu": {
                "type": "Odpis aktu zgonu",
                "fields": ["Imię i nazwisko", "Data zgonu", "Miejsce zgonu", "Data wydania odpisu", "Numer aktu"],
                "content": "Dokument potwierdzający fakt zgonu osoby.",
                "issuer": "Urząd stanu cywilnego",
                "renewal_process": "Dokument bezterminowy. W przypadku potrzeby można uzyskać nowy odpis. Czas uzyskania: 1-7 dni."
            },

            # DOKUMENTY TECHNICZNE
            "instrukcja_obslugi": {
                "type": "Instrukcja obsługi",
                "fields": ["Nazwa produktu", "Model", "Producent", "Spis treści", "Specyfikacja techniczna",
                           "Data wydania"],
                "content": "Dokument zawierający wskazówki dotyczące obsługi, konserwacji i bezpieczeństwa produktu.",
                "issuer": "Producent",
                "renewal_process": "Nie wymaga odnowienia. Aktualizowana przy zmianach w produkcie."
            },
            "karta_gwarancyjna": {
                "type": "Karta gwarancyjna",
                "fields": ["Nazwa produktu", "Model", "Numer seryjny", "Data zakupu", "Okres gwarancji",
                           "Warunki gwarancji"],
                "content": "Dokument określający warunki i okres gwarancji na produkt.",
                "issuer": "Producent lub sprzedawca",
                "renewal_process": "Nie podlega odnowieniu. Po upływie okresu gwarancji możliwe przedłużenie odpłatne."
            },
            "certyfikat_zgodnosci": {
                "type": "Certyfikat zgodności",
                "fields": ["Nazwa produktu", "Model", "Producent", "Normy zgodności", "Jednostka certyfikująca",
                           "Data wydania", "Numer certyfikatu"],
                "content": "Dokument potwierdzający zgodność produktu z określonymi normami i przepisami.",
                "issuer": "Jednostka certyfikująca",
                "renewal_process": "Ważny przez określony czas lub do zmiany specyfikacji produktu. Wymaga ponownej certyfikacji."
            },
            "deklaracja_zgodnosci": {
                "type": "Deklaracja zgodności",
                "fields": ["Nazwa produktu", "Model", "Producent", "Normy zgodności", "Data wydania"],
                "content": "Dokument, w którym producent deklaruje zgodność produktu z określonymi normami i przepisami.",
                "issuer": "Producent",
                "renewal_process": "Nie wymaga odnowienia. Aktualizowana przy zmianach w produkcie lub normach."
            },
            "paszport_techniczny": {
                "type": "Paszport techniczny urządzenia",
                "fields": ["Nazwa urządzenia", "Model", "Numer seryjny", "Producent", "Data produkcji",
                           "Parametry techniczne", "Historia przeglądów"],
                "content": "Dokument zawierający dane techniczne urządzenia oraz historię jego eksploatacji i przeglądów.",
                "issuer": "Producent lub serwis",
                "renewal_process": "Nie wymaga odnowienia. Uzupełniany przy przeglądach i naprawach."
            },
            "protokol_odbioru": {
                "type": "Protokół odbioru",
                "fields": ["Przekazujący", "Odbierający", "Przedmiot odbioru", "Stan przedmiotu", "Uwagi",
                           "Data odbioru"],
                "content": "Dokument potwierdzający odbiór przedmiotu, usługi lub pracy przez odbiorcę od przekazującego.",
                "issuer": "Strony (przekazujący i odbierający)",
                "renewal_process": "Nie wymaga odnowienia. Dokument jednorazowy."
            },
            "plan_ewakuacyjny": {
                "type": "Plan ewakuacyjny",
                "fields": ["Nazwa i adres obiektu", "Schemat budynku", "Drogi ewakuacyjne", "Miejsca zbiórki",
                           "Data opracowania"],
                "content": "Dokument zawierający graficzne przedstawienie dróg ewakuacyjnych w budynku.",
                "issuer": "Zarządca obiektu lub specjalista BHP",
                "renewal_process": "Aktualizowany przy zmianach w układzie budynku lub przepisach. Czas odnowienia: 1-30 dni."
            },

            # DOKUMENTY ELEKTRONICZNE
            "certyfikat_podpisu_elektronicznego": {
                "type": "Certyfikat podpisu elektronicznego",
                "fields": ["Imię i nazwisko", "Numer PESEL", "Wystawca certyfikatu", "Klucz publiczny", "Data wydania",
                           "Data ważności"],
                "content": "Dokument elektroniczny umożliwiający składanie podpisu elektronicznego.",
                "issuer": "Kwalifikowany podmiot świadczący usługi certyfikacyjne",
                "renewal_process": "Ważny przez określony czas (zwykle 1-3 lata). Wymaga złożenia wniosku przed upływem ważności. Czas odnowienia: 1-7 dni."
            },
            "licencja_oprogramowania": {
                "type": "Licencja oprogramowania",
                "fields": ["Nazwa oprogramowania", "Producent", "Numer licencji", "Typ licencji", "Liczba stanowisk",
                           "Data wydania", "Data ważności"],
                "content": "Dokument określający prawa użytkownika do korzystania z oprogramowania.",
                "issuer": "Producent oprogramowania",
                "renewal_process": "Wymaga odnowienia przed upływem okresu ważności. Czas odnowienia: 1-3 dni."
            },
            "profil_zaufany": {
                "type": "Potwierdzenie profilu zaufanego",
                "fields": ["Imię i nazwisko", "PESEL", "Login", "Data utworzenia", "Data ważności"],
                "content": "Dokument potwierdzający posiadanie profilu zaufanego, umożliwiającego załatwianie spraw urzędowych online.",
                "issuer": "Punkt potwierdzający profil zaufany",
                "renewal_process": "Ważny przez określony czas (zwykle 3 lata). Wymaga przedłużenia online lub w punkcie potwierdzającym. Czas odnowienia: 1 dzień."
            },
            "token_bezpieczenstwa": {
                "type": "Karta/token bezpieczeństwa",
                "fields": ["Użytkownik", "Numer seryjny", "Wydawca", "Data wydania", "Data ważności"],
                "content": "Urządzenie fizyczne służące do weryfikacji tożsamości użytkownika w systemach informatycznych.",
                "issuer": "Administrator systemu lub instytucja finansowa",
                "renewal_process": "Wymaga odnowienia przed upływem okresu ważności. Czas odnowienia: 1-14 dni."
            },
            "dostep_vpn": {
                "type": "Certyfikat dostępu VPN",
                "fields": ["Użytkownik", "Organizacja", "Serwer VPN", "Poziom dostępu", "Data wydania",
                           "Data ważności"],
                "content": "Dokument elektroniczny umożliwiający bezpieczne połączenie z siecią prywatną przez internet.",
                "issuer": "Administrator systemu informatycznego",
                "renewal_process": "Wymaga odnowienia przed upływem okresu ważności. Czas odnowienia: 1-3 dni."
            },
            "konto_administratora": {
                "type": "Uprawnienia administratora systemu",
                "fields": ["Użytkownik", "System", "Zakres uprawnień", "Data nadania", "Data ważności"],
                "content": "Dokument określający uprawnienia użytkownika do administrowania systemem informatycznym.",
                "issuer": "Dział IT lub administrator bezpieczeństwa informacji",
                "renewal_process": "Może wymagać okresowego odnowienia zgodnie z polityką bezpieczeństwa organizacji. Czas odnowienia: 1 dzień."
            },

            # MIĘDZYNARODOWE DOKUMENTY I CERTYFIKATY
            "apostille": {
                "type": "Apostille",
                "fields": ["Dokument, którego dotyczy", "Państwo wydania", "Organ wydający", "Data wydania",
                           "Numer apostille"],
                "content": "Poświadczenie dokumentu urzędowego do użytku w państwach będących stronami Konwencji haskiej.",
                "issuer": "Ministerstwo Spraw Zagranicznych",
                "renewal_process": "Nie wymaga odnowienia. Ważny bezterminowo dla danego dokumentu."
            },
            "karta_polaka": {
                "type": "Karta Polaka",
                "fields": ["Imię i nazwisko", "Data urodzenia", "Miejsce urodzenia", "Obywatelstwo", "Data wydania",
                           "Data ważności"],
                "content": "Dokument potwierdzający przynależność do narodu polskiego dla osób nieposiadających obywatelstwa polskiego.",
                "issuer": "Konsul RP",
                "renewal_process": "Ważna przez 10 lat. Wymaga złożenia wniosku o przedłużenie. Czas odnowienia: 30-60 dni."
            },
            "zezwolenie_na_prace": {
                "type": "Zezwolenie na pracę dla cudzoziemca",
                "fields": ["Imię i nazwisko cudzoziemca", "Obywatelstwo", "Pracodawca", "Stanowisko", "Data wydania",
                           "Data ważności"],
                "content": "Dokument uprawniający cudzoziemca do legalnej pracy na terytorium Polski.",
                "issuer": "Urząd wojewódzki",
                "renewal_process": "Wymaga złożenia nowego wniosku przed upływem ważności. Czas odnowienia: 30-90 dni."
            },
            "zaswiadczenie_a1": {
                "type": "Zaświadczenie A1",
                "fields": ["Imię i nazwisko", "PESEL", "Pracodawca", "Kraj delegowania", "Okres delegowania",
                           "Data wydania"],
                "content": "Dokument potwierdzający podleganie polskiemu systemowi ubezpieczeń społecznych podczas pracy w innym kraju UE/EFTA.",
                "issuer": "Zakład Ubezpieczeń Społecznych (ZUS)",
                "renewal_process": "Wydawane na określony czas delegowania. Wymaga złożenia nowego wniosku. Czas odnowienia: 14-30 dni."
            },
            "karta_ue": {
                "type": "Karta pobytu członka rodziny obywatela UE",
                "fields": ["Imię i nazwisko", "Data urodzenia", "Obywatelstwo", "Adres zamieszkania", "Data wydania",
                           "Data ważności"],
                "content": "Dokument potwierdzający prawo pobytu członka rodziny obywatela UE na terytorium Polski.",
                "issuer": "Urząd wojewódzki",
                "renewal_process": "Ważna przez 5 lat. Wymaga złożenia wniosku o przedłużenie. Czas odnowienia: 30-60 dni."
            },
            "pozwolenie_na_pobyt_staly": {
                "type": "Zezwolenie na pobyt stały",
                "fields": ["Imię i nazwisko", "Data urodzenia", "Obywatelstwo", "Adres zamieszkania", "Data wydania",
                           "Data ważności"],
                "content": "Dokument uprawniający cudzoziemca do stałego pobytu na terytorium Polski.",
                "issuer": "Urząd wojewódzki",
                "renewal_process": "Wydawane bezterminowo. Karta pobytu wymaga wymiany co 10 lat. Czas odnowienia karty: 30-60 dni."
            },

            # INNE SPECJALISTYCZNE DOKUMENTY
            "ksiazeczka_wojskowa": {
                "type": "Książeczka wojskowa",
                "fields": ["Imię i nazwisko", "Data urodzenia", "PESEL", "Stopień wojskowy", "Specjalność wojskowa",
                           "Data wydania"],
                "content": "Dokument potwierdzający stosunek do służby wojskowej.",
                "issuer": "Wojskowa Komenda Uzupełnień (WKU)",
                "renewal_process": "Dokument bezterminowy. Aktualizowany podczas ćwiczeń lub służby wojskowej."
            },
            "ksiazeczka_zczepien_zwierzat": {
                "type": "Książeczka szczepień zwierzęcia",
                "fields": ["Dane właściciela", "Gatunek zwierzęcia", "Imię zwierzęcia", "Rasa", "Numer chipa",
                           "Historia szczepień"],
                "content": "Dokument zawierający historię szczepień i zabiegów weterynaryjnych zwierzęcia.",
                "issuer": "Lekarz weterynarii",
                "renewal_process": "Nie wymaga odnowienia. Uzupełniana przy kolejnych szczepieniach i zabiegach."
            },
            "paszport_zwierzecia": {
                "type": "Paszport zwierzęcia",
                "fields": ["Dane właściciela", "Gatunek zwierzęcia", "Imię zwierzęcia", "Rasa", "Numer chipa",
                           "Data szczepienia przeciwko wściekliźnie"],
                "content": "Dokument umożliwiający przewóz zwierzęcia przez granice w ramach UE.",
                "issuer": "Upoważniony lekarz weterynarii",
                "renewal_process": "Dokument bezterminowy. Wymaga aktualizacji szczepień zgodnie z wymaganiami."
            },
            "pozwolenie_na_bron": {
                "type": "Pozwolenie na broń",
                "fields": ["Imię i nazwisko", "PESEL", "Adres zamieszkania", "Rodzaj pozwolenia",
                           "Cel posiadania broni", "Data wydania", "Data ważności"],
                "content": "Dokument uprawniający do nabycia i posiadania broni.",
                "issuer": "Komendant wojewódzki Policji",
                "renewal_process": "Wymaga odnowienia co 5 lat. Czas odnowienia: 30-60 dni."
            },
            "patent_sternika": {
                "type": "Patent sternika motorowodnego",
                "fields": ["Imię i nazwisko", "Data urodzenia", "Numer patentu", "Uprawnienia", "Data wydania"],
                "content": "Dokument uprawniający do prowadzenia jachtów motorowych po wodach śródlądowych i morskich.",
                "issuer": "Polski Związek Motorowodny i Narciarstwa Wodnego",
                "renewal_process": "Dokument bezterminowy, nie wymaga odnowienia."
            },
            "patent_zeglarza": {
                "type": "Patent żeglarza jachtowego",
                "fields": ["Imię i nazwisko", "Data urodzenia", "Numer patentu", "Uprawnienia", "Data wydania"],
                "content": "Dokument uprawniający do prowadzenia jachtów żaglowych po wodach śródlądowych i określonych wodach morskich.",
                "issuer": "Polski Związek Żeglarski",
                "renewal_process": "Dokument bezterminowy, nie wymaga odnowienia."
            },
            "licencja_pilota": {
                "type": "Licencja pilota",
                "fields": ["Imię i nazwisko", "Data urodzenia", "Typ licencji", "Uprawnienia", "Ograniczenia",
                           "Data wydania", "Data ważności"],
                "content": "Dokument uprawniający do pilotowania statków powietrznych określonego typu.",
                "issuer": "Urząd Lotnictwa Cywilnego",
                "renewal_process": "Wymaga odnowienia co 2-5 lat, zależnie od typu licencji i wieku pilota. Czas odnowienia: 14-30 dni."
            },
            "karta_rowerowa": {
                "type": "Karta rowerowa",
                "fields": ["Imię i nazwisko", "Data urodzenia", "Numer karty", "Data wydania", "Organ wydający"],
                "content": "Dokument uprawniający do kierowania rowerem po drogach publicznych przez osoby w wieku 10-18 lat.",
                "issuer": "Dyrektor szkoły lub WORD",
                "renewal_process": "Dokument bezterminowy, nie wymaga odnowienia."
            },
            "legitymacja_osoby_niepelnosprawnej": {
                "type": "Legitymacja osoby niepełnosprawnej",
                "fields": ["Imię i nazwisko", "PESEL", "Stopień niepełnosprawności", "Symbol niepełnosprawności",
                           "Data ważności"],
                "content": "Dokument potwierdzający status osoby niepełnosprawnej, uprawniający do różnych ulg i świadczeń.",
                "issuer": "Powiatowy Zespół ds. Orzekania o Niepełnosprawności",
                "renewal_process": "Ważna przez okres ważności orzeczenia o niepełnosprawności. Wymaga ponownego złożenia wniosku. Czas odnowienia: 30-60 dni."
            },

            # PROJEKTY AKADEMICKIE
            "projekt_akademicki": {
                "type": "Karta projektu akademickiego",
                "fields": ["Tytuł projektu", "Opiekun projektu", "Jednostka", "Opis projektu", "Kompetencje"],
                "content": "Dokument opisujący zakres projektu studenckiego i związane z nim kompetencje.",
                "issuer": "Uczelnia wyższa",
                "renewal_process": "Nie wymaga odnowienia. Dokument informacyjny o charakterze akademickim."
            },
            "praca_dyplomowa": {
                "type": "Praca dyplomowa",
                "fields": ["Tytuł pracy", "Autor", "Promotor", "Recenzent", "Rodzaj pracy", "Data złożenia"],
                "content": "Dokument naukowy stanowiący podstawę do uzyskania dyplomu uczelni wyższej.",
                "issuer": "Student pod kierunkiem promotora",
                "renewal_process": "Nie wymaga odnowienia. Dokument akademicki o charakterze naukowym."
            },
            "plan_studiow": {
                "type": "Plan studiów",
                "fields": ["Kierunek studiów", "Specjalność", "Wykaz przedmiotów", "Punkty ECTS", "Rok akademicki"],
                "content": "Dokument określający program kształcenia na danym kierunku studiów.",
                "issuer": "Uczelnia wyższa",
                "renewal_process": "Aktualizowany w każdym roku akademickim lub przy zmianach programu studiów."
            },
            "protokol_egzaminu": {
                "type": "Protokół egzaminu",
                "fields": ["Przedmiot", "Prowadzący", "Data egzaminu", "Lista studentów", "Oceny"],
                "content": "Dokument zawierający wyniki egzaminu z danego przedmiotu.",
                "issuer": "Egzaminator/uczelnia",
                "renewal_process": "Nie wymaga odnowienia. Dokument jednorazowy."
            },
            "karta_okresowych_osiagniec": {
                "type": "Karta okresowych osiągnięć studenta",
                "fields": ["Dane studenta", "Kierunek studiów", "Semestr", "Przedmioty", "Oceny", "Punkty ECTS"],
                "content": "Dokument podsumowujący osiągnięcia studenta w danym semestrze studiów.",
                "issuer": "Uczelnia wyższa",
                "renewal_process": "Wystawiana na koniec każdego semestru. Nie wymaga odnowienia."
            }
        }