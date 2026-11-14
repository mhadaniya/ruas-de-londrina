#!/usr/bin/env python3
"""Gera data/verbetes.json: a lista das ruas que já têm verbete. O mapa usa essa lista para colorir as ruas."""
import json, pathlib

raiz = pathlib.Path(__file__).resolve().parent.parent
ruas = set(json.loads((raiz / "data" / "ruas.json").read_text(encoding="utf-8"))["n"])

feitas = set()
for arq in (raiz / "verbetes").glob("*.json"):
    try:
        rua = json.loads(arq.read_text(encoding="utf-8")).get("rua")
    except Exception:
        continue
    if rua in ruas:
        feitas.add(rua)

saida = raiz / "data" / "verbetes.json"
saida.write_text(json.dumps(sorted(feitas), ensure_ascii=False, indent=0) + "\n", encoding="utf-8")
print(f"{len(feitas)} ruas com verbete gravadas em {saida.relative_to(raiz)}.")
