# Programátorská dokumentace

## Obsah

- [Struktura projektu](#struktura-projektu)
- [Klíčové třídy a funkce](#klíčové-třídy-a-funkce)

## Struktura projektu

```
pyFold/
├── main.py                  # FastAPI webserver, vstupní bod
├── pyproject.toml           # Konfigurační soubor UV
├── pyfold/
│   ├── engine.py            # Simulační engine (fyzikální model)
│   ├── reference.py         # Volání ESMFold API
│   ├── index.html           # Frontend (HTML + JS + 3Dmol.js)
│   └── data/                # Vzorová data (ubiquitin)
└── docs/
    ├── programmer.md        # Programátorská dokumentace
    └── user.md              # Uživatelská dokumentace
```

## Klíčové třídy a funkce

### Třída `Residue`
*pyfold/engine.py*

```python
class Residue:
    def __init__(self, x, y, z, code, hydrophobic=0)
```

Jeden aminokyselinový zbytek. Uchovává 3D pozici (`position`), jednopísmenný kód (`code`) a příznak hydrofobicity (`hydrophobic`).

### Třída `Chain`
*pyfold/engine.py*

```python
class Chain:
    def __init__(self, seq)
```

Řetězec residuí. Při inicializaci rozmístí residua lineárně s rozestupem `3.8 Å`. Metoda `calculate_timestep()` provede jeden krok simulace — vypočítá síly a aktualizuje pozice. Metoda `__str__()` serializuje aktuální stav do formátu PDB pomocí BioPython.

### Fyzikální model (`calculate_timestep`)
*pyfold/engine.py*

Každý krok počítá tři typy sil:

| Síla | Popis | Prahová vzdálenost |
|------|-------|--------------------|
| **Pružiny páteře** | Udržují sousední residua ve správné vzdálenosti | `3.8 Å` |
| **Sterická repulze** | Odpuzuje residua, která jsou si příliš blízko | `3.0 Å` |
| **Hydrofobní přitažlivost** | Přitahuje páry hydrofobních residuí k sobě | — |

Po aplikaci sil se přidá náhodný šum simulující tepelný pohyb.

> **Poznámka:** Jedná se o zjednodušený fyzikální model sloužící k demonstraci principu protein foldingu, nikoliv o vědecky přesnou simulaci.

### Funkce `fold`
*pyfold/engine.py*

```python
async def fold(seq, steps)
```

Asynchronní generátor volaný z webserveru. Streamuje JSON (NDJSON) s průběžnými PDB daty do frontendu.

### Funkce `reference_fold`
*pyfold/reference.py*

```python
def reference_fold(sequence)
```

Odešle sekvenci na ESMFold API a vrátí PDB odpověď.
