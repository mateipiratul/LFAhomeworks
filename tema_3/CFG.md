# Gramatici independente de context *(CFG)*

*proiect de Cocu Matei-Iulian*

În această documentație va fi prezentată implementarea gramaticii independente de context `S → aSb | ε`, cât și aplicații ce au legătură cu aceasta.

## Conținut
- [1. Definirea](#1-definirea)
- [2. Generarea](#2-generarea)
- [3. Derivarea](#3-derivarea)
- [4. Apartenența](#4-apartenența)
- [5. Scriptul principal](#5-scriptul-principal)
- [6. Bonus](#6-bonus)

## 1. Definirea
Implementarea este făcută prin intermediul clasei `CFG`, ce reprezintă *clasa obiectelor gramaticilor independente de context*, și conține datele membre: `non_terminals`*(structura de date set(), pentru memorarea simbolurilor neterminale)*, `terminals`*(structura de date set(), pentru memorarea simbolurilor terminale)*, `productions`*(structura de date hashmap, pentru memorarea producțiilor în funcție de simbolul de plecare)*, `start_symbol`*(string pentru memorarea simbolului de start)*.
De asemenea, clasa are funcțiile membre: `set_start_symbol`, pentru setarea simbolului de start, primit prin parametrul funcției (a se apela o singură dată pentru o instanțierea unui obiect) și `add_production`, care primește de la cei doi parametrii simbolul de plecare al producției (în format string) și, bineînțeles, producția în sine (tot sub formă de string), simbolurile componente ale acesteia fiind adăugate în mulțimiile specifice acestora. Pentru afișarea simplă a definirii gramaticii, cât și cea separată pe componente, sunt implementate prin funcțiile membre `print_cfg`, respectiv `print_cfg_info`.
În plus, necesară pentru implementarea generatorului de cuvinte bazat pe gramatica dată, este funcția membră `production_choice`, care alege, la întâmplare, o producție asociată simbolului parametrizat, cu mențiunea că șansele simbolului epsilon, asta în cazul în care există măcar, sunt înjumătățite.

## 2. Generarea
Funcția `string_generator` primește ca parametrii trei elemente: gramatica independentă de context aleasă, un număr maxim de cuvinte de generat *(al cărui valoare default este `10`)*, și valoarea lungimii maxime posibile pentru un cuvânt generat *(al cărei valoare default este `10`)*, și generează aleator, cu posibilitatea de repetare a anumitor elemente, **un array de cuvinte ce aparțin CFG-ului dat**, al cărui elemente sunt afișate pe ecran și, ulterior, returnate.

## 3. Derivarea
Funcția `membership_derivation` rezolvă simultan apartenența unui cuvânt dat la un limbaj independent de context și derivarea acestuia, în cazul pozitiv. Aceasta primește ca parametrii *un CFG* și cuvântul de verificat. 
Este simulată o stivă a pașilor făcuți, și, prin apelul recursiv al funcției `find_derivation`, care returnează valori booleene, este determinată apartenența cuvântului la limbaj. Bineînțeles, dacă acesta aparține, sunt afișați pașii luați pentru derivarea cuvântului, iar în caz contrar, este afișat un mesaj corespunzător.
În cadrul funcției recursive, este inițial adăugat în stiva simulată cuvântul curent; dacă acesta coincide cu cel cerut de verificat, funcția returnează valoarea booleană `True`, iar în caz contrar, se continuă execuția funcției: dacă cuvântul curent nu mai are nici un simbol neterminal, dar nu coincide cu cel intenționat, sau dacă acesta are o lungime mai mare decât cuvântul de verificat, este scos de pe stivă, iar funcția returnează valoarea booleană `False`. Ulterior, dacă cuvântul trece de aceste verificări, pentru fiecare producție posibilă neterminală, este reactualizat, iar funcția este apelată (recursiv) din nou; acest proces se repetă, bineînțeles, până când se ajunge la unul dintre cele două cazuri posibile.

## 4. Apartenența
Acest pas este verificat în funcția explicată anterior, aceasta returnând valori booleene conforme răspunsului dat; implementarea acesteia are o funcționalitate optimă, cazurile de recursivitate infinită fiind rezolvate prin verificările inițiale prin care trebuie să treacă cuvântul la un moment dat:
```
if not any(symbol in cfg.non_terminals for symbol in current_string):
    steps.pop() # if there are not any non-terminal symbols left, yet
    return False # the current word does not match with the target

if len(current_string) > len(target_string) + 1:
    steps.pop() # avoid infinite recursion case if the current word
    return False # is bigger than the target word
```

## 5. Scriptul Principal
Este importat modulul `tasks.py`, ce conține implementările descrise anterior, și este instanțiat obiectul clasei `CFG`:
```
cfg = CFG()
cfg.set_start_symbol("S")
cfg.add_production("S", "aSb")
cfg.add_production("S", "ε")
```
Sunt afișate detaliile gramaticii independente de context, setul de cuvinte generate al acesteia, și, ulterior este apelată funcția de derivare și verificare a apartenenței unui cuvânt arbitrar.
Adițional, este creată o nouă gramatică definită prin expresia regulată `a*b*` și un set de cuvinte generat de aceasta, pentru o testare mai elaborată a funcției de apartenență la limbajul definit anterior cu aceste cuvinte.

## 6. Bonus
De ce limbajul `{ aⁿbⁿcⁿ | n ≥ 1 }` NU este un limbaj liber-context

### Definiția limbajului
Limbajul conține șiruri formate din:
- un număr egal de `a`-uri, `b`-uri și `c`-uri,
- în această ordine: toate `a`-urile, urmate de toate `b`-urile, urmate de toate `c`-urile.

### Exemple valide:
- `abc`
- `aabbcc`
- `aaabbbccc`

### Exemple invalide:
- `aabcc` (lipsă un `b`)
- `aaabbbcc` (`#c ≠ #a` și `#b`)

### Problema cu `{ aⁿbⁿcⁿ }`
Pentru a verifica apartenența unui șir la limbaj:
- trebuie comparate **trei cantități egale** (`#a = #b = #c`)
- un PDA are **o singură stivă**, deci poate compara doar două cantități simultan

### Pseudoimplementarea acestui limbaj
În fișierul anex `bonus_task.py`, funcția `bonus_cfg` returnează un șir de cuvinte generate de acest limbaj, dar fără o implementare propriu zisă utilizând clasa `CFG`. Ulterior, este *"încercată"* o asemenea *implementare*, limbajul rezultat fiind: `Labc = {a^i.b^i.c^i}`.