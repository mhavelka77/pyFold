# pyFold

Webová aplikace pro simulaci skládání proteinů. Uživatel zadá sekvenci aminokyselin a program v reálném čase vizualizuje průběh skládání pomocí jednoduchého fyzikálního modelu (pružiny, sterika, hydrofobní interakce). Výsledek lze porovnat s referenční strukturou z ESMFold (Meta).

## Instalace a spuštění

Vyžaduje Python 3.13+ a [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python main.py
```

Server se spustí na `http://127.0.0.1:8000`.

## Dokumentace

- [Uživatelská dokumentace](docs/user.md)
- [Programátorská dokumentace](docs/programmer.md)
