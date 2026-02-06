# Programátorská dokumentace

## Struktura projektu

- `main.py` -- FastAPI webserver, definuje endpointy
- `pyfold/engine.py` -- simulační engine (fyzikální model)
- `pyfold/reference.py` -- volání ESMFold API pro referenční strukturu
- `pyfold/index.html` -- frontend (HTML + JS + 3Dmol.js)

## Klíčové třídy a funkce

### `Residue`
Jeden aminokyselinový zbytek. Uchovává 3D pozici (`position`), jednopísmenný kód (`code`) a příznak hydrofobicity (`hydrophobic`).

### `Chain`
Řetězec residuí. Při inicializaci rozmístí residua lineárně s rozestupem 3.8 Å. Metoda `calculate_timestep()` provede jeden krok simulace -- vypočítá síly a aktualizuje pozice. Metoda `__str__()` serializuje aktuální stav do formátu PDB pomocí BioPython.

### Fyzikální model (`calculate_timestep`)
Každý krok počítá tři typy sil:
1. **Pružiny páteře** -- udržují sousední residua ve vzdálenosti 3.8 Å
2. **Sterická repulze** -- odpuzuje residua, která jsou si blíže než 3.0 Å
3. **Hydrofobní přitažlivost** -- přitahuje páry hydrofobních residuí k sobě

Po aplikaci sil se přidá náhodný šum simulující tepelný pohyb.

### `fold(seq, steps)`
Asynchronní generátor volaný z webserveru. Streamuje JSON (NDJSON) s průběžnými PDB daty do frontendu.

### `reference_fold(sequence)`
Odešle sekvenci na ESMFold API a vrátí PDB odpověď.

## Komunikace frontend--backend
Frontend volá `POST /fold` a čte odpověď jako NDJSON stream. Každý řádek obsahuje stav simulace a PDB data, která se vykreslují pomocí knihovny 3Dmol.js.
