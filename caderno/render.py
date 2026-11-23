"""Monta o HTML do caderno de questões a partir dos YAML. Uso: python3 render.py saida.html dados/*.yaml"""
import pathlib
import sys

import validar

AQUI = pathlib.Path(__file__).resolve().parent
NIVEL = {1: "●", 2: "●●", 3: "●●●"}
ROMANOS = validar.ROMANOS
POR_LINHA = 10
TITULO = "SEFAZ-RS · Auditor-Fiscal da Receita Estadual"

MARCA = ('<div class="marca"><span class="bolhas">' + "".join(f"<span>{l}</span>" for l in "ABCDE")
         + '</span><span><i class="chk"></i>dúvida</span><span><i class="chk"></i>revisar</span>'
           '<span class="notas"></span></div>')


def _runhead(esq, dir_="Estilo FCC"):
    return f'<div class="runhead"><span>{esq}</span><span>{dir_}</span></div>'


def _alternativas(q):
    curtas = all(len(str(v)) <= 18 for v in q["alternativas"].values())
    estilo = ' style="display:grid;grid-template-columns:repeat(3,1fr)"' if curtas else ""
    lis = "".join(f'<li><b>({k})</b><span>{q["alternativas"][k]}</span></li>' for k in "ABCDE")
    return f'<ol class="alt"{estilo}>{lis}</ol>'


def _questao(num, q):
    partes = [f'<div class="q"><div class="qhead"><span class="num">{num:02d}</span>'
              f'<span class="nivel">{NIVEL[q["nivel"]]}</span><span class="assunto">{q["assunto"]}</span></div>',
              f'<p class="enun">{q["enunciado"]}</p>']
    if q.get("itens"):
        lis = "".join(f"<li><b>{ROMANOS[i]}.</b><span>{t}</span></li>" for i, t in enumerate(q["itens"]))
        partes.append(f'<ol class="itens">{lis}</ol>')
        if q.get("comando"):
            partes.append(f'<p class="enun">{q["comando"]}</p>')
    partes += [_alternativas(q), MARCA, "</div>"]
    return "".join(partes)


def _faixa(pares):
    out = []
    for i in range(0, len(pares), POR_LINHA):
        bloco = pares[i:i + POR_LINHA]
        nums = "".join(f"<td>{n:02d}</td>" for n, _ in bloco)
        resp = "".join(f"<td>{r}</td>" for _, r in bloco)
        out.append(f'<table class="gtab"><tr><td>Questão</td>{nums}</tr><tr><td>Resposta</td>{resp}</tr></table>')
    return "".join(out)


def html_caderno(caderno, inicio):
    """Retorna (html_questoes, html_gabarito); numeração contínua a partir de `inicio`."""
    nome = f'Caderno {caderno["caderno"]} — {caderno["materia"]}'
    total_temas = len(caderno["temas"])
    corpo, gab, pares = [], [], []
    num = inicio
    for ti, t in enumerate(caderno["temas"], 1):
        n = len(t["questoes"])
        corpo.append(f'<div class="tbox"><div class="kicker">Tema {ti} de {total_temas} · {n} questões</div>'
                     f'<h3>{t["titulo"]}</h3><div class="base">Base: {t["base"]}</div>'
                     f'<div class="ctl"><span>1ª resolução __/__ · acertos __/{n}</span>'
                     f'<span>Revisão __/__ · acertos __/{n}</span></div></div>')
        gab.append(f'<div class="gtema">Tema {ti} · {t["titulo"]}</div>')
        for q in t["questoes"]:
            corpo.append(_questao(num, q))
            gab.append(f'<div class="gc"><h3>Questão {num:02d} <span class="letra">{q["resposta"]}</span></h3>'
                       f'<p>{q["comentario"]}</p><div class="fund">Fundamento: {q["fundamento"]}</div></div>')
            pares.append((num, q["resposta"]))
            num += 1
    html_q = (f'<section class="page">{_runhead(f"<b>{TITULO}</b> · {nome}")}'
              f'<div class="abertura"><div class="k">Caderno {caderno["caderno"]}</div><h2>{caderno["materia"]}</h2></div>'
              f'<div class="cols">{"".join(corpo)}</div></section>')
    dica = f'<div class="pegadinha">{caderno["dica"]}</div>' if caderno.get("dica") else ""
    html_g = (f'<section class="page">{_runhead(f"<b>Gabarito comentado</b> · {nome}")}'
              f'{_faixa(pares)}<div class="cols gab">{"".join(gab)}</div>{dica}</section>')
    return html_q, html_g


def _capa(total):
    return (f'<section class="capa"><div class="topo">Secretaria da Fazenda do Rio Grande do Sul · Concurso previsto para 2027</div>'
            f'<div><h1>Caderno de Questões<br>Auditor-Fiscal da<br>Receita Estadual</h1>'
            f'<div class="sub">{total} questões inéditas no estilo FCC, organizadas por matéria e tema, com gabarito comentado</div></div>'
            f'<div class="nota">Questões elaboradas para estudo com base na legislação vigente em novembro de 2026. '
            f'A distribuição por matéria segue o último edital (2018) e os editais fiscais recentes da FCC; '
            f'ajuste o foco quando o edital for publicado.</div></section>')


def _sumario(cadernos):
    linhas, num = [], 1
    for c in cadernos:
        n = sum(len(t["questoes"]) for t in c["temas"])
        temas = " · ".join(t["titulo"] for t in c["temas"])
        linhas.append(f'<tr><td class="n">{c["caderno"]:02d}</td><td><b>{c["materia"]}</b>'
                      f'<div class="temas">{temas}</div></td><td class="qs">questões {num:02d}–{num + n - 1:02d}</td></tr>')
        num += n
    como = ('<div class="como"><b>Como usar</b><ul>'
            '<li>Resolva um tema por vez; anote data e acertos no quadro do tema.</li>'
            '<li>Marque a bolha da resposta; use “dúvida” quando chutou e “revisar” quando errou.</li>'
            '<li>Confira no gabarito ao fim de cada caderno e refaça as marcadas na revisão.</li>'
            '<li>Dificuldade: ● fácil · ●● média · ●●● difícil — cresce dentro de cada tema.</li></ul></div>')
    return f'<section class="sumario"><h2>Sumário</h2><table>{"".join(linhas)}</table>{como}</section>'


def html_volume(cadernos):
    css = (AQUI / "estilo.css").read_text(encoding="utf-8")
    partes, num = [], 1
    for c in cadernos:
        hq, hg = html_caderno(c, num)
        partes += [hq, hg]
        num += sum(len(t["questoes"]) for t in c["temas"])
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Caderno de Questões SEFAZ-RS</title>'
            f'<style>{css}</style></head><body>{_capa(num - 1)}{_sumario(cadernos)}{"".join(partes)}</body></html>')


if __name__ == "__main__":
    saida, arquivos = sys.argv[1], sorted(sys.argv[2:])
    cads = [validar.carregar(a) for a in arquivos]
    pathlib.Path(saida).write_text(html_volume(cads), encoding="utf-8")
    print(f"{saida}: {len(cads)} cadernos")
