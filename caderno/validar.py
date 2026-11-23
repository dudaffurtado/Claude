"""Valida os arquivos YAML de questões. Uso: python3 validar.py arquivo.yaml [...] [--meta]"""
import re
import sys
from collections import Counter

import yaml

LETRAS = list("ABCDE")
CAMPOS = ["nivel", "assunto", "enunciado", "alternativas", "resposta", "comentario", "fundamento"]
ROMANOS = ["I", "II", "III", "IV", "V", "VI"]
MAX_LETRA = 0.30


def carregar(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def questoes(caderno):
    for t in caderno["temas"]:
        for q in t["questoes"]:
            yield t, q


def _erros_questao(rotulo, q):
    erros = [f"{rotulo}: falta {c}" for c in CAMPOS if not q.get(c)]
    alts = q.get("alternativas") or {}
    if sorted(alts) != LETRAS:
        erros.append(f"{rotulo}: alternativas devem ser A–E (tem {sorted(alts)})")
    if q.get("resposta") not in LETRAS:
        erros.append(f"{rotulo}: resposta inválida {q.get('resposta')!r}")
    if q.get("nivel") not in (1, 2, 3):
        erros.append(f"{rotulo}: nível inválido {q.get('nivel')!r}")
    itens = q.get("itens")
    if itens:
        validos = set(ROMANOS[: len(itens)])
        for letra, texto in alts.items():
            citados = re.findall(r"\b(?:VI|IV|V|I{1,3})\b", str(texto))
            fora = [r for r in citados if r not in validos]
            if fora:
                erros.append(f"{rotulo}: alternativa {letra} cita item inexistente {fora}")
    return erros


def erros(caderno, checar_meta):
    out = []
    n = 0
    for ti, t in enumerate(caderno["temas"], 1):
        ultimo = 0
        for qi, q in enumerate(t["questoes"], 1):
            rotulo = f"caderno {caderno['caderno']} tema {ti} questão {qi}"
            out += _erros_questao(rotulo, q)
            nivel = q.get("nivel") or 0
            if nivel < ultimo:
                out.append(f"{rotulo}: nível fora de ordem crescente")
            ultimo = max(ultimo, nivel)
            n += 1
    if checar_meta:
        if n != caderno["meta"]:
            out.append(f"caderno {caderno['caderno']}: {n} questões, meta {caderno['meta']}")
        cont = Counter(q.get("resposta") for _, q in questoes(caderno))
        for letra, k in cont.items():
            if n and k / n > MAX_LETRA:
                out.append(f"caderno {caderno['caderno']}: letra {letra} em {k}/{n} (> {MAX_LETRA:.0%})")
    return out


def main(argv):
    checar = "--meta" in argv
    total, ruins = 0, 0
    for p in [a for a in argv if not a.startswith("--")]:
        c = carregar(p)
        e = erros(c, checar_meta=checar)
        n = sum(1 for _ in questoes(c))
        total += n
        dist = Counter(q["resposta"] for _, q in questoes(c))
        print(f"{p}: {n} questões; respostas {dict(sorted(dist.items()))}")
        for linha in e:
            print("  ERRO", linha)
        ruins += len(e)
    print(f"TOTAL: {total} questões, {ruins} erros")
    return 1 if ruins else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
