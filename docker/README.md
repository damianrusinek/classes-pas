
# Docker - skrypty dla konetenera do zajęć PAS

Wszystkie skrypty omawiane i tworzone podczas zajęć będą dedykowane dla systemów UNIXowych, czyli w szczególności nie będziemy korzystać z WinApi. W związku z tym, przygotowałem skrypt, który wykorzystuje narzędzie Docker do stworzenia tzw. kontenera, w którym będzie uruchomiony system operacyjny Ubuntu 16.04. Dzięki temu, zarówno ja, jak i Ty będziemy mieli jednolite środowisko pracy.

_Wykorzystanie kontenera jest szczególnie przydatne dla tych, którzy używają Windowsa i nie mają maszyny z zainstalowanym Linuxem. Docker stworzy minimalne środowisko Linux, które będzie wykorzystywane tylko do zajęć._

Do stworzenia kontenera potrzebny jest przede wszystkim Docker. Więcej informacji o tym, jak go zainstalować i o pierwszych krokach znajdziesz pod [tym linkiem](https://www.docker.com/products/overview). Następnie wystarczy postępować według poniższych kroków.

_Jeśli instalujesz Dockera na Windowsie, pamiętaj o stworzeniu maszyny wirtualnej dockera. Spokojnie, wszystko jest tworzone i uruchamiane automatycznie i sprowadza się do uruchomienia kilku komend. Wszystkie informacje znajdzieć w sekcji Get Started pod powyżej wspomnianym linkiem._

## Kilka uwag dla użytkowników Windowsa

Komendy, o których będę wspominał należy uruchamiać w wierszu poleceń, który można uruchomić, jak każdą inną aplikację (wyszukać słowo `cmd`). Jeśli posiadasz Windows z PowerShellem, to w nim również można uruchamiać komendy.

Poniżej wypisywane komendy będą typowe dla środowiska Linux, także nie zdziw się, gdy w wierusz poleceń Widnowsa zamiast `docker exec ...` pojawi się `docker.exe exec ...`.

*Uwaga!* Przed przejściem do sekcji _Zbudowanie i uruchomienie środowiska_ należy wykonać następujące kroki (dokładniej opisane [tutaj](https://docs.docker.com/machine/get-started/)):

1. Stworzyć maszynę wirtualną za pomocą komendy `docker-machine.exe create --driver virtualbox default`.
2. Otworzyć program VirtualBox (zarządca maszyn wirtualnych) i w konfiguracji w sekcji _Shared folders_ dodać folder z zajęć (nie _docker/_, ale ten wyżej) jako współdzielony, nazwę folderu ustawić na `pas`, zostawić puste _Read only_ i zaznaczyć pozostałe checkboxy. Zatwierdzić i zamknąć VirtualBox.
3. Uruchomić komendę `docker-machine.exe env default`, a następnie uruchomić ostatnią, zakomentowaną linię z wyświetlonego wyniku (np. `eval "$(docker-machine env default)"`).
4. Uruchomić komendę `docker-machine.exe ssh default 'sudo mkdir --parents /opt/pas'` (stworzenie folderu w maszynie wirtualnej).
5. Uruchomić komendę `docker-machine.exe ssh default 'sudo mount -t vboxsf pas /opt/pas'` (zamontowanie współdzielonego folderu na maszynie wirtualnej).

Powyższe kroki mają na celu umożliwienie na systemie Windows współdzielenia plików z Windows z kontenerem, o czym wspominam w jednym z kroków poniżej. Jeśli chcesz sprawdzić, czy powyższe kroki zostały wykonane pomyślnie, wykonaj następujący test:

1. Jeśli jesteś w tym samym wierszu poleceń, przeskocz do pkt. 3.
2. Uruchom komendę `docker-machine.exe env default`, a następnie uruchomić ostatnią, zakomentowaną linię z wyświetlonego wyniku (np. `eval "$(docker-machine env default)"`).
3. Uruchom komendę `docker-machine.exe ssh default 'ls -la /opt/pas'`.
4. Jeśli widzisz listę plików z folderu z zajęć, to wszystko jest OK. Jeśli nie ma żadnego pliku (sam napis `total 0`), to sprawdź jeszcze raz powyżej wymienione kroki.

## Kilka uwag dla użytkowników Linuxa

Dla użytkowników Linuxa istnieje skrypt, który automatycznie realizuje kroki 1 i 2. Znajduje się on w pliku `run_linux.sh` i można go wywołać wpisując `bash run_linux.sh`.

## Zbudowanie i uruchomienie środowiska

1. Zbudowanie obrazu

	Kontener to taki uruchomiony komputer z systemem operacyjnym i być może dodatkowo zainstalowanymi programami. Obraz z kolei to taki prototyp dla kontenera, z którego docker korzysta jak chce uruchomić nowy kontener.  

	Komenda, która zbuduje nam obraz to `docker build -t pas:latest .` uruchamiana z poziomu folderu `docker/`.

	Budowanie obrazu może chwilę pobrać, ponieważ docker musi pobrać obraz systemu oraz doinstalować programy, jednakże operacja ta jest wykonywana jednorazowo. 

2. Uruchomienie kontenera

	Po zbudowaniu obrazu możemy na jego podstawie uruchomić kontener. W tym celu należy uruchomić jedną z poniższych komend, w zależności na jakim systemie działasz.

	Linux: `docker run --d --name pas -v <sciezka_bezwzgledna_do_folderu_z_zajec>:/opt/pas pas:latest`
	Windows: `docker.exe run --d --name pas -v //opt/pas:/opt/pas pas:latest`

	Kontener zostanie uruchomiony i będziesz mógł/mogła się z nim połączyć. 

3. Połączenie z kontenerem

	Niektórzy lubią połączyć się z kontenerem i uruchamiać wszystkie komendy (np. kompilujące kod lub uruchamiające program) bezpośrednio z linii poleceń kontenera, a inni wolą pośrednio przez dockera. Ta sekcja jest dla pierwszej grupy.

	Po uruchomieniu kontenera w punkcie 2 musisz wywołać komendę `docker exec -it pas bash`, żeby przejść do jego wiersza poleceń. *To jest punkt wyjścia dla wszystkich przykładów i zadań omawianych na zajęciach*. Możesz sprawdzić, czy wszystko działa uruchamiając komendę `ls -la`. Powinna pojawić się lista współdzielonych plików z folderu z zajęć. Jeśli chcesz powrócić do wiersza poleceń systemu głównego, wystarczy że wciśniesz Ctrl+D. Po opuszczeniu kontenera on wciąż działa i ma się dobrze. Jeśli chcesz do niego powrócić (np. żeby uruchomić program, który właśnie zmieniłeś/łaś) musisz wywołać ponownie komendę `docker exec -it pas bash`. Podobnie, jak wcześniej pojawi się jego wiersz poleceń.

	*Jeśli z jakiegoś powodu, w dalszej pracy, kontener przestanie działać, możesz go usunąć i stworzyć na nowo. Usunięcie kontenera polega na uruchomieniu komendy `docker rm -f pas`. Nie martw się, nie stracisz plików, ponieważ one są tak naprawdę na Twoim systemie głównym, a w kontenerze są tylko współdzielone.*

	_Oczywiście istnieje możliwość połączenia się z kontenerem przez SSH, jednakże opcja, którą udostępnia docker jest wygodniejsza, bo nie wymaga konfiguracji (np. stworzenia konta użytkownika i ustawienia hasła). To tylko pokazuje, że dla każdego problemu istnieje wiele rozwiązań._

4. Uruchamianie komend na kontenerze bez połączenia

	Druga opcja uruchamiania komend w kontenerze polega na wykorzystaniu mechanizmu dockera, z którego tak naprawdę korzystamy w punkcie 3 również. Zauważ, że tam wywołujemy `docker exec -it pas bash`, żeby uruchomić bash. Jednakże ostatni argument możemy zastąpić dowolną komendą, która ma być uruchomiona na kontenerze, i tak zmieniamy naszą komendę na `docker exec -it pas <komenda_do_uruchomienia_na_kontenerze>` (np. `docker exec -it pas python skrypt.py`.).

	Jednakże, jeśli komenda do uruchomienia na kontenerze ma być komendą bash, to bezpieczniej użyć polecenia `docker exec -it pas bash -c "<komenda_do_uruchomienia_na_kontenerze>"`, ponieważ unikniemy pewnych problemów, które na początku nie rzucają się w oczy. 

	Spójrzmy na przykład na dwie komendy: `docker exec -it pas echo $HOME` i `docker exec -it pas bash -c "echo \$HOME"`. Teoretycznie obie powinny wyświetlić ścieżkę do katalogu domowego w kontenerze, czyli `/root`, jednakże w przypadku pierwszej z nich tak się nie dzieje. Dlaczego? Bo wartość `$HOME` jest obliczana przed przekazaniem do kontenera, czyli na kontenerze tak naprawdę wykonywana jest komenda `echo <sciezka_do_katalogu_domowego_na_glownym_systemie>`.

5. That's all folks

	W tym momencie masz gotowe środowisko uruchomieniowe dla programów i skryptów napisanych na zajęciach. Pamiętaj, że współdzielisz folder z zajęć (i tylko ten folder), więc możesz modyfikować pliki na systemie głównym (np. na Windowsie), a kompilować i uruchamiać w kontenerze bezpośrednio po wcześniejszym połączeniu się z kontenerem (pkt. 3) lub pośrednio przez dockera (pkt. 4).

	Szybka powtówka komend:

	* Zbudowanie obrazu (jednorazowe)

		`docker build -t pas:latest .` uruchamiana z poziomu folderu `docker/`.

	* Uruchomienie kontenera (optymistycznie jednorazowe)

		Linux: `docker run --d --name pas -v <sciezka_bezwzgledna_do_folderu_z_zajec_na_systemie_glownym>:/opt/pas pas:latest`
		Windows: `docker.exe run --d --name pas -v //opt/pas:/opt/pas pas:latest`

	* Usunięcie kontenera
		
		`docker rm -f pas`

	* Połączenie z kontenerem
		
		`docker exec -it pas bash`.

	* Uruchomienie komendy przez dockera
		
		`docker exec -it pas bash -c "<komenda_do_uruchomienia_na_kontenerze>"`.
