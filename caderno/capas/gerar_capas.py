"""Gera 3 opções de capa + contracapa (A4). Uso: python3 gerar_capas.py"""
import math
import pathlib
import random

AQUI = pathlib.Path(__file__).resolve().parent
CADERNOS = [
    ("01", "Direito Tributário", 45), ("02", "ICMS, ITCD e IPVA", 45), ("03", "Reforma Tributária", 15),
    ("04", "Contabilidade Geral e Avançada", 45), ("05", "Contabilidade de Custos", 15), ("06", "Auditoria", 20),
    ("07", "Direito Constitucional", 20), ("08", "Direito Administrativo", 20), ("09", "Direito Empresarial", 15),
    ("10", "Língua Portuguesa", 25), ("11", "Raciocínio Lógico e Mat. Financeira", 20), ("12", "Estatística", 15),
]

BASE_CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: "Inter", sans-serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.pg { width: 210mm; height: 297mm; position: relative; overflow: hidden; page-break-after: always; }
.pg:last-child { page-break-after: auto; }
.prog { width: 100%; border-collapse: collapse; font-size: 10.2pt; }
.prog th { text-align: left; font-size: 7.4pt; letter-spacing: .1em; text-transform: uppercase; font-weight: 600; padding: 0 0 5pt; }
.prog td { padding: 8.6pt 0; border-bottom: .5pt solid var(--linha); vertical-align: middle; }
.prog td.n { width: 9mm; font-weight: 700; }
.prog td.q { width: 14mm; text-align: right; padding-right: 4mm; opacity: .75; }
.prog td.b { width: 22mm; }
.box { display: inline-block; width: 10pt; height: 10pt; border: .8pt solid currentColor; vertical-align: -1pt; margin-right: 3pt; }
.lin { display: inline-block; width: 12mm; border-bottom: .6pt solid currentColor; }
"""


def tabela_progresso():
    linhas = "".join(
        f'<tr><td class="n">{n}</td><td>{m}</td><td class="q">{q} q.</td>'
        f'<td class="b"><i class="box"></i>feito</td><td class="b"><i class="box"></i>revisado</td>'
        f'<td class="b"><span class="lin"></span>%</td></tr>'
        for n, m, q in CADERNOS)
    return ('<table class="prog"><tr><th></th><th>Caderno</th><th style="text-align:right;padding-right:4mm">Qtd.</th>'
            '<th>1ª resolução</th><th>Revisão</th><th>Acertos</th></tr>' + linhas + '</table>')


def pagina(css, capa, contra):
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Capa</title>'
            f'<style>{BASE_CSS}{css}</style></head><body>'
            f'<section class="pg capa">{capa}</section><section class="pg contra">{contra}</section></body></html>')


# ---------- Opção 1: Clássica (faixa com as cores do RS) ----------
def opcao1():
    css = """
