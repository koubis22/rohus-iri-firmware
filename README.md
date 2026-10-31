# Rohus IRI – firmware

ESPHome firmware řídicí jednotky závlahy **Rohus irrigation controller** (12 zón, 24 VAC, XIAO ESP32-C3 + MCP23017, HW v0.9).

## Struktura

| Soubor | Účel |
|---|---|
| `rohus-iri.yaml` | **zákaznický build**: bez tajných údajů, staví ho GitHub Actions |
| `base.yaml` | ESP32-C3, reset MCP (GPIO5, priorita 1000), WiFi/captive portal/Improv, API, I²C, MCP23017 |
| `update.yaml` | aktualizace z GitHub Pages (`http_request`) |
| `zones.yaml` | 12 zón: interlock, `ALWAYS_OFF`, bezpečnostní limit `zone_max_on` |
| `rain_gauge.yaml` | srážkoměr (Hallova sonda, GPIO3, aktivní LOW) |
| `make_manifest.py` | vytvoří `manifest.json` (ESP Web Tools + OTA, MD5) |
| `index.html` | instalační stránka pro první nahrání přes prohlížeč |
| `.github/workflows/release.yml` | build a publikace po tagu |

## Kanály

| Repozitář | Kanál | Kdo |
|---|---|---|
| `koubis22/rohus-iri-firmware` (veřejný) | **stable**: tag `vX.Y.Z` → build → GitHub Pages | zákazníci, kdokoli |
| `koubis22/rohus-iri-dev` (soukromý) | **vývoj / beta**: testování přes ESPHome dashboard | jen autor |

Zařízení kontroluje `https://koubis22.github.io/rohus-iri-firmware/stable/manifest.json` každých 6 h. Aktualizaci spouští uživatel **ručně** v HA (entita *Firmware update*), protože instalace restartuje jednotku a přeruší probíhající zalévání.

## Licence

[PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0): pouze nekomerční použití.

## Vydání produkční verze

1. Změny se vyvíjejí a testují v soukromém repozitáři `rohus-iri-dev`.
2. Otestované soubory se zkopírují sem a zapíše se změna do `CHANGELOG.md`.
3. Release s tagem `vX.Y.Z` (`https://github.com/koubis22/rohus-iri-firmware/releases/new`).
4. GitHub Actions sestaví firmware a zveřejní ho do kanálu **stable** (~3–4 min).

## Zásady

- **entity_id zůstávají anglicky** (podle `name` v YAML). Českou lokalizaci řeš jen přes zobrazovaný název v HA, entity_id se nikdy nemění.
- Do zákaznického buildu **nepatří žádné tajné údaje**. `secrets.yaml` je v `.gitignore`.
- API šifrování je zapnuté **bez pevného klíče** (`encryption: {}`). Klíč lze nastavit za běhu, do té doby API šifrované není.
