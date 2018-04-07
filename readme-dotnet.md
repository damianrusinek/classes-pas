# Jak postawić projekt w .net?
## Platformy
Poradnik dla tych, którzy chcą stworzyć sobie projekt .net niezależnie od systemu operacyjnego. Jeśli chcesz używać tylko windowsa do developmentu, to postaw projekt w visualu i przejdź do ostatniego punktu

## Instalacja .net core
Pobieramy sdk dla swojej platformy [stąd](https://www.microsoft.com/net/download/windows) i instalujemy
## Nowy projekt

```sh
mkdir nazwa-projektu && cd nazwa-projektu
dotnet new console
```
Powyższe polecenie tworzy nowy konsolowy projekt .net core z nazwą odpowiadającą nazwie folderu, z którego wykonalismy polecenie ```dotnet new```.
Domyślnie tworzony jest projekt w języku C#, ale nic nie stoi na przeszkodzie żeby wybrać F# (dla ambitnych albo pasjonatów programowania funkcyjnego) lub VBA 😀
Szczegółowe opcje komend .net core znajdziemy [tutaj](https://github.com/dotnet/docs/tree/master/docs/core/tools)
## Uruchamianie

Po zmodyfikowaniu Program.cs możemy uruchomić nasz projekt za pomocą polecenia
```dotnet run```.
Polecenie to buduje program i go uruchamia. Możemy do niego dodać argumenty podane w łańcuchu znaków:
```dotnet run "127.0.0.1"```
Jeśli uzywamy opcjonalnych flag polecenia ```run```, argumenty do naszego programu podajemy na samym końcu, np:
```
dotnet run --project /projects/tutorial/tutorial.csproj "192.168.10.1" "8080"
```

### Tworzenie pliku wykonywalnego na konkretną platformę 

Słuzy do tego polecenie ```dotnet publish```
Możemy za jego pomocą wygenerować katalog z np. exec na windowsa lub linuxową binarkę, który będzie zawierał wymagane biblioteki niezależnie od tego, czy na danej platformie jest zainstalowany .net core. 
Przykład:
```
dotnet publish -c Release -r win10-x64
```
gdzie ostatni argument to RID systemu operacyjnego, których listę można znaleźć [tutaj](https://github.com/dotnet/docs/blob/master/docs/core/rid-catalog.md)
wykonywalny plik jest w folderze
```nazwa-projektu\bin\Release\netcoreapp2.0\win10-x64\nazwa.projektu.exe```, analogicznie do dostarczonych opcji
Jeśli pominiemy flagę -r, wygenerowany zostanie plik korzystający z instalacji .netu maszyny, na której go uruchomimy