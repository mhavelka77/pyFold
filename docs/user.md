# Uživatelská dokumentace

Po spuštění programu (`uv run python main.py`) se otevřete prohlížeč na adrese `http://127.0.0.1:8000`.

## Ovládání

1. **Sekvence** -- do textového pole zadejte sekvenci aminokyselin jednopísmenným kódem (např. `MQIFVKTLTG...`). Výchozí sekvence je ubiquitin.
2. **Steps** -- počet kroků simulace (výchozí 100, maximum 10 000).
3. **Fold Protein** -- spustí simulaci. Průběh se zobrazuje v reálném čase v pravém 3D panelu. Během skládání se tlačítko změní na **Stop**, kterým lze simulaci kdykoli zastavit.
4. **Generate Reference** -- stáhne referenční strukturu z ESMFold API (Meta) a zobrazí ji v levém panelu pro porovnání.

Oba 3D panely podporují rotaci (tažení myší), zoom (kolečko) a posun (pravé tlačítko).
