#!/usr/bin/env python3
"""Vytvoří adresář kanálu pro GitHub Pages: firmware + manifest.json.

Použití: make_manifest.py <build_dir> <out_dir> <version> <channel>
  build_dir  … .esphome/build/<name>  (hledá firmware.factory.bin a OTA image)
  out_dir    … cílový adresář kanálu (např. out/beta)
"""
import hashlib, json, pathlib, shutil, sys

build_dir, out_dir, version, channel = sys.argv[1:5]
build = pathlib.Path(build_dir)
out = pathlib.Path(out_dir)
out.mkdir(parents=True, exist_ok=True)

def find(names):
    for n in names:
        hits = sorted(build.rglob(n))
        if hits:
            return hits[0]
    sys.exit(f"Nenalezen žádný z {names} v {build}")

factory = find(["firmware.factory.bin"])
ota = find(["firmware.ota.bin", "firmware.bin"])

shutil.copy(factory, out / "rohus-iri.factory.bin")
shutil.copy(ota, out / "rohus-iri.ota.bin")
md5 = hashlib.md5((out / "rohus-iri.ota.bin").read_bytes()).hexdigest()

manifest = {
    "name": "Rohus IRI",
    "version": version,
    "home_assistant_domain": "esphome",
    "new_install_prompt_erase": True,
    "builds": [{
        "chipFamily": "ESP32-C3",
        "parts": [{"path": "rohus-iri.factory.bin", "offset": 0}],
        "ota": {
            "path": "rohus-iri.ota.bin",
            "md5": md5,
            "summary": f"Rohus IRI {version} ({channel})",
            "release_url": f"https://github.com/koubis22/rohus-iri-firmware/releases/tag/v{version}",
        },
    }],
}
(out / "manifest.json").write_text(json.dumps(manifest, indent=2))
print(f"{channel}: {version} md5={md5}")
