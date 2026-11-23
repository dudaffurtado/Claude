"""Gera 3 capas + contracapas no estilo 'cartaz retrô/divertido'. Uso: python3 gerar_capas2.py"""
import math
import pathlib

AQUI = pathlib.Path(__file__).resolve().parent
CADERNOS = [
    ("01", "Direito Tributário", 45), ("02", "ICMS, ITCD e IPVA", 45), ("03", "Reforma Tributária", 15),
    ("04", "Contabilidade Geral e Avançada", 45), ("05", "Contabilidade de Custos", 15), ("06", "Auditoria", 20),
    ("07", "Direito Constitucional", 20), ("08", "Direito Administrativo", 20), ("09", "Direito Empresarial", 15),
    ("10", "Língua Portuguesa", 25), ("11", "Raciocínio Lógico e Mat. Financeira", 20), ("12", "Estatística", 15),
]

BASE = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { -webkit-print-color-adjust: exact; print-color-adjust: exact; font-family: "DM Sans", sans-serif; }
.pg { width: 210mm; height: 297mm; position: relative; overflow: hidden; page-break-after: always; }
.pg:last-child { page-break-after: auto; }
.abs { position: absolute; }
.prog { width: 100%; border-collapse: collapse; font-size: 10pt; }
.prog th { text-align: left; font-size: 7pt; letter-spacing: .12em; text-transform: uppercase; font-weight: 800; padding: 0 0 6pt; }
.prog td { padding: 7.4pt 0; border-bottom: 1pt dashed var(--linha); }
.prog td.n { width: 9mm; font-weight: 800; }
.prog td.q { width: 13mm; text-align: right; padding-right: 4mm; opacity: .7; }
.prog td.b { width: 21mm; white-space: nowrap; }
.box { display: inline-block; width: 10pt; height: 10pt; border: 1.2pt solid currentColor; border-radius: 3pt; vertical-align: -1.5pt; margin-right: 3pt; }
.lin { display: inline-block; width: 11mm; border-bottom: 1pt solid currentColor; }
.aviso { font-size: 6.8pt; opacity: .7; }
"""


def tabela():
    linhas = "".join(
        f'<tr><td class="n">{n}</td><td>{m}</td><td class="q">{q} q.</td>'
        f'<td class="b"><i class="box"></i>feito</td><td class="b"><i class="box"></i>revisado</td>'
        f'<td class="b"><span class="lin"></span> %</td></tr>' for n, m, q in CADERNOS)
    return ('<table class="prog"><tr><th></th><th>Caderno</th><th style="text-align:right;padding-right:4mm">Qtd.</th>'
            '<th>1ª vez</th><th>Revisão</th><th>Acertos</th></tr>' + linhas + '</table>')


AVISO = ("Questões inéditas para estudo, com base na legislação vigente em novembro de 2026. "
         "Material independente, sem vínculo com a SEFAZ-RS ou com a banca organizadora.")


def doc(css, capa, contra, quarta=None):
    return ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Capa</title>'
            f'<link rel="stylesheet" href="fontes/fontes.css"><style>{BASE}{css}</style></head><body>'
            f'<section class="pg capa">{capa}</section><section class="pg contra">{contra}</section>'
            + (f'<section class="pg quarta">{quarta}</section>' if quarta else '') + '</body></html>')


def estrela_raios(cx, cy, raios, r_in, r_out, cor, larg=1.6):
    """Explosão de raios finos (como o 'sol' do cartaz Black Week)."""
    linhas = []
    for i in range(raios):
        a = 2 * math.pi * i / raios
        comp = r_out if i % 2 == 0 else r_out * 0.62
        linhas.append(f'<line x1="{cx + r_in * math.cos(a):.1f}" y1="{cy + r_in * math.sin(a):.1f}" '
                      f'x2="{cx + comp * math.cos(a):.1f}" y2="{cy + comp * math.sin(a):.1f}" '
                      f'stroke="{cor}" stroke-width="{larg}" stroke-linecap="round"/>')
    return "".join(linhas)


def brilho(cx, cy, r, cor):
    """Estrelinha de 4 pontas."""
    k = r * 0.18
    return (f'<path d="M{cx},{cy - r} Q{cx + k},{cy - k} {cx + r},{cy} Q{cx + k},{cy + k} {cx},{cy + r} '
            f'Q{cx - k},{cy + k} {cx - r},{cy} Q{cx - k},{cy - k} {cx},{cy - r}Z" fill="{cor}"/>')


# ======================= Estilo 1 — Tipográfico (bege, raios laranja, selo rosa) =======================
def estilo1():
    css = """