:root { --verde:#1d7a3b; --verm:#c62a2f; --amar:#f1c232; --tinta:#141414; --linha:#cfcfcf; }
.capa, .contra { background:#fbfaf7; color:var(--tinta); }
.faixa { position:absolute; top:0; bottom:0; width:16mm; display:flex; flex-direction:column; }
.faixa i { flex:1; } .faixa i:nth-child(1){background:var(--verde);} .faixa i:nth-child(2){background:var(--verm);} .faixa i:nth-child(3){background:var(--amar);}
.capa .faixa { left:0; } .contra .faixa { right:0; }
.capa .miolo { position:absolute; left:34mm; right:20mm; top:26mm; bottom:22mm; display:flex; flex-direction:column; }
.topo { font-size:8.5pt; letter-spacing:.22em; text-transform:uppercase; font-weight:600; border-bottom:1.4pt solid var(--tinta); padding-bottom:5pt; }
.num { font-size:210pt; font-weight:800; line-height:.8; letter-spacing:-.05em; margin-top:22mm; color:transparent; -webkit-text-stroke:2.2pt var(--tinta); }
.num-l { font-size:11pt; font-weight:600; letter-spacing:.18em; text-transform:uppercase; margin:6mm 0 0 2mm; }
h1 { font-size:40pt; line-height:1.02; letter-spacing:-.025em; font-weight:800; margin-top:auto; }
h1 em { font-style:normal; color:var(--verde); }
.sub { font-family:"Caladea",serif; font-size:13pt; margin-top:6mm; color:#333; max-width:130mm; }
.rodape { display:flex; justify-content:space-between; font-size:8pt; letter-spacing:.12em; text-transform:uppercase; border-top:1.4pt solid var(--tinta); padding-top:5pt; margin-top:12mm; }
.contra .miolo { position:absolute; left:20mm; right:32mm; top:24mm; bottom:20mm; display:flex; flex-direction:column; }
.contra h2 { font-size:18pt; font-weight:800; letter-spacing:-.01em; margin-bottom:2mm; }
.contra .lead { font-family:"Caladea",serif; font-size:10.5pt; color:#444; margin-bottom:7mm; }
.dono { margin-top:auto; font-size:9pt; } .dono span { display:inline-block; width:110mm; border-bottom:.8pt solid var(--tinta); margin-left:3mm; }
.nota { font-size:7pt; color:#666; margin-top:6mm; }
"""
    faixa = '<div class="faixa"><i></i><i></i><i></i></div>'
    capa = (f'{faixa}<div class="miolo"><div class="topo">Concurso SEFAZ-RS · 2027</div>'
            '<div class="num">300</div><div class="num-l">questões inéditas · estilo FCC</div>'
            '<h1>Caderno de Questões<br><em>Auditor-Fiscal</em> da<br>Receita Estadual</h1>'
            '<div class="sub">Organizado por matéria e tema, com gabarito comentado e fundamento legal.</div>'
            '<div class="rodape"><span>12 cadernos</span><span>Edição nov. 2026</span></div></div>')
    contra = (f'{faixa}<div class="miolo"><h2>Meu progresso</h2>'
              '<div class="lead">Marque cada caderno ao concluir a primeira resolução e a revisão, e anote o percentual de acertos.</div>'
              f'{tabela_progresso()}'
              '<div class="dono">Este caderno pertence a <span></span></div>'
              '<div class="nota">Questões inéditas elaboradas para estudo, com base na legislação vigente em novembro de 2026. Material sem vínculo com a SEFAZ-RS ou com a banca organizadora.</div></div>')
    return pagina(css, capa, contra)


# ---------- Opção 2: Documento fiscal (escura, código de barras) ----------
def barras(seed, w=170, h=22):
    random.seed(seed)
    x, out = 0.0, []
    while x < w:
        bw = random.choice([0.35, 0.35, 0.7, 1.05, 1.4])
        if random.random() > 0.35:
            out.append(f'<rect x="{x:.2f}" y="0" width="{bw}" height="{h}"/>')
        x += bw + random.choice([0.35, 0.7, 0.7, 1.05])
    return f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="none" width="100%" height="100%">{"".join(out)}</svg>'


def gabarito_fundo():
    refs = ["CTN", "CF/88", "LC 87/96", "LEI 8.820/89", "RICMS/RS", "EC 132/23", "LC 214/25", "LEI 6.404/76", "CPC 00", "NBC TA 200"]
    return " · ".join(refs * 40)


def opcao2():
    css = """
:root { --fundo:#0f1c2e; --creme:#f3ead8; --ouro:#e2b04a; --linha:rgba(243,234,216,.28); }
.capa, .contra { background:var(--fundo); color:var(--creme); }
.grade { position:absolute; inset:0; padding:14mm; font-family:"JetBrains Mono",monospace; font-size:7.2pt; line-height:1.75; letter-spacing:.06em; color:rgba(243,234,216,.07); word-spacing:3pt; }
.capa .miolo { position:absolute; left:22mm; right:22mm; top:22mm; bottom:22mm; display:flex; flex-direction:column; }
.selo { align-self:flex-start; font-family:"JetBrains Mono",monospace; font-size:8pt; letter-spacing:.14em; border:1pt solid var(--ouro); color:var(--ouro); padding:3pt 7pt; text-transform:uppercase; }
.sigla { font-size:150pt; font-weight:800; letter-spacing:-.04em; line-height:.85; margin-top:30mm; }
.sigla span { color:var(--ouro); }
h1 { font-size:21pt; font-weight:700; line-height:1.15; margin-top:7mm; max-width:140mm; }
.meta { display:grid; grid-template-columns:repeat(3,auto); justify-content:start; gap:0 12mm; margin-top:auto; font-family:"JetBrains Mono",monospace; font-size:8pt; text-transform:uppercase; letter-spacing:.1em; }
.meta b { display:block; font-family:"Inter",sans-serif; font-size:22pt; letter-spacing:-.02em; color:var(--ouro); }
.cod { height:16mm; margin-top:9mm; fill:var(--creme); }
.codtxt { font-family:"JetBrains Mono",monospace; font-size:7pt; letter-spacing:.5em; margin-top:2mm; opacity:.8; }
.contra .miolo { position:absolute; left:22mm; right:22mm; top:22mm; bottom:20mm; display:flex; flex-direction:column; }
.contra h2 { font-size:17pt; font-weight:800; color:var(--ouro); margin-bottom:2mm; }
.contra .lead { font-size:9pt; opacity:.8; margin-bottom:7mm; }
.prog td.n { color:var(--ouro); }
.dono { margin-top:auto; font-size:9pt; } .dono span { display:inline-block; width:110mm; border-bottom:.8pt solid var(--creme); margin-left:3mm; }
.nota { font-family:"JetBrains Mono",monospace; font-size:6.5pt; opacity:.6; margin-top:6mm; letter-spacing:.04em; }
.contra .cod { height:10mm; width:60mm; margin-top:6mm; }
"""
    fundo = f'<div class="grade">{gabarito_fundo()}</div>'
    capa = (f'{fundo}<div class="miolo"><div class="selo">Caderno de questões · SEFAZ-RS 2027</div>'
            '<div class="sigla">AFRE<span>.</span></div>'
            '<h1>Auditor-Fiscal da Receita Estadual do Rio Grande do Sul</h1>'
            '<div class="meta"><div><b>300</b>questões</div><div><b>12</b>cadernos</div><div><b>FCC</b>estilo</div></div>'
            f'<div class="cod">{barras(3)}</div><div class="codtxt">RS · 2027 · AFRE · 300Q · FCC</div></div>')
    contra = (f'{fundo}<div class="miolo"><h2>Controle de progresso</h2>'
              '<div class="lead">Registre a primeira resolução, a revisão e o percentual de acertos de cada caderno.</div>'
              f'{tabela_progresso()}'
              '<div class="dono">Este caderno pertence a <span></span></div>'
              '<div class="nota">Questões inéditas para estudo · legislação vigente em nov./2026 · material sem vínculo com a SEFAZ-RS ou com a banca.</div>'
              f'<div class="cod">{barras(11, 120, 22)}</div></div>')
    return pagina(css, capa, contra)


# ---------- Opção 3: Pampa (curvas de nível) ----------
def curvas(seed, n=26, w=210, h=297, cor="#ffffff", op=0.22):
    random.seed(seed)
    fases = [random.uniform(0, 6.28) for _ in range(4)]
    paths = []
    for k in range(n):
        y0 = -20 + k * (h + 40) / n
        pts = []
        for i in range(0, 61):
            x = i * w / 60
            y = (y0 + 7 * math.sin(x / 23 + fases[0] + k * .18) + 4 * math.sin(x / 9 + fases[1] + k * .31)
                 + 3 * math.sin(x / 41 + fases[2]) + 9 * math.sin(k / 5 + fases[3]) * math.sin(x / 70))
            pts.append(f"{x:.1f},{y:.1f}")
        paths.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{cor}" stroke-opacity="{op}" stroke-width="{0.5 if k % 5 else 0.9}"/>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="none">{"".join(paths)}</svg>'


def opcao3():
    css = """
:root { --pampa1:#1f5e3a; --pampa2:#2f8a52; --sol:#f2c94c; --branco:#ffffff; --linha:#c9d8cd; --tinta:#173b26; }
.capa { background:linear-gradient(165deg,var(--pampa2) 0%,var(--pampa1) 70%,#163f28 100%); color:var(--branco); }
.contra { background:#f4f7f2; color:var(--tinta); }
.curvas { position:absolute; inset:0; }
.sol { position:absolute; width:62mm; height:62mm; border-radius:50%; background:var(--sol); right:24mm; top:30mm; }
.capa .miolo { position:absolute; left:22mm; right:22mm; top:24mm; bottom:22mm; display:flex; flex-direction:column; }
.topo { font-size:8.5pt; letter-spacing:.24em; text-transform:uppercase; font-weight:600; }
h1 { font-family:"Caladea",serif; font-weight:700; font-size:46pt; line-height:1.02; margin-top:auto; letter-spacing:-.01em; }
.sub { font-size:11pt; margin-top:6mm; max-width:140mm; opacity:.92; line-height:1.4; }
.chips { display:flex; gap:3mm; margin-top:10mm; flex-wrap:wrap; }
.chips span { border:1pt solid rgba(255,255,255,.75); border-radius:20pt; padding:3pt 10pt; font-size:8.5pt; font-weight:600; letter-spacing:.04em; }
.contra .curvas { opacity:1; }
.contra .miolo { position:absolute; left:22mm; right:22mm; top:24mm; bottom:20mm; display:flex; flex-direction:column; }
.contra h2 { font-family:"Caladea",serif; font-size:22pt; color:var(--pampa1); margin-bottom:2mm; }
.contra .lead { font-size:9.5pt; color:#3d5a47; margin-bottom:7mm; }
.prog td.n { color:var(--pampa2); }
.frase { font-family:"Caladea",serif; font-style:italic; font-size:12pt; color:var(--pampa1); margin-top:8mm; }
.dono { margin-top:auto; font-size:9pt; } .dono span { display:inline-block; width:110mm; border-bottom:.8pt solid var(--tinta); margin-left:3mm; }
.nota { font-size:7pt; color:#5d7465; margin-top:6mm; }
"""
    capa = (f'<div class="sol"></div><div class="curvas">{curvas(5)}</div>'
            '<div class="miolo"><div class="topo">Rio Grande do Sul · Concurso 2027</div>'
            '<h1>Caderno de Questões<br>Auditor-Fiscal da<br>Receita Estadual</h1>'
            '<div class="sub">300 questões inéditas no estilo FCC, organizadas por matéria e tema, com gabarito comentado e fundamento legal.</div>'
            '<div class="chips"><span>12 cadernos</span><span>Tributário · ICMS</span><span>Contabilidade</span><span>Reforma Tributária</span></div></div>')
    contra = (f'<div class="curvas">{curvas(9, cor="#2f8a52", op=0.10)}</div><div class="miolo"><h2>Meu progresso</h2>'
              '<div class="lead">Marque cada caderno ao concluir a primeira resolução e a revisão, e anote o percentual de acertos.</div>'
              f'{tabela_progresso()}'
              '<div class="frase">Uma questão por vez. Um tema por dia.</div>'
              '<div class="dono">Este caderno pertence a <span></span></div>'
              '<div class="nota">Questões inéditas elaboradas para estudo, com base na legislação vigente em novembro de 2026. Material sem vínculo com a SEFAZ-RS ou com a banca organizadora.</div></div>')
    return pagina(css, capa, contra)


if __name__ == "__main__":
    for i, f in enumerate([opcao1, opcao2, opcao3], 1):
        (AQUI / f"capa-opcao-{i}.html").write_text(f(), encoding="utf-8")
    print("ok")
