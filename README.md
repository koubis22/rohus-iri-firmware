# Rohus IRI – firmware

ESPHome firmware řídicí jednotky závlahy **Rohus irrigation controller** (12 zón, 24 VAC, XIAO ESP32-C3 + MCP23017, HW v0.9).

## Struktura

| Soubor | Účel |
|---|---|
| `rohus-iri.yaml` | **zákaznický build**: bez tajných údajů, staví ho GitHub Actions |
| `rohus-iri-dev.yaml` | **vývojový build** pro vlastní kusy (ESPHome dashboard, WiFi a API klíč ze `secrets.yaml`) |
| `packages/base.yaml` | ESP32-C3, reset MCP (GPIO5, priorita 1000), WiFi/captive portal/Improv, API, I²C, MCP23017 |
| `packages/update.yaml` | aktualizace z GitHub Pages (`http_request`) |
| `packages/zones.yaml` | 12 zón: interlock, `ALWAYS_OFF`, bezpečnostní limit `zone_max_on` |
| `packages/rain_gauge.yaml` | srážkoměr (Hallova sonda, GPIO3, aktivní LOW) |
| `tools/make_manifest.py` | vytvoří `manifest.json` (ESP Web Tools + OTA, MD5) |
| `static/index.html` | instalační stránka pro první nahrání přes prohlížeč |
| `.github/workflows/release.yml` | build a publikace po tagu |

## Kanály

| Tag | Kanál | Kdo ho dostane |
|---|---|---|
| `v0.2.0-beta1` | `beta` | testovací kusy |
| `v0.2.0` | `stable` (a zároveň `beta`) | zákazníci |

Zařízení kontroluje `https://koubis22.github.io/rohus-iri-firmware/<kanál>/manifest.json` každých 6 h. Aktualizaci spouští uživatel **ručně** v HA (entita *Firmware update*), protože instalace restartuje jednotku a přeruší probíhající zalévání.

## První nastavení repozitáře

1. Na GitHubu vytvoř **veřejný** repozitář `koubis22/rohus-iri-firmware` (prázdný).
2. Nahraj do něj obsah této složky.
3. **Settings → Actions → General → Workflow permissions:** *Read and write permissions*.
4. Vytvoř první tag, např. `v0.1.0-beta1` (*Releases → Draft a new release → Choose a tag*).
5. Po doběhnutí Actions: **Settings → Pages → Source:** *Deploy from a branch*, branch **`gh-pages`**, složka `/ (root)`.
6. Instalační stránka: `https://koubis22.github.io/rohus-iri-firmware/`.

## Vydání nové verze

1. Uprav YAML a zapiš změnu do `CHANGELOG.md`.
2. Otestuj lokálně přes `rohus-iri-dev.yaml`.
3. Tag `vX.Y.Z-betaN`: testovací kusy dostanou nabídku aktualizace.
4. Po otestování tag `vX.Y.Z`: dostanou ji zákazníci.

## Zásady

- **entity_id zůstávají anglicky** (podle `name` v YAML). Českou lokalizaci řeš jen přes zobrazovaný název v HA, entity_id se nikdy nemění.
- Do zákaznického buildu **nepatří žádné tajné údaje**. `secrets.yaml` je v `.gitignore`.
- API šifrování je zapnuté **bez pevného klíče** (`encryption: {}`). Klíč lze nastavit za běhu, do té doby API šifrované není.
