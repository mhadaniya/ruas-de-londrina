#!/usr/bin/env python3
"""Confere os verbetes: JSON válido, campos obrigatórios, rua existente e nome de arquivo correto."""
import json, pathlib, re, sys, unicodedata

raiz = pathlib.Path(__file__).resolve().parent.parent
ruas = set(json.loads((raiz / "data" / "ruas.json").read_text(encoding="utf-8"))["n"])


def slug(nome):
    s = unicodedata.normalize("NFD", nome)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


erros = []
for arq in sorted((raiz / "verbetes").glob("*")):
    def erro(msg):
        erros.append(f"{arq.name}: {msg}")

    if arq.suffix != ".json":
        erro("o arquivo precisa terminar em .json")
        continue
    try:
        v = json.loads(arq.read_text(encoding="utf-8"))
    except Exception as e:
        erro(f"JSON inválido ({e})")
        continue
    rua = v.get("rua")
    if rua not in ruas:
        erro(f'"rua" precisa ser igual ao nome que aparece no mapa (recebido: {rua!r})')
        continue
    if arq.stem != slug(rua):
        erro(f"o arquivo deveria se chamar {slug(rua)}.json")
    texto = v.get("texto")
    if not (isinstance(texto, list) and texto and all(isinstance(p, str) and p.strip() for p in texto)):
        erro('"texto" precisa ser uma lista de parágrafos não vazios')
    if not isinstance(v.get("confirmado"), bool):
        erro('"confirmado" precisa ser true ou false')
    fontes = v.get("fontes")
    if not (isinstance(fontes, list) and fontes):
        erro('inclua pelo menos uma fonte em "fontes"')
    else:
        for f in fontes:
            if not (isinstance(f, dict) and str(f.get("titulo", "")).strip() and re.match(r"https?://", str(f.get("url", "")))):
                erro('cada fonte precisa de "titulo" e de uma "url" começando com http')

if erros:
    print("\n".join(erros))
    sys.exit(1)
print("Verbetes conferidos, tudo certo.")