:root { --bege:#e8dac7; --creme:#fbf5ec; --laranja:#ee8a58; --rosa:#e6a3c8; --marrom:#6e5140; --linha:#b9a38c; }
.pg { background: var(--bege); }
.rep { position:absolute; left:-40mm; right:-40mm; top:-22mm; color:var(--creme); line-height:.86; text-align:center; }
.rep .it { font-family:"Fraunces",serif; font-style:italic; font-weight:400; font-size:118pt; letter-spacing:-.02em; }
.rep .up { font-family:"Fraunces",serif; font-weight:600; font-size:112pt; letter-spacing:.01em; }
.raios { position:absolute; inset:0; }
.selo { position:absolute; left:18mm; top:182mm; width:82mm; height:82mm; border-radius:50%; background:var(--rosa);
        display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;
        color:var(--creme); transform:rotate(-8deg); font-family:"DM Sans",sans-serif; }
.selo b { font-family:"Fraunces",serif; font-weight:600; font-size:44pt; line-height:1; }
.selo span { font-size:12pt; letter-spacing:.16em; text-transform:uppercase; font-weight:600; line-height:1.35; }
.rodape { position:absolute; right:14mm; bottom:12mm; text-align:right; color:var(--marrom); font-size:9pt; letter-spacing:.2em; text-transform:uppercase; font-weight:600; }
.rodape i { display:block; font-family:"Fraunces",serif; font-style:italic; text-transform:none; letter-spacing:0; font-size:15pt; font-weight:400; }
.cartao { position:absolute; left:16mm; right:16mm; top:34mm; bottom:16mm; background:var(--creme); border-radius:9mm; padding:12mm 12mm 9mm; color:var(--marrom); display:flex; flex-direction:column; }
.cartao h2 { font-family:"Fraunces",serif; font-style:italic; font-weight:400; font-size:30pt; line-height:1; color:var(--laranja); }
.cartao .lead { font-size:9.5pt; margin:3mm 0 7mm; }
.dono { margin-top:auto; font-size:10pt; } .dono span { display:inline-block; width:105mm; border-bottom:1pt solid var(--marrom); margin-left:2mm; }
.aviso { margin-top:5mm; }
.quarta .rep { opacity:.55; }
.quarta .raios { opacity:.9; }
.q-miolo { position:absolute; left:18mm; right:18mm; top:22mm; bottom:16mm; display:flex; flex-direction:column; color:var(--marrom); }
.q-titulo { font-family:"Fraunces",serif; font-style:italic; font-weight:400; font-size:38pt; line-height:1.02; color:var(--marrom); max-width:150mm; }
.q-titulo b { font-weight:600; color:var(--laranja); }
.q-texto { background:var(--creme); border-radius:7mm; padding:8mm 9mm; margin-top:9mm; font-size:10.5pt; line-height:1.5; }
.q-texto p + p { margin-top:3mm; }
.q-lista { display:grid; grid-template-columns:1fr 1fr; gap:3mm 6mm; margin-top:6mm; }
.q-lista div { font-size:9.5pt; line-height:1.35; padding-left:7mm; position:relative; }
.q-lista div::before { content:"✳"; position:absolute; left:0; top:-.5pt; color:var(--laranja); font-size:11pt; }
.q-lista b { display:block; font-family:"Fraunces",serif; font-style:italic; font-weight:600; font-size:12pt; color:var(--marrom); }
.q-materias { margin-top:7mm; display:flex; flex-wrap:wrap; gap:2.2mm; }
.q-materias span { background:var(--creme); border-radius:20pt; padding:3.5pt 10pt; font-size:8.6pt; font-weight:600; }
.q-selo { position:absolute; right:14mm; bottom:34mm; width:46mm; height:46mm; border-radius:50%; background:var(--rosa); color:var(--creme);
          display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; transform:rotate(8deg); }
.q-selo b { font-family:"Fraunces",serif; font-style:italic; font-weight:400; font-size:17pt; line-height:1.05; }
.q-selo span { font-size:7.6pt; letter-spacing:.14em; text-transform:uppercase; font-weight:600; margin-top:1.5mm; line-height:1.3; }
.q-rodape { margin-top:auto; display:flex; justify-content:space-between; align-items:flex-end; font-size:8pt; letter-spacing:.18em; text-transform:uppercase; font-weight:600; }
.q-rodape i { font-family:"Fraunces",serif; font-style:italic; font-size:14pt; letter-spacing:0; text-transform:none; font-weight:400; }
.q-aviso { font-size:6.8pt; opacity:.75; margin-top:3mm; max-width:120mm; }
.contra .topo { position:absolute; left:0; right:0; top:4mm; text-align:center; font-family:"Fraunces",serif; font-style:italic; font-size:52pt; color:var(--creme); line-height:1; }
"""
    linhas = []
    for i in range(8):
        if i % 2 == 0:
            linhas.append('<div class="it">Auditor</div>')
        else:
            linhas.append('<div class="up">FISCAL</div>')
    raios = f'<svg class="raios" viewBox="0 0 210 297">{estrela_raios(176, 150, 16, 9, 70, "#ee8a58", 1.3)}</svg>'
    capa = (f'<div class="rep">{"".join(linhas)}</div>{raios}'
            '<div class="selo"><b>300</b><span>questões<br>inéditas<br>estilo FCC</span></div>'
            '<div class="rodape"><i>Caderno de Questões</i>SEFAZ-RS · 2027</div>')
    contra = ('<div class="topo">rumo à aprovação</div>'
              '<div class="cartao"><h2>Meu progresso</h2>'
              '<div class="lead">Marque cada caderno ao terminar a primeira resolução e a revisão, e anote os acertos.</div>'
              f'{tabela()}<div class="dono">Este caderno pertence a <span></span></div>'
              f'<div class="aviso">{AVISO}</div></div>')
    materias = "".join(f'<span>{m}</span>' for _, m, _ in CADERNOS)
    raios_q = f'<svg class="raios" viewBox="0 0 210 297">{estrela_raios(192, 26, 16, 7, 48, "#ee8a58", 1.2)}</svg>'
    quarta = (f'<div class="rep">{"".join(linhas)}</div>{raios_q}'
              '<div class="q-miolo">'
              '<div class="q-titulo">Questão por questão,<br><b>a aprovação vem.</b></div>'
              '<div class="q-texto">'
              '<p>Este caderno reúne <b>300 questões inéditas</b>, elaboradas no estilo da Fundação Carlos Chagas para quem se prepara para o concurso de '
              '<b>Auditor-Fiscal da Receita Estadual do Rio Grande do Sul</b>.</p>'
              '<p>São 12 cadernos e 69 temas, com as questões em ordem crescente de dificuldade, espaço para resolver à mão '
              'e gabarito comentado ao fim de cada caderno, com o fundamento legal de cada resposta.</p>'
              '<div class="q-lista">'
              '<div><b>Feito para o papel</b>Bolhas para marcar, caixas de “dúvida” e “revisar” e quadro de acertos por tema.</div>'
              '<div><b>Gabarito que ensina</b>Por que a certa está certa e onde está a pegadinha de cada errada.</div>'
              '<div><b>Legislação em dia</b>Inclui a Reforma Tributária, com a EC 132/2023, a LC 214/2025, o IBS, a CBS e o Imposto Seletivo.</div>'
              '<div><b>O jeito da FCC</b>Letra da lei, itens I a IV, casos práticos e as trocas de palavras que a banca adora.</div>'
              '</div></div>'
              f'<div class="q-materias">{materias}</div>'
              '<div class="q-rodape"><div><i>Caderno de Questões</i><br>SEFAZ-RS · 2027</div><div>estilo FCC</div></div>'
              f'<div class="q-aviso">{AVISO}</div></div>'
              '<div class="q-selo"><b>legislação<br>de nov./2026</b><span>inclui reforma<br>tributária</span></div>')
    return doc(css, capa, contra, quarta)


# ======================= Estilo 2 — Xadrez amarelo com moldura =======================
def moldura_svg(w, h, cor_borda, cor_zig, cor_ponto):
    """Moldura vermelha pontilhada + borda azul em zigue-zague, em mm."""
    m = 14          # margem externa
    b = 7           # espessura da faixa vermelha
    partes = [f'<rect x="{m}" y="{m}" width="{w - 2 * m}" height="{h - 2 * m}" fill="none" stroke="{cor_borda}" stroke-width="{b}"/>']
    # pontinhos brancos na faixa vermelha
    passo = 9
    x = m + 4
    while x < w - m - 2:
        partes.append(f'<circle cx="{x:.1f}" cy="{m}" r=".75" fill="{cor_ponto}"/><circle cx="{x:.1f}" cy="{h - m}" r=".75" fill="{cor_ponto}"/>')
        x += passo
    y = m + 4
    while y < h - m - 2:
        partes.append(f'<circle cx="{m}" cy="{y:.1f}" r=".75" fill="{cor_ponto}"/><circle cx="{w - m}" cy="{y:.1f}" r=".75" fill="{cor_ponto}"/>')
        y += passo
    # zigue-zague azul (dentes voltados para dentro)
    zi = m + b / 2 + 2.5   # borda interna da moldura
    dente, alt = 5, 4.2

    def lado(x0, y0, x1, y1, nx, ny):
        comp = math.hypot(x1 - x0, y1 - y0)
        n = int(comp // dente)
        ux, uy = (x1 - x0) / comp, (y1 - y0) / comp
        pts = []
        for i in range(n + 1):
            px, py = x0 + ux * i * dente, y0 + uy * i * dente
            pts.append(f"{px:.1f},{py:.1f}")
            if i < n:
                mx, my = px + ux * dente / 2 + nx * alt, py + uy * dente / 2 + ny * alt
                pts.append(f"{mx:.1f},{my:.1f}")
        return f'<polygon points="{" ".join(pts)}" fill="{cor_zig}"/>'
    partes.append(f'<rect x="{zi - .8}" y="{zi - .8}" width="{w - 2 * zi + 1.6}" height="{h - 2 * zi + 1.6}" fill="none" stroke="{cor_zig}" stroke-width="1.6"/>')
    partes.append(lado(zi, zi, w - zi, zi, 0, 1))
    partes.append(lado(zi, h - zi, w - zi, h - zi, 0, -1))
    partes.append(lado(zi, zi, zi, h - zi, 1, 0))
    partes.append(lado(w - zi, zi, w - zi, h - zi, -1, 0))
    # linha fina interna vermelha
    li = zi + alt + 4
    partes.append(f'<rect x="{li}" y="{li}" width="{w - 2 * li}" height="{h - 2 * li}" fill="none" stroke="{cor_borda}" stroke-width=".8" rx="1"/>')
    return f'<svg class="abs" style="inset:0" viewBox="0 0 {w} {h}" width="100%" height="100%">{"".join(partes)}</svg>'


def estilo2():
    css = """
:root { --amarelo:#fbf2c0; --xadrez:rgba(240,206,72,.55); --verm:#c73a52; --azul:#8fc4d0; --branco:#fffdf4; --linha:#d7a7af; }
.pg { background-color:var(--amarelo);
      background-image:linear-gradient(90deg,var(--xadrez) 50%,transparent 50%),linear-gradient(var(--xadrez) 50%,transparent 50%);
      background-size:9mm 9mm; }
.capa .txt { position:absolute; left:34mm; right:34mm; top:40mm; bottom:40mm; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; color:var(--verm); font-family:"Sniglet",cursive; }
.capa .p { font-size:28pt; font-weight:800; letter-spacing:.02em; }
.capa .g { font-size:78pt; font-weight:800; line-height:.95; margin:1mm 0; }
.capa .m { font-size:52pt; font-weight:800; line-height:1; }
.capa .fita { margin-top:8mm; font-size:15pt !important; background:var(--verm); color:var(--branco); font-size:13pt; font-weight:800; padding:3pt 14pt; border-radius:30pt; transform:rotate(-3deg); }
.capa .sub { margin-top:7mm; font-family:"DM Sans",sans-serif; font-size:10.5pt; font-weight:600; color:#8c2e3f; letter-spacing:.06em; text-transform:uppercase; }
.contra .painel { position:absolute; left:34mm; right:34mm; top:36mm; bottom:34mm; background:var(--branco); border-radius:4mm; padding:9mm 9mm 7mm; color:#7a2536; display:flex; flex-direction:column; }
.contra h2 { font-family:"Sniglet",cursive; font-weight:800; font-size:26pt; color:var(--verm); text-align:center; }
.contra .lead { font-size:9pt; text-align:center; margin:1mm 0 6mm; }
.contra .prog { font-size:9pt; } .contra .prog td { padding:6.2pt 0; } .contra .prog td.b { width:19mm; }
.contra .dono { margin-top:auto; font-size:9.5pt; } .contra .dono span { display:inline-block; width:78mm; border-bottom:1pt solid #7a2536; margin-left:2mm; }
.contra .aviso { margin-top:4mm; text-align:center; }
"""
    mold = moldura_svg(210, 297, "#c73a52", "#8fc4d0", "#fffdf4")
    capa = (f'{mold}<div class="txt"><div class="p">CADERNO DE</div><div class="g">QUES<br>TÕES</div>'
            '<div class="m">AUDITOR<br>FISCAL</div><div class="p" style="margin-top:3mm">SEFAZ · RS</div>'
            '<div class="fita">a prova vem. estuda logo!</div>'
            '<div class="sub">300 questões · estilo FCC · 2027</div></div>')
    contra = (f'{mold}<div class="painel"><h2>MEU PROGRESSO</h2>'
              '<div class="lead">Marque cada caderno ao terminar a primeira vez e a revisão, e anote os acertos.</div>'
              f'{tabela()}<div class="dono">Este caderno pertence a <span></span></div>'
              f'<div class="aviso">{AVISO}</div></div>')
    return doc(css, capa, contra)


# ======================= Estilo 3 — Listras + chimarrão =======================
def listras_svg(cor, n=9, op=1.0, seed=2):
    faixas = []
    for i in range(n):
        y = 6 + i * 33
        faixas.append(f'<rect x="-10" y="{y}" width="230" height="17" fill="{cor}" opacity="{op}" filter="url(#aquarela{seed})"/>')
    return (f'<svg class="abs" style="inset:0" viewBox="0 0 210 297" width="100%" height="100%" preserveAspectRatio="none">'
            f'<defs><filter id="aquarela{seed}" x="-5%" y="-30%" width="110%" height="160%">'
            f'<feTurbulence type="fractalNoise" baseFrequency=".035 .6" numOctaves="3" seed="{seed}" result="r"/>'
            f'<feDisplacementMap in="SourceGraphic" in2="r" scale="4.5"/></filter></defs>{"".join(faixas)}</svg>')


def arcos(cx, cy, cor, n=4, r0=10, passo=8, larg=4.2):
    return "".join(f'<circle cx="{cx}" cy="{cy}" r="{r0 + i * passo}" fill="none" stroke="{cor}" stroke-width="{larg}"/>' for i in range(n))


def cuia(cx, cy, s, verm, creme, erva):
    """Cuia de chimarrão com bomba, em traço retrô. (cx, cy) = centro do bojo; s = escala."""
    def P(x, y):
        return f"{cx + x * s:.1f},{cy + y * s:.1f}"
    corpo = (f'M{P(-14, -12)} C{P(-16, -4)} {P(-24, 2)} {P(-23, 14)} C{P(-22, 27)} {P(-10, 33)} {P(0, 33)} '
             f'C{P(10, 33)} {P(22, 27)} {P(23, 14)} C{P(24, 2)} {P(16, -4)} {P(14, -12)} Z')
    boca = f'<ellipse cx="{cx}" cy="{cy - 12 * s:.1f}" rx="{14 * s:.1f}" ry="{4 * s:.1f}" fill="{verm}"/>'
    erva_m = f'<ellipse cx="{cx - 2 * s:.1f}" cy="{cy - 12.6 * s:.1f}" rx="{11.5 * s:.1f}" ry="{2.8 * s:.1f}" fill="{erva}"/>'
    bomba = (f'<path d="M{P(4, -11)} L{P(13, -40)} Q{P(14.5, -44)} {P(18, -44)} L{P(22, -44)}" fill="none" '
             f'stroke="{verm}" stroke-width="{2.6 * s:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<path d="M{P(4, -11)} L{P(13, -40)} Q{P(14.5, -44)} {P(18, -44)} L{P(22, -44)}" fill="none" '
             f'stroke="{creme}" stroke-width="{1 * s:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    faixa = (f'<path d="M{P(-21, 6)} Q{P(0, 11)} {P(21, 6)}" fill="none" stroke="{creme}" stroke-width="{1.6 * s:.1f}"/>'
             f'<path d="M{P(-22.6, 12)} Q{P(0, 17)} {P(22.6, 12)}" fill="none" stroke="{creme}" stroke-width="{1.6 * s:.1f}"/>')
    pontos = "".join(f'<circle cx="{cx + x * s:.1f}" cy="{cy + (9.2 + abs(x) * -0.02) * s:.1f}" r="{.9 * s:.1f}" fill="{creme}"/>'
                     for x in range(-16, 17, 4))
    base = f'<ellipse cx="{cx}" cy="{cy + 33.5 * s:.1f}" rx="{11 * s:.1f}" ry="{2 * s:.1f}" fill="{verm}" opacity=".35"/>'
    brilho_cuia = f'<path d="M{P(-15, 0)} Q{P(-18, 12)} {P(-12, 22)}" fill="none" stroke="{creme}" stroke-width="{1.4 * s:.1f}" stroke-linecap="round" opacity=".8"/>'
    vapor = "".join(f'<path d="M{P(x, -20)} q{2 * s:.1f},{-4 * s:.1f} 0,{-8 * s:.1f} q{-2 * s:.1f},{-4 * s:.1f} 0,{-8 * s:.1f}" fill="none" '
                    f'stroke="{verm}" stroke-width="{1.2 * s:.1f}" stroke-linecap="round" opacity=".7"/>' for x in (-8, -2))
    return f'{base}<path d="{corpo}" fill="{verm}"/>{boca}{erva_m}{faixa}{pontos}{brilho_cuia}{bomba}{vapor}'


def estilo3():
    css = """
:root { --creme:#f8ecdc; --amarelo:#e6c13a; --verm:#b5403d; --erva:#7f8f3a; --linha:#d9b99a; }
.pg { background:var(--creme); }
.capa h1 { position:absolute; left:0; right:0; text-align:center; font-family:"Anton",sans-serif; color:var(--verm); font-weight:400; letter-spacing:.01em; line-height:1;
           text-shadow: 1.6pt 1.6pt 0 var(--creme), -1.6pt -1.6pt 0 var(--creme), 1.6pt -1.6pt 0 var(--creme), -1.6pt 1.6pt 0 var(--creme); }
.capa .t1 { top:44mm; font-size:50pt; }
.capa .t2 { top:205mm; font-size:56pt; }
.capa .info { position:absolute; left:38mm; right:38mm; bottom:20mm; background:var(--creme); border:1.4pt solid var(--verm); border-radius:30pt; padding:6pt 14pt; text-align:center; color:var(--verm); font-weight:800; font-size:10pt; letter-spacing:.08em; text-transform:uppercase; }
.capa .info span { display:block; font-family:"Caveat",cursive; text-transform:none; letter-spacing:0; font-size:17pt; font-weight:700; line-height:1.05; }
.contra .painel { position:absolute; left:20mm; right:20mm; top:30mm; bottom:22mm; background:var(--creme); border:1.6pt solid var(--verm); border-radius:8mm; padding:10mm 11mm 8mm; color:#7b2c29; display:flex; flex-direction:column; }
.contra h2 { font-family:"Anton",sans-serif; font-weight:400; font-size:30pt; color:var(--verm); line-height:1; }
.contra .lead { font-family:"Caveat",cursive; font-size:16pt; margin:1mm 0 5mm; }
.contra .dono { margin-top:auto; font-size:10pt; } .contra .dono span { display:inline-block; width:105mm; border-bottom:1pt solid #7b2c29; margin-left:2mm; }
.contra .aviso { margin-top:5mm; }
"""
    arte = (f'<svg class="abs" style="inset:0" viewBox="0 0 210 297" width="100%" height="100%">'
            f'{arcos(40, -6, "#b5403d", 5, 14, 9, 4.6)}{arcos(196, -2, "#b5403d", 3, 10, 9, 4.6)}'
            f'{arcos(-4, 300, "#b5403d", 4, 14, 9, 4.6)}{arcos(150, 312, "#b5403d", 5, 12, 9, 4.6)}'
            f'{cuia(105, 150, 1.55, "#b5403d", "#f8ecdc", "#7f8f3a")}'
            f'{brilho(46, 120, 9, "#b5403d")}{brilho(36, 146, 5, "#b5403d")}{brilho(166, 118, 8, "#b5403d")}{brilho(176, 142, 5, "#b5403d")}'
            '</svg>')
    capa = (f'{listras_svg("#e6c13a")}{arte}'
            '<h1 class="t1">TOMA TEU CHIMARRÃO</h1><h1 class="t2">E VAI ESTUDAR!</h1>'
            '<div class="info"><span>Caderno de Questões</span>Auditor-Fiscal · SEFAZ-RS 2027 · 300 questões estilo FCC</div>')
    arte2 = (f'<svg class="abs" style="inset:0" viewBox="0 0 210 297" width="100%" height="100%">'
             f'{arcos(200, -4, "#b5403d", 4, 10, 8, 4)}{arcos(8, 302, "#b5403d", 4, 10, 8, 4)}</svg>')
    contra = (f'{listras_svg("#e6c13a", op=.55, seed=5)}{arte2}<div class="painel"><h2>MEU PROGRESSO</h2>'
              '<div class="lead">um caderno de cada vez, tchê!</div>'
              f'{tabela()}<div class="dono">Este caderno pertence a <span></span></div>'
              f'<div class="aviso">{AVISO}</div></div>')
    return doc(css, capa, contra)


if __name__ == "__main__":
    for i, f in enumerate([estilo1, estilo2, estilo3], 1):
        (AQUI / f"capa-retro-{i}.html").write_text(f(), encoding="utf-8")
    print("ok")
